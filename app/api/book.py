#!/usr/bin/python
# encoding: utf-8

# @file: book.py
# @time: 2018/4/10 1:10
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from flask import request

from util.common import is_isbn, Token

from . import api
from .view_modes import BookCollection, ResponseModel, BookViewModel, BookDetail
from ..forms import SearchForm, IsbnForm
from ..spider import DouBanBook
from ..models import Donate, Wish, Gift
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
    form = IsbnForm(request.args)
    if form.validate():
        isbn = form.isbn.data
        book = DouBanBook().search_by_isbn(isbn).first
        # 未查找到图书
        if not book:
            return ResponseModel(code=200, msg_code=ErrorCode.BOOK_NOT_FIND,
                                 msg='未查找到相应图书', check=False).to_response()

        book = BookViewModel().fill(book)
        gift_num = Donate.query_num(isbn)
        wish_num = Wish.query_num(isbn)
        book_detail = BookDetail(book, {'num': gift_num}, {"num": wish_num})
        return ResponseModel(dataObj=book_detail).to_response()
    else:
        return ResponseModel(msg_code=ErrorCode.ISBN_CODE_ERROR,
                             msg='ISBN编号错误', check=False
                             ).to_response()


@api.route('/api/book/donate', methods=['GET'])
def donate():
    token = request.headers.get('token')
    form = DetailForm(request.args)
    if token is None:
        return ResponseModel(code=401, msg_code=4010, msg='token是必须参数',
                             check=False).to_response()

    openId = Token.get_openid(token)
    if openId is None:
        return ResponseModel(code=401, msg_code=4010, msg='token无效请登录',
                             check=False).to_response()

    if form.validate():
        isbn = form.isbn.data
        don = Donate(openId, isbn)
        don.save()
        num = don.query_num(isbn)
        return ResponseModel({"num": num}, check=False).to_response()
    else:
        return ResponseModel(form.errors, check=False).to_response()


@api.route('/api/book/wish')
def addWish():
    token = request.headers.get('token')
    form = IsbnForm(request.args)
    if token is None:
        return ResponseModel(code=401, msg_code=4010, msg='token是必须参数',
                             check=False).to_response()

    openId = Token.get_openid(token)
    if openId is None:
        return ResponseModel(code=401, msg_code=4010, msg='token无效请登录',
                             check=False).to_response()

    if form.validate():
        isbn = form.isbn.data
        wis = Wish(openId, isbn)
        wis.save()
        num = wis.query_num(isbn)
        return ResponseModel({"num": num}, check=False).to_response()
    else:
        return ResponseModel(form.errors, check=False).to_response()


@api.route('/api/book/recent')
def recent_gift():
    recent_gifts = Gift.recent()
    recent_books = [BookViewModel(gift.book) for gift in recent_gifts]
    return ResponseModel(dataObj=recent_books).to_response()
