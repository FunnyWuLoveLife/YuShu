#!/usr/bin/python
# encoding: utf-8

# @file: services.py
# @time: 2018/4/7 16:26
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm

from flask import current_app as app

from util.httpHelper import HTTP


class Book:
    _isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    _keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    @classmethod
    def search_by_isbn(cls, isbn):
        result = HTTP.get(cls._isbn_url.format(isbn))
        return result

    @classmethod
    def search_by_keyword(cls, keyword, page=1):
        url = cls._keyword_url.format(keyword,
                                      app.config['PRE_PAGE'],
                                      Book.calculate_start(page))
        result = HTTP.get(url)
        return result

    @staticmethod
    def calculate_start(page):
        return (page - 1) * app.config['PRE_PAGE']
