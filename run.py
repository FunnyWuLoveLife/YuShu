#!/usr/bin/python
# encoding: utf-8

# @file: run.py
# @time: 2018/4/1 18:21
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
