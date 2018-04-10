#!/usr/bin/python
# encoding: utf-8

# @file: base.py
# @time: 2018/4/10 18:02
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm


class ResponseViewModel:

    def __init__(self, code=None, msg=None, data=None):
        self.code = code or 200
        self.msg = msg or '请求成功'
        if data:
            self.data = data
