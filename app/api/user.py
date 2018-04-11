#!/usr/bin/python
# encoding: utf-8

# @file: user.py
# @time: 2018/4/9 17:15
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from flask import request

from . import api


def user_info():
    pass


@api.route('/api/user/onLogin', methods=['POST'])
def on_login():
    print(request.json)
    return 'yes'
