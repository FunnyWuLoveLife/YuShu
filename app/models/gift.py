#!/usr/bin/python
# encoding: utf-8

# @file: gift.py
# @time: 2018/4/10 2:27
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, and_
from sqlalchemy.orm import relationship

from . import BaseModel, db


class Gift(BaseModel):
    __tablename__ = 'tb_gitf'

    uid = Column(Integer, ForeignKey('tb_user.id'))

    isbn = Column(String(15), nullable=False, comment='唯一isbn号')

    launched = Column(Boolean, comment='图书是否已经送出')


class Donate(BaseModel):
    __tablename__ = 'tb_donate'

    user = relationship('User')
    uid = Column(Integer, ForeignKey('tb_user.id'), comment='用户id')

    isbn = Column(String(15), nullable=False, comment='唯一isbn号')
    launched = Column(Boolean, default=False, comment='礼物是否送出')

    def __init__(self, oid, isbn):
        self.oid = oid
        self.isbn = isbn

    @classmethod
    def query_num(cls, isbn):
        num = db.session.query(Donate).filter(and_(Donate.launched is False, Donate.isbn == isbn)).count()
        return num


class Wish(BaseModel):
    __tablename__ = 'tb_wish'

    user = relationship('User')
    uid = Column(Integer, ForeignKey('tb_user.id'), comment='用户id')

    # TODO 暂时没保存书籍信息
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('tb_book.id'), comment='数据id号')

    isbn = Column(String(15), nullable=False, comment='唯一isbn号')

    def __init__(self, oid, isbn):
        self.oid = oid
        self.isbn = isbn

    @classmethod
    def query_num(cls, isbn):
        num = db.session.query(Wish).filter(and_(Wish.status == 1, Wish.isbn == isbn)).count()
        return num
