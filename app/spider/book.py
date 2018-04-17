#!/usr/bin/python
# encoding: utf-8

# @file: book.py
# @time: 2018/4/10 1:17
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from flask import current_app as app

from util.httpHelper import HTTP

from ..models.book import BookModel


class DouBanBook:
    # _isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    _isbn_url = 'https://api.douban.com/v2/book/isbn/{}'
    # _keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'
    _keyword_url = 'https://api.douban.com/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        book = BookModel.find_book_by_isbn(isbn)
        if book:
            self._fill_single(book)
        else:
            result = HTTP.get(self._isbn_url.format(isbn))
            BookModel().set_attrs_from_douban(result).save()
            if result.get('isbn13'):
                result['isbn'] = result.get('isbn13')
            elif result.get('isbn10'):
                result['isbn'] = result.get('isbn10')
            self._fill_single(result)
        return self

    def _fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

        return self

    def _fill_collection(self, data):
        self.total = data['total']
        self.books = data['books']
        return self

    def search_by_keyword(self, keyword, page=1):
        url = self._keyword_url.format(keyword,
                                       app.config['PRE_PAGE'],
                                       self.calculate_start(page))
        result = HTTP.get(url)
        if result:
            res = []
            for book in result.get('books', list()):
                if book.get('isbn13'):
                    book['isbn'] = book.get('isbn13')
                    BookModel().set_attrs_from_douban(book).save()
                    res.append(book)
                elif book.get('isbn10'):
                    book['isbn'] = book.get('isbn13')
                    BookModel().set_attrs_from_douban(book).save()
                    res.append(book)
            result['books'] = res
        self._fill_collection(result)
        return self

    @classmethod
    def calculate_start(cls, page):
        return (page - 1) * app.config['PRE_PAGE']

    @property
    def first(self):
        if self.total >= 1:
            return self.books[0]
        else:
            return None
