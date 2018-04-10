#!/usr/bin/python
# encoding: utf-8

# @file: gift.py
# @time: 2018/4/10 2:27
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from . import BaseModel


class Gift(BaseModel):
    __tablename__ = 'tb_gitf'

    uid = Column(Integer, ForeignKey('tb_user.id'))

    isbn = Column(String(15), nullable=False, comment='唯一isbn号')

    launched = Column(Boolean, comment='图书是否已经送出')
