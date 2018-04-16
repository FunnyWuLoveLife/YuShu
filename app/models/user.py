#!/usr/bin/python
# encoding: utf-8

# @file: user.py
# @time: 2018/4/9 17:02
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from util.common import is_isbn
from .base import BaseModel, db
from .gift import Gift, Wish
from ..spider import DouBanBook


class User(BaseModel, UserMixin):
    __tablename__ = 'tb_user'

    # 平台
    nickname = Column(String(20), nullable=False, comment='用户昵称')
    email = Column(String(50), unique=True, comment='用户邮箱')
    _password = Column('password', String(128), comment='用户密码Hash后的')

    phone_number = Column(String(18), unique=True, comment='用户手机号')
    confirmed = Column(Boolean, default=False, comment='是否验证邮箱地址')
    beans = Column(Float, default=0, comment='鱼豆数量')
    send_counter = Column(Integer, default=0, comment='捐赠数量')
    receive_counter = Column(Integer, default=0, comment='获取数量')

    # 微信
    openId = Column(String(40), unique=True, comment='微信开放平台App唯一id')
    unionId = Column(String(40), nullable=True, comment='微信开放平台用户唯一id')

    avatarUrl = Column(String(1000), nullable=True,
                       comment='用户头像，最后一个数值代表正方形头像大小（有0、46、64、96、132数值可选，'
                               '0代表640*640正方形头像），用户没有头像时该项为空。若用户更换头像，原有头像URL将失效。')
    gender = Column(String(1), comment='用户的性别，值为1时是男性，值为2时是女性，值为0时是未知')
    city = Column(String(10), comment='用户所在城市')
    province = Column(String(10), comment='用户所在省份')
    country = Column(String(10), comment='用户所在国家')
    language = Column(String(10), comment='用户的语言，简体中文为zh_CN')

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    def can_save_to_list(self, isbn):
        """
        判断用户是否已经填本书到赠送清单或者心愿清单，且判断该书是否存在
        :param isbn:<str> 图书的isbn编号
        :return: <bool>: 如果用户能将该书添加至心愿清单或者赠送清单返回True,else False
        """
        if not is_isbn(isbn):
            return False
        dou_book = DouBanBook()
        dou_book.search_by_isbn(isbn)
        if not dou_book.first:
            return False

        # 不允许一个用户同时是赠送者又是索要者
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False

    @property
    def send_count(self):
        return len(db.session.query(Gift).filter(Gift.uid == self.id).all())

    @property
    def receive_count(self):
        return len(Wish.query.filter_by(uid=self.id, launched=True).all())

    @property
    def isRegisterWx(self):
        """
        判断微信账号是否已经注册
        :return:
        """
        return self.query.filter_by(openId=self.openId).first()

    def set_attrs(self, attrs_dict, ignore=list(), ignoreId=True):

        ignore.append('id') if ignoreId else ''

        for k, v in attrs_dict.items():
            if k == 'nickName':
                k = 'nickname'
            if hasattr(self, k) and k not in ignore:
                if isinstance(v, list):
                    v = ','.join(v)
                setattr(self, k, v)  # 动态赋值
        return self

    @classmethod
    def find_user_by_openid(cls, openid):
        return cls.query.filter_by(openId=openid).first()


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
        return '<Sessionkey: openId=%r, sessionKey=%r>' % (self.openid, self.session_key)

    def save(self):
        secKey = db.session.query(Sessionkey).filter(Sessionkey.openid == self.openid).first()
        if secKey is None:
            super(Sessionkey, self).save()
        else:
            secKey.session_key = self.session_key
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
        return self
