#!/usr/bin/python
# encoding: utf-8

# @file: User.py
# @time: 2018/4/9 17:02
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from uuid import uuid4

from sqlalchemy import Column, INTEGER, String

from . import db
from util.httpHelper import HTTP


class User(db.Model):
    __tablename__ = 'tb_user'

    id = Column(INTEGER, primary_key=True, autoincrement=True, comment='自增主键')
    openId = Column(String(20), unique=True, comment='微信开放平台App唯一id')
    unionId = Column(String(20), nullable=True, comment='微信开放平台用户唯一id')

    nickName = Column(String(20), nullable=False, comment='用户昵称')
    avatarUrl = Column(String(50), nullable=True,
                       comment='用户头像，最后一个数值代表正方形头像大小（有0、46、64、96、132数值可选，'
                               '0代表640*640正方形头像），用户没有头像时该项为空。若用户更换头像，原有头像URL将失效。')
    gender = Column(String(1), comment='用户的性别，值为1时是男性，值为2时是女性，值为0时是未知')
    city = Column(String(10), comment='用户所在城市')
    province = Column(String(10), comment='用户所在省份')
    country = Column(String(10), comment='用户所在国家')
    language = Column(String(10), comment='用户的语言，简体中文为zh_CN')


class Sessionkey(db.Model):
    __tablename__ = 'tb_session'

    token = Column(String(40), primary_key=True, comment='用户Token')
    openId = Column(String(30), primary_key=True, comment='用户唯一标识')
    sessionKey = Column(String(30), unique=True, nullable=False, comment='会话密钥')

    @classmethod
    def save(cls, session_key, openid):
        token = str(uuid4())
        key = db.session.query(Sessionkey).filter(Sessionkey.openId is openid).first()
        if key:
            print(key)
            # db.session.update(Sessionkey.sessionKey == session_key)
            pass
        else:
            key = Sessionkey()
            key.sessionKey = session_key
            key.token = token
            key.openId = openid
            db.session.add(key)
            db.session.commit()

    @classmethod
    def get_session_key_by_openid(cls, openid):
        key = db.session.query(Sessionkey.sessionKey).filter(Sessionkey.openId is openid).first()
        return key

    def __repr__(self):
        return '<Sessionkey: openId=%r, sessionKey=%r>' % (self.openId, self.sessionKey)

    @classmethod
    def getSessionKeyFromWx(cls, code):
        wx_url = 'https://api.weixin.qq.com/sns/jscode2session?appid={}' \
                 '&secret={}&js_code={}&grant_type=authorization_code'.format(app.config['APPID'],
                                                                              app.config['SECRET'], code)
        with app.app_context():
            data = HTTP.get(wx_url)
            if data != '':
                cls.save(data.get('session_key'), data.get('openid'))
                return True
        return False
