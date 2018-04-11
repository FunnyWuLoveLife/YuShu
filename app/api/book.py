#!/usr/bin/python
# encoding: utf-8

# @file: book.py
# @time: 2018/4/10 1:10
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from flask import request

from util.common import is_isbn

from . import api
from ..forms import SearchForm, DetailForm
from ..spider import DouBanBook
from ..view_models import BookCollection, ResponseViewModel, ResponseModel, BookDetail


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
    form = DetailForm(request.args)
    if form.validate():
        isbn = form.isbn.data

        book = DouBanBook.search_detail_by_isbn(isbn)

        return ResponseModel(dataObj=BookDetail().fill(book)).to_response()
    else:
        return ResponseModel(dataObj=form.errors).to_response()
