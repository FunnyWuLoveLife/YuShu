#!/usr/bin/python
# encoding: utf-8

# @file: index.py
# @time: 2018/4/3 23:14
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm

from . import web


@web.route('/')
def index():
    return 'Hello Flask'
