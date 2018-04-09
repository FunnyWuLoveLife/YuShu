#!/usr/bin/python
# encoding: utf-8

# @file: book.py
# @time: 2018/4/2 0:48
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm

from flask import jsonify, request

from util.common import is_isbn

from . import web
from ..services import Book
from ..forms import SearchForm


@web.route('/book/search')
def search():
    """
    图书检索
    :return:
    """
    # 参数校验
    form = SearchForm(request.args)
    if form.validate():
        q = form.q.data.strip()
        if is_isbn(q):
            res = Book.search_by_isbn(q)
        else:
            res = Book.search_by_keyword(q)
        return jsonify(res)
    else:
        return jsonify(form.errors)
