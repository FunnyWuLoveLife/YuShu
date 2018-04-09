#!/usr/bin/python
# encoding: utf-8

# @file: __init__.py.py
# @time: 2018/4/2 0:49
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from flask import Flask

from .models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')

    # 初始化蓝图
    register_buleprint(app)

    # 绑定数据库
    db.init_app(app)

    # 下面两种方法都可以创建数据库
    # with app.app_context():
    #     db.create_all()
    db.create_all(app=app)

    return app


def register_buleprint(app):
    from .web import web
    from .api import api
    app.register_blueprint(web)
    app.register_blueprint(api)
