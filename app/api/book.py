#!/usr/bin/python
# encoding: utf-8

# @file: book.py
# @time: 2018/4/10 1:10
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from flask import request, current_app

from util.common import is_isbn, Token

from . import api
from .view_modes import BookCollection, ResponseModel, BookViewModel, BookDetail, TradeInfo
from ..forms import SearchForm, IsbnForm, ReqDonateForm, DetailForm
from ..spider import DouBanBook
from ..models import Wish, Gift, BookModel, User, db
from ..error import ErrorCode


@api.route('/api/book/search', methods=['GET'])
def search():
    """
    图书检索
    :return:
    """
    # 参数校验
    form = SearchForm(request.args)
    if form.validate():
        q = form.q.data.strip()
        dou_book = DouBanBook()

        if is_isbn(q):
            dou_book.search_by_isbn(q)
        else:
            dou_book.search_by_keyword(q, page=form.page.data)

        books = BookCollection().fill(dou_book, q)

        return ResponseModel(dataObj=books).to_response()

    else:
        return ResponseModel(dataObj=form.errors).to_response()


@api.route('/api/book/details', methods=['GET'])
def details():
    token = request.headers.get('token')
    user = None
    if token:
        openId = Token.get_openid(token)
        user = User.find_user_by_openid(openId)

    form = DetailForm(request.args)
    if form.validate():

        return _book_details(form.isbn.data, user.id if user else None,
                             gid=form.gid.data, wid=form.wid.data).to_response()

    else:
        return ResponseModel(msg_code=ErrorCode.ISBN_CODE_ERROR,
                             msg='ISBN编号错误', check=False
                             ).to_response()


@api.route('/api/book/gift', methods=['GET'])
def donate():
    token = request.headers.get('token')
    openId = Token.get_openid(token)
    form = IsbnForm(request.args)
    if token is None or openId is None:
        return ResponseModel(msg_code=ErrorCode.TOKEN_IS_MUST,
                             msg='Token无效请登录',
                             check=False).to_response()

    if form.validate():
        isbn = form.isbn.data
        user = User.find_user_by_openid(openId)
        if user.can_save_to_list(isbn):
            gift = Gift()
            gift.bid = BookModel.find_book_by_isbn(isbn).id

            gift.uid = user.id
            gift.isbn = isbn
            # 赠书成本，鱼豆增加
            user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            gift.save()
            return ResponseModel({"num": gift.gifts_count}, check=False).to_response()
        else:
            return ResponseModel(msg_code=ErrorCode.ALREADY_IN_GIFT_OR_WISH,
                                 msg='这本书已经添加至你的赠送清单或已存在于你的心意清单，请不要重复添加',
                                 check=False).to_response()
    else:
        return ResponseModel(msg_code=ErrorCode.ISBN_CODE_ERROR,
                             msg='ISBN编号错误',
                             check=False).to_response()


@api.route('/api/book/wish')
def addWish():
    token = request.headers.get('token')
    openId = Token.get_openid(token)
    form = IsbnForm(request.args)
    if token is None or openId is None:
        return ResponseModel(msg_code=ErrorCode.TOKEN_IS_MUST,
                             msg='Token无效请登录',
                             check=False).to_response()

    if form.validate():
        isbn = form.isbn.data
        user = User.find_user_by_openid(openId)
        if user.can_save_to_list(isbn):
            bid = BookModel.find_book_by_isbn(isbn).id
            wis = Wish(user.id, isbn, bid)
            if user.beans - current_app.config['BEANS_WISH_ONE_BOOK'] < 0:
                return ResponseModel(msg_code=ErrorCode.BEANS_NOT_ENOUGH,
                                     msg='书豆余额不足，赠送图书可获取',
                                     check=False).to_response()
            user.beans -= current_app.config['BEANS_WISH_ONE_BOOK']
            wis.save()
            return ResponseModel({"num": wis.wishes_count}, check=False).to_response()
        else:
            return ResponseModel(msg_code=ErrorCode.ALREADY_IN_GIFT_OR_WISH,
                                 msg='这本书已经添加至你的赠送清单或已存在于你的心意清单，请不要重复添加',
                                 check=False).to_response()
    else:
        return ResponseModel(msg_code=ErrorCode.ISBN_CODE_ERROR,
                             msg='ISBN编号错误',
                             check=False).to_response()


@api.route('/api/book/recent')
def recent_gift():
    recent_gifts = Gift.recent()
    recent_books = [BookViewModel(gift.book) for gift in recent_gifts]
    return ResponseModel(dataObj=recent_books).to_response()


@api.route('/api/book/requestBook', methods=['GET'])
def requestBook():
    token = request.headers.get('token')
    openId = Token.get_openid(token)

    form = ReqDonateForm(request.args)

    if form.validate() and openId is not None:
        requester = User.find_user_by_openid(openId)

        gift = Gift.query.filter_by(id=form.tid.data, launched=False).first()
        wish = Wish.query.filter_by(uid=requester.id, isbn=gift.isbn, launched=False).first()

        #
        if wish.uid != requester.id:
            return ResponseModel(msg_code=ErrorCode.ISBN_CODE_ERROR,
                                 msg='不能赠送别人的数据哟',
                                 check=False).to_response()

        wish.launched = True
        wish.benefactor = gift.uid

        gift.launched = True
        gift.receiver = requester.id

        requester.send_counter += 1
        try:
            db.session.commit()
        except Exception as e:
            return ResponseModel(msg_code=ErrorCode.SERVER_ERROR,
                                 msg='服务器内部错误',
                                 check=False).to_response()

        return _book_details(gift.isbn, uid=requester.id, gid=form.tid.data).to_response()

    else:
        return ResponseModel(msg_code=ErrorCode.PARAMETERS_ERROR, msg='参数错误',
                             check=False).to_response()


@api.route('/api/book/donateBook', methods=['GET'])
def donateBook():
    token = request.headers.get('token')
    openId = Token.get_openid(token)

    form = ReqDonateForm(request.args)
    print(form.data)

    if form.validate() and openId is not None:
        sender = User.find_user_by_openid(openId)

        wish = Wish.query.filter_by(id=form.tid.data, launched=False).first()
        gift = Gift.query.filter_by(uid=sender.id, isbn=wish.isbn, launched=False).first()

        if gift.uid != sender.id:
            return ResponseModel(msg_code=ErrorCode.ISBN_CODE_ERROR,
                                 msg='不能赠送别人的数据哟',
                                 check=False).to_response()

        wish.launched = True
        wish.benefactor = sender.id

        gift.launched = True
        gift.receiver = wish.uid

        sender.send_counter += 1
        try:
            db.session.commit()
        except Exception as e:
            return ResponseModel(msg_code=ErrorCode.SERVER_ERROR,
                                 msg='服务器内部错误',
                                 check=False).to_response()

        return _book_details(gift.isbn, uid=sender.id, wid=form.tid.data).to_response()
    else:
        return ResponseModel(msg_code=ErrorCode.PARAMETERS_ERROR, msg='参数错误',
                             check=False).to_response()


@api.route('/api/hotSearch')
def hot_search():
    hot_key = ['java', 'vue', 'python', '物联网', 'web']
    return ResponseModel(dataObj=hot_key,
                         check=False).to_response()


def _book_details(isbn, uid, gid=None, wid=None):
    # 取值不能同时为True,在添加gift和wish时已经限制
    has_in_gifts, has_in_wishes = (False, False)

    book = DouBanBook().search_by_isbn(isbn).first
    # 未查找到图书
    if not book:
        return ResponseModel(code=200, msg_code=ErrorCode.BOOK_NOT_FIND,
                             msg='未查找到相应图书', check=False)

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)

    # 判断是在赠送清单还是在心愿清单，或者都不在
    # 判断是否登录，不登录的情况是不在心愿清单也不在赠送清单
    if uid:
        if Gift.query.filter_by(uid=uid, isbn=isbn, launched=False).first():
            has_in_gifts = True
        elif Wish.query.filter_by(uid=uid, isbn=isbn, launched=False).first():
            has_in_wishes = True

    book = BookViewModel().fill(book)

    gift = Gift()
    gift.isbn = isbn
    wish = Wish()
    wish.isbn = isbn

    data = {
        'book': book,
        'gift': {'num': gift.gifts_count,
                 'has_in_gifts': has_in_gifts,
                 'trade_gifts': trade_gifts_model
                 },
        'wish': {"num": wish.wishes_count,
                 'has_in_wishes': has_in_wishes,
                 'trade_wishes': trade_wishes_model},
        'hiddenTrade': True
    }

    # 赠送者，接受者
    sender, recipient = dict(hasSender=False), dict(hasRecipient=False)
    if gid:
        gi = Gift.query.filter_by(id=gid).first()
        # 接收者
        re = User.query.filter_by(id=gi.receiver).first()
        if re:
            recipient = {
                'hasRecipient': True,
                'nickname': re.nickname,
                'updateTime': gi.update_time[:11] if isinstance(gi.update_time, str) else ''
            }
            data['hiddenTrade'] = False
    if wid:
        wi = Wish.query.filter_by(id=wid).first()
        se = User.query.filter_by(id=wi.benefactor).first()
        if se:
            sender = {
                'hasSender': True,
                'nickname': se.nickname,
                'updateTime': wi.update_time[:11] if isinstance(wi.update_time, str) else ''
            }
            data['hiddenTrade'] = False
    data['sender'] = sender
    data['recipient'] = recipient

    book_detail = BookDetail()
    book_detail.fill(data)

    return ResponseModel(dataObj=book_detail, check=False)
