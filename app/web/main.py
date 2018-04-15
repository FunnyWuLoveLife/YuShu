from flask import render_template
from flask_login import current_user, login_required
from . import web
from ..models import Gift
from ..view_models import UserViewModel

__author__ = '七月'


@web.route('/')
def index():
    recent_gifts = Gift.recent()
    recent_books = [gift.book for gift in recent_gifts]
    return render_template('index.html', recent=recent_books)


@web.route('/personal')
@login_required
def personal_center():
    userView = UserViewModel(current_user)
    return render_template('personal.html', user=userView)
