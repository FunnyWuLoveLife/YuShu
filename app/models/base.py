#!/usr/bin/python
# encoding: utf-8

# @file: base.py
# @time: 2018/4/10 2:22
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from datetime import datetime

from sqlalchemy import Column, SmallInteger, Integer, DateTime

from . import db


class BaseModel(db.Model):
    __abstract__ = True  # 忽略该表让该表不创建数据库表

    id = Column(Integer, primary_key=True, autoincrement=True, comment='自增主键')

    status = Column(SmallInteger, default=1, comment='软删除状态，1表示未删除，0表示删除')
    create_time = Column('create_time', Integer, comment='创建时间')
    update_time = Column(Integer, onupdate=int(datetime.now().timestamp()), comment='数据更新时间')

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def set_attrs(self, attrs_dict, ignore=list()):
        ignore.append('id')
        for k, v in attrs_dict.items():
            if hasattr(self, k) and k not in ignore:
                if isinstance(v, list):
                    v = ','.join(v)
                setattr(self, k, v)  # 动态赋值
        return self

    def save(self):
        with db.auto_commit():
            db.session.add(self)
        return self

    @classmethod
    def update(cls):
        # db.session.commit()
        pass
