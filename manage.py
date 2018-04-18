#!/usr/bin/python
# encoding: utf-8

# @file: manage.py
# @time: 2018/4/18 18:26
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from app import create_app
from flask_script import Manager

app = create_app()
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
