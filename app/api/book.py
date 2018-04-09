#!/usr/bin/python
# encoding: utf-8

# @file: book.py
# @time: 2018/4/10 1:10
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
import json

from flask import jsonify, request

from util.common import is_isbn

from . import api
from ..forms import SearchForm
from ..spider import DouBanBook
from ..view_models import BookCollection


@api.route('/api/book/search')
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
        return json.dumps(books, default=lambda o: o.__dict__), 200, {'content-type': 'application/json', }
    else:
        return jsonify(form.errors)
