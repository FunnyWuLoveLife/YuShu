#!/usr/bin/python
# encoding: utf-8

# @file: common.py
# @time: 2018/4/1 23:51
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
import requests
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

from flask import current_app as app


def is_isbn(word):
    """
    判断是否是isbn
    :param word: 需要判断的字符串
    :return:
    """

    if len(word) == 13 and word.isdigit():
        return True

    short_key = word.replace('-', '')
    # 多条件判断原则
    # 大概率的过滤掉的放在前面，后面判断不会执行
    if '-' in word and len(short_key) == 10 and short_key.isdigit():
        return True
    return False


def get_openid_and_session_key(appId, secret, code):
    _url = "https://api.weixin.qq.com/sns/jscode2session?" \
           "appid={}&secret={}&js_code={}&" \
           "grant_type=authorization_code".format(appId, secret, code)
    r = requests.get(_url)
    if r.status_code:
        return r.json()
    else:
        return None


class Token:
    def __init__(self, uid):
        self.uid = uid
        pass

    def generate_auth_token(self, expiration=3600):
        s = Serializer(app.config['SECRET'], expires_in=expiration)
        return s.dumps({'uid': self.uid}).decode('UTF-8')

    def verify_auth_token(self, token):
        s = Serializer(app.config['SECRET'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return False  # valid token, but expired
        except BadSignature:
            return False  # invalid token
        return data['uid'] == self.uid
