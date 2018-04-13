#!/usr/bin/python
# encoding: utf-8

# @file: User.py
# @time: 2018/4/9 17:02
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from uuid import uuid4

from flask import current_app as app
from sqlalchemy import Column, Integer, String, ForeignKey

from . import BaseModel, db
from util.httpHelper import HTTP


class User(BaseModel):
    __tablename__ = 'tb_user'

    openId = Column(String(40), unique=True, comment='微信开放平台App唯一id')
    unionId = Column(String(40), nullable=True, comment='微信开放平台用户唯一id')

    nickName = Column(String(20), nullable=False, comment='用户昵称')
    avatarUrl = Column(String(50), nullable=True,
                       comment='用户头像，最后一个数值代表正方形头像大小（有0、46、64、96、132数值可选，'
                               '0代表640*640正方形头像），用户没有头像时该项为空。若用户更换头像，原有头像URL将失效。')
    gender = Column(String(1), comment='用户的性别，值为1时是男性，值为2时是女性，值为0时是未知')
    city = Column(String(10), comment='用户所在城市')
    province = Column(String(10), comment='用户所在省份')
    country = Column(String(10), comment='用户所在国家')
    language = Column(String(10), comment='用户的语言，简体中文为zh_CN')


class Sessionkey(BaseModel):
    __tablename__ = 'tb_session'

    openid = Column(String(40), primary_key=True, comment='用户唯一标识')
    session_key = Column(String(40), unique=True, nullable=False, comment='会话密钥')

    @classmethod
    def get_session_key_by_openid(cls, openid):
        secKey = db.session.query(Sessionkey).filter(Sessionkey.openid == openid).first()
        key = secKey.session_key if secKey else None
        return key

    def __repr__(self):
        return '<Sessionkey: openId=%r, sessionKey=%r>' % (self.openId, self.sessionKey)

    def save(self):
        secKey = db.session.query(Sessionkey).filter(Sessionkey.openid == self.openid).first()
        if secKey is None:
            super.save()
        else:
            secKey.session_key = self.session_key
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
        return self
