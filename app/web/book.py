#!/usr/bin/python
# encoding: utf-8

# @file: book.py
# @time: 2018/4/2 0:48
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from flask import request, render_template, flash
from flask_login import current_user
from util.common import is_isbn

from . import web
from ..forms import SearchForm
from ..models import Gift, Wish
from ..spider import DouBanBook
from ..view_models import BookCollection, BookDetail, TradeInfo


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
            dou_book.search_by_keyword(q, page=form.page.data)
        books.fill(dou_book, q)

    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    # 取值不能同时为True,在添加gift和wish时已经限制
    has_in_gifts, has_in_wishes = (False, False)

    # 取书籍详情信息
    book = BookDetail()
    book.fill(DouBanBook().search_by_isbn(isbn).first)

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)

    # 判断是在赠送清单还是在心愿清单，或者都不在
    # 判断是否登录，不登录的情况是不在心愿清单也不在赠送清单
    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_gifts = True
        elif Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_wishes = True

    return render_template('book_detail.html', book=book,
                           wishes=trade_wishes_model,
                           gifts=trade_gifts_model,
                           has_in_gifts=has_in_gifts,
                           has_in_wishes=has_in_wishes)
