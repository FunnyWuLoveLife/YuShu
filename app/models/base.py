#!/usr/bin/python
# encoding: utf-8

# @file: base.py
# @time: 2018/4/10 2:22
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from datetime import datetime

from sqlalchemy import Column, SmallInteger, Integer

from . import db


class BaseModel(db.Model):
    __abstract__ = True  # 忽略该表让该表不创建数据库表

    id = Column(Integer, primary_key=True, autoincrement=True, comment='自增主键')

    status = Column(SmallInteger, default=1)
    create_time = Column('create_time', Integer, default=datetime.now())

    def set_attrs(self, attrs_dict):
        for k, v in attrs_dict.items():
            if hasattr(self, k) and k != 'id':
                setattr(self, k, v)  # 动态复制
