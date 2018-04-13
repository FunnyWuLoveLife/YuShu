#!/usr/bin/python
# encoding: utf-8

# @file: base.py
# @time: 2018/4/10 2:22
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from datetime import datetime

from sqlalchemy import Column, SmallInteger, Integer, DateTime
from sqlalchemy.exc import IntegrityError

from . import db


class BaseModel(db.Model):
    __abstract__ = True  # 忽略该表让该表不创建数据库表

    id = Column(Integer, primary_key=True, autoincrement=True, comment='自增主键')

    status = Column(SmallInteger, default=1, comment='软删除状态，1表示未删除，0表示删除')
    create_time = Column(DateTime, default=datetime.now(), comment='创建时间')
    update_time = Column(DateTime, onupdate=datetime.now(), comment='数据更新时间')

    def set_attrs(self, attrs_dict, ignore=list()):
        ignore.append('id')
        for k, v in attrs_dict.items():
            if hasattr(self, k) and k not in ignore:
                setattr(self, k, v)  # 动态赋值
        return self

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            self.update()

    @classmethod
    def update(cls):
        db.session.commit()
