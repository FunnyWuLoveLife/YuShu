#!/usr/bin/python
# encoding: utf-8

# @file: __init__.py.py
# @time: 2018/4/9 17:01
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from .base import BaseModel

from .user import User, Sessionkey
from .book import BookModel
from .gift import Gift
