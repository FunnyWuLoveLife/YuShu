#!/usr/bin/python
# encoding: utf-8

# @file: book.py
# @time: 2018/4/2 0:48
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from flask import request, render_template, flash

from util.common import is_isbn

from . import web
from ..forms import SearchForm
from ..spider import DouBanBook
from ..view_models import BookCollection, BookDetail


@web.route('/book/search', methods=['Get', 'POST'])
def search():
    """
    图书检索
    :return:
    """
    # 参数校验
    form = SearchForm(request.args)
    books = BookCollection()
    if form.validate():
        q = form.q.data.strip()
        dou_book = DouBanBook()

        if is_isbn(q):
            dou_book.search_by_isbn(q)
        else:
            dou_book.search_by_keyword(q)

        books.fill(dou_book, q)

    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    book = BookDetail()
    book.fill(DouBanBook.search_detail_by_isbn(isbn))
    return render_template('book_detail.html', book=book, wishes=None, gifts=None)
