#!/usr/bin/python
# encoding: utf-8

# @file: __init__.py.py
# @time: 2018/4/9 17:01
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            # TODO 异常处理需要完善
            # print(e)
            # raise e


db = SQLAlchemy()

from .base import BaseModel

from .user import User, Sessionkey
from .book import BookModel
from .gift import Gift, Donate, Wish
from .hot import HotSearch
