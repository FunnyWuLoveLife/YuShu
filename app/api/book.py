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
from ..forms import SearchForm, IsbnForm
from ..spider import DouBanBook
from ..models import Wish, Gift, BookModel, User
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
            dou_book.search_by_keyword(q)

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

    form = IsbnForm(request.args)
    if form.validate():

        # 取值不能同时为True,在添加gift和wish时已经限制
        has_in_gifts, has_in_wishes = (False, False)

        isbn = form.isbn.data
        book = DouBanBook().search_by_isbn(isbn).first
        # 未查找到图书
        if not book:
            return ResponseModel(code=200, msg_code=ErrorCode.BOOK_NOT_FIND,
                                 msg='未查找到相应图书', check=False).to_response()

        trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
        trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

        trade_gifts_model = TradeInfo(trade_gifts)
        trade_wishes_model = TradeInfo(trade_wishes)

        # 判断是在赠送清单还是在心愿清单，或者都不在
        # 判断是否登录，不登录的情况是不在心愿清单也不在赠送清单
        if user:
            if Gift.query.filter_by(uid=user.id, isbn=isbn, launched=False).first():
                has_in_gifts = True
            elif Wish.query.filter_by(uid=user.id, isbn=isbn, launched=False).first():
                has_in_wishes = True

        book = BookViewModel().fill(book)

        gift = Gift()
        gift.isbn = isbn
        wish = Wish()
        wish.isbn = isbn

        book_detail = BookDetail()
        book_detail.fill({
            'book': book,
            'gift': {'num': gift.gifts_count,
                     'has_in_gifts': has_in_gifts,
                     'trade_gifts': trade_gifts_model
                     },
            'wish': {"num": wish.wishes_count,
                     'has_in_wishes': has_in_wishes,
                     'trade_wishes': trade_wishes_model}
        })

        return ResponseModel(dataObj=book_detail, check=False).to_response()
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
