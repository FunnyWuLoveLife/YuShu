#!/usr/bin/python
# encoding: utf-8

# @file: user.py
# @time: 2018/4/9 17:15
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from flask import request, current_app as app

from . import api
from ..view_models import ResponseModel, TokenViewModel
from util.common import get_openid_and_session_key, Token


@api.route('/api/user/info', methods=['POST'])
def user_info():
    print(request.json)
    return 'user.info'


@api.route('/api/user/token/onLogin', methods=['POST'])
def on_login():
    code = request.json.get('code')
    if code is None:
        return ResponseModel({}).to_response()
    res = get_openid_and_session_key(app.config['APPID'], app.config['SECRET'], code)
    if res:
        uid = 1
        # TODO 待完善,token接口不完善
        token = Token(uid).generate_auth_token()
        return ResponseModel(TokenViewModel(token)).to_response()
    else:
        return ResponseModel(code=403, msg_code=4030,
                             msg='微信登录接口错误', check=False).to_response()


@api.route('/api/user/token/verify', methods=['POST'])
def verify():
    token = request.json.get('token')
    print(token)
    # TODO token接口问题
    return 'yes'
