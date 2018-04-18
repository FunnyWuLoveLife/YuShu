#!/usr/bin/python
# encoding: utf-8

# @file: test.py
# @time: 2018/4/14 18:25
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from app.models.gift import Gift
from app import create_app
from app.spider.book import JdSpider

# app = create_app()
if __name__ == '__main__':
    JdSpider().search('9787560639192')
