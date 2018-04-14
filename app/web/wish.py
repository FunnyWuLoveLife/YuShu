from flask import render_template, flash, redirect, url_for, current_app
from flask_login import current_user

from ..models import Wish
from . import web, BookModel

__author__ = '七月'


@web.route('/my/wish')
def my_wish():
    return render_template('my_wish.html', wishes=[])


@web.route('/wish/book/<isbn>')
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        wish = Wish(current_user.id, isbn)
        # wish.bid = BookModel.find_book_by_isbn(isbn).id

        if current_user.beans < current_app.config['BEANS_WISH_ONE_BOOK']:
            flash('你的鱼豆余额不足')
            return redirect(url_for('web.book_detail', isbn=isbn))

        current_user.beans -= current_app.config['BEANS_WISH_ONE_BOOK']
        wish.save()
        flash('已成功添加至心愿清单')
    else:
        flash('这本书已存在于心意清单或已经添加至你的你的赠送清单，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
def satisfy_wish(wid):
    pass


@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    pass
