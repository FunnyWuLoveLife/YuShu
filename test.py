#!/usr/bin/python
# encoding: utf-8

# @file: test.py
# @time: 2018/4/14 18:25
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from app.models.gift import Gift
from app import create_app

app = create_app()
if __name__ == '__main__':
    with app.app_context():
        a = Gift.query.filter_by(uid=1).first()
        pass
