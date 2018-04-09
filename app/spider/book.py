#!/usr/bin/python
# encoding: utf-8

# @file: book.py
# @time: 2018/4/10 1:17
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from flask import current_app as app

from util.httpHelper import HTTP


class DouBanBook:
    _isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    _keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        result = HTTP.get(self._isbn_url.format(isbn))
        self._fill_single(result)
        return self

    def _fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def _fill_collection(self, data):
        self.total = data['total']
        self.books = data['books']

    def search_by_keyword(self, keyword, page=1):
        url = self._keyword_url.format(keyword,
                                       app.config['PRE_PAGE'],
                                       self.calculate_start(page))
        result = HTTP.get(url)
        self._fill_collection(result)
        return self

    @classmethod
    def calculate_start(cls, page):
        return (page - 1) * app.config['PRE_PAGE']
