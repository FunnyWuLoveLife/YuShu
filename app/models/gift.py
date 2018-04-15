#!/usr/bin/python
# encoding: utf-8

# @file: gift.py
# @time: 2018/4/10 2:27
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, and_, desc
from sqlalchemy.orm import relationship
from flask import current_app

from .base import BaseModel, db
from .book import BookModel


class Gift(BaseModel):
    __tablename__ = 'tb_gitf'

    user = relationship('User')
    uid = Column(Integer, ForeignKey('tb_user.id'), nullable=False)

    # book = relationship('Book')
    bid = Column(Integer, ForeignKey('tb_book.id'), nullable=False, comment='数据id号')

    isbn = Column(String(15), nullable=False, comment='唯一isbn号')

    launched = Column(Boolean, default=False, comment='图书是否已经送出')

    @property
    def book(self):
        return BookModel.query.filter_by(isbn=self.isbn).first()

    @classmethod
    def find_user_gift(cls, uid):
        return cls.query.filter_by(uid=uid).order_by(desc(Gift.create_time)).all()

    @classmethod
    def recent(cls):
        recent_gifs = Gift.query.filter_by(launched=False).group_by(
            Gift.isbn).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).all()
        return recent_gifs

    # TODO 这种方式存在效率问题，前期不用考虑
    @property
    def wishes_count(self):
        return len(Wish.query.filter_by(isbn=self.isbn, launched=False).all())


class Donate(BaseModel):
    __tablename__ = 'tb_donate'

    user = relationship('User')
    uid = Column(Integer, ForeignKey('tb_user.id'), comment='用户id')

    isbn = Column(String(15), nullable=False, comment='唯一isbn号')
    launched = Column(Boolean, default=False, comment='礼物是否送出')

    def __init__(self, uid, isbn):
        self.uid = uid
        self.isbn = isbn
        super(Donate, self).__init__()

    @classmethod
    def query_num(cls, isbn):
        num = db.session.query(Donate).filter(and_(Donate.launched is False, Donate.isbn == isbn)).count()
        return num


class Wish(BaseModel):
    __tablename__ = 'tb_wish'

    user = relationship('User')
    uid = Column(Integer, ForeignKey('tb_user.id'), comment='用户id')

    # book = relationship('Book')
    bid = Column(Integer, ForeignKey('tb_book.id'), comment='数据id号')

    isbn = Column(String(15), nullable=False, comment='唯一isbn号')
    launched = Column(Boolean, default=False, comment='礼物是否送出')

    def __init__(self, uid=None, isbn=None):
        self.uid = uid
        self.isbn = isbn
        super(Wish, self).__init__()

    @classmethod
    def query_num(cls, isbn):
        num = db.session.query(Wish).filter(and_(Wish.status == 1, Wish.isbn == isbn)).count()
        return num

    @property
    def book(self):
        return BookModel.query.filter_by(isbn=self.isbn).first()

    @classmethod
    def find_user_wishes(cls, uid):
        return cls.query.filter_by(uid=uid).order_by(desc(Wish.create_time)).all()

    @property
    def gifts_count(self):
        return len(Gift.query.filter_by(isbn=self.isbn, launched=False).all())
