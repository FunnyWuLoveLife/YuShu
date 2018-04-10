#!/usr/bin/python
# encoding: utf-8

# @file: book.py
# @time: 2018/4/10 0:46
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm


class BookViewModel:
    def __init__(self, book):
        self.title = book['title']
        self.author = book['author']
        self.publisher = book['publisher'] or ''
        self.image = book['image']
        self.summary = book['summary'] or ''
        self.price = book['price'] or '未知'


class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, dou_book, keyword):
        self.total = dou_book.total
        self.books = [BookViewModel(book) for book in dou_book.books]
        self.keyword = keyword
        return self
