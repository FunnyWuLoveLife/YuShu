from flask import render_template, redirect, current_app, flash, url_for, request
from flask_login import login_required, current_user

from . import web
from ..models import Gift, BookModel

__author__ = '七月'


@web.route('/my/gifts')
@login_required
def my_gifts():
    gifts = Gift.find_user_gift(current_user.id)
    return render_template('my_gifts.html', gifts=gifts)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        gift = Gift()
        gift.isbn = isbn
        gift.uid = current_user.id
        gift.bid = BookModel.find_book_by_isbn(isbn).id

        # 鱼豆增加
        current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
        gift.save()
    else:
        flash('这本书已经添加至你的赠送清单或已存在于你的心意清单，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    pass
