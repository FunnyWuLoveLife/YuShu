#!/usr/bin/python
# encoding: utf-8

# @file: hot.py
# @time: 2018/4/11 21:02
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm

from sqlalchemy import Column, String, Integer

from . import BaseModel


class HotSearch(BaseModel):
    __tablename__ = 'tb_hotSearch'

    keyword = Column(String(30), nullable=False, unique=True, comment='搜索的关键字')
    count = Column(Integer, nullable=False, default=0, comment='搜索次数')
