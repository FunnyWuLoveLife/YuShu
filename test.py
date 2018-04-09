#!/usr/bin/python
# encoding: utf-8

# @file: test.py
# @time: 2018/4/7 20:42
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm

from  flask import Flask, current_app

app = Flask(__name__)

ctx = app.app_context()
ctx.push()

a = current_app

pass
