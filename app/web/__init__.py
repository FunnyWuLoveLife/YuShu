#!/usr/bin/python
# encoding: utf-8

# @file: __init__.py.py
# @time: 2018/4/2 0:49
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from flask import Blueprint

web = Blueprint('web', __name__)

from .book import search
from .index import index
