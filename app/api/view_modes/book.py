#!/usr/bin/python
# encoding: utf-8

# @file: book.py
# @time: 2018/4/10 0:46
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm


class BookViewModel:
    def __init__(self, book=None):
        self.title = ''
        self.author = '未知'
        self.publisher = '未知'
        self.pubdate = ''
        self.summary = '未知'
        self.price = '未知'
        self.image = ''
        self.isbn = ''
        self.pages = 0
        self.binding = '未知'
        if book:
            self.fill(book)

    def fill(self, book, ignore=list()):
        if isinstance(book, dict):
            self.title = book['title']
            self.author = book['author']
            self.publisher = book['publisher'] or ''
            self.summary = ' ' + book['summary'].replace(r'.', '') if book['summary'] else ''
            self.price = '￥' + book.get('price') if book.get('price') else '未知'
            self.image = book['image']
            self.pubdate = book['pubdate']
            self.isbn = book['isbn']
            self.pages = book['pages']
            self.binding = book['binding']
        else:
            for k, v in book.__dict__.items():
                if hasattr(self, k) and k not in ignore:
                    setattr(self, k, v)  # 动态赋值
        return self


class BookDetail:
    def __init__(self, book=None, gift=None, wish=None, recipient=None, sender=None, hiddenTrade=None):
        self.book = book
        self.gift = gift
        self.wish = wish
        self.recipient = recipient
        self.sender = sender
        self.hiddenTrade = True

    def fill(self, attrs_dict):
        if isinstance(attrs_dict, dict):
            for k, v in attrs_dict.items():
                if hasattr(self, k):
                    setattr(self, k, v)  # 动态赋值

        return self


class BookTradeInfo:
    def __init__(self, tid, book):
        self.tid = tid
        self.book = book


class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, dou_book, keyword):
        self.total = dou_book.total
        self.books = [BookViewModel().fill(book) for book in dou_book.books]
        self.keyword = keyword
        return self

    def fill_by_book_list(self, b_list):
        self.total = len(b_list)
        self.books = [BookViewModel().fill(book) for book in b_list]
        del self.keyword
        return self

    def fill_gift_or_wish(self, b_list, t_list):
        self.total = len(b_list)
        self.books = [BookTradeInfo(tid, BookViewModel(book)) for book, tid in zip(b_list, t_list)]
        del self.keyword
        return self
