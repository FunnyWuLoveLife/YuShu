#!/usr/bin/python
# encoding: utf-8

# @file: test.py
# @time: 2018/4/15 1:44
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from app import create_app
from app.models import Gift

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        gift = Gift.query.filter_by(uid=1).first()
        # user = gift.user
        pass
