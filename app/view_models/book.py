#!/usr/bin/python
# encoding: utf-8

# @file: book.py
# @time: 2018/4/10 0:46
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from ..models import BookModel


class BookViewModel:
    def __init__(self, book):
        self.title = book['title']
        self.image = book['image']
        self.isbn = book['isbn']


class BookDetail:
    def __init__(self):
        self.title = ''
        self.author = '未知'
        self.publisher = '未知'
        self.summary = '未知'
        self.price = '未知'
        self.image = ''
        self.isbn = ''
        self.pages = 0
        self.binding = '未知'
        self.pubdate = '未知'

    def fill(self, book):
        if isinstance(book, dict):
            self._fill(book)
        elif isinstance(book, BookModel):
            self._fill(book.__dict__)
            pass
        return self

    def _fill(self, book):
        self.title = book['title']
        self.author = ','.join(book['author'])
        self.publisher = book['publisher'] or ''
        self.summary = ' ' + book['summary'].replace(r'.', '') if book['summary'] else ''
        self.price = '￥' + book['price'] or '未知'
        self.image = book['image']
        self.isbn = book['isbn']
        self.pages = book['pages']
        self.binding = book['binding']
        self.pubdate = book['pubdate']


class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, dou_book, keyword):
        self.total = dou_book.total
        self.books = [BookDetail().fill(book) for book in dou_book.books]
        self.keyword = keyword
        return self
