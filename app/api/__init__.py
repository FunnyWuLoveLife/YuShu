#!/usr/bin/python
# encoding: utf-8

# @file: __init__.py.py
# @time: 2018/4/4 0:21
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from flask import Blueprint
from flask_restful import Api

api = Blueprint('api', __name__)
# api = Api()

from .book import *
from .user import *
