#!/usr/bin/python
# encoding: utf-8

# @file: book.py
# @time: 2018/4/9 17:02
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from sqlalchemy import Column, INTEGER, String, Text

from .base import BaseModel, db


class BookModel(BaseModel):
    __tablename__ = 'tb_book'

    title = Column(String(50), nullable=False, comment='数据的名称')
    author = Column(String(100), default='未知', comment='作者')
    binding = Column(String(20), comment='装帧')
    category = Column(String(20), comment='分类')
    image = Column(String(50), comment='图片地址')
    isbn = Column(String(15), nullable=False, unique=True, comment='唯一isbn号')
    pages = Column(INTEGER, comment='页数')
    price = Column(String(20), comment='价格')
    pubdate = Column(String(20), comment='出版年')
    publisher = Column(String(50), comment='出版社')
    summary = Column(Text, comment='内容简介')

    @classmethod
    def find_book_by_isbn(cls, isbn):
        book = db.session.query(BookModel).filter(BookModel.isbn == isbn).first()
        return book
