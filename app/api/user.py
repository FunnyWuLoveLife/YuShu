#!/usr/bin/python
# encoding: utf-8

# @file: user.py
# @time: 2018/4/9 17:15
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from flask import request, current_app as app

from . import api
from .view_modes import ResponseModel, TokenViewModel, UserViewModel
from util.common import get_openid_and_session_key, Token
from util.WXBizDataCrypt import WXBizDataCrypt
from ..models import User, Sessionkey
from ..error import ErrorCode


@api.route('/api/user/info', methods=['POST'])
def user_info():
    data = request.json
    encryptedData = data.get('encryptedData')
    iv = data.get('iv')
    token = request.headers['token']
    if token is None:
        ResponseModel(code=200, msg_code=4030,
                      msg='token失效', check=False).to_response()

    oid = Token.get_openid(token)
    if oid is None:
        ResponseModel(code=200, msg_code=4030,
                      msg='openid不存在，无session_key', check=False).to_response()

    secKey = Sessionkey.get_session_key_by_openid(oid)
    if secKey is None:
        app.logger.info('用户秘钥不存在', oid)
        return ResponseModel(code=200,
                             msg_code=ErrorCode.IS_REGISTER_WX,
                             msg='用户秘钥不存在',
                             check=False).to_response()

    wx = WXBizDataCrypt(app.config['APPID'], secKey)
    try:
        decryptedData = wx.decrypt(encryptedData, iv)
    except Exception as e:
        app.logger.error(e)
        return ResponseModel(code=200, msg_code=4030,
                             msg='解码错误', check=False).to_response()
    user = User().set_attrs(decryptedData)
    wxU = user.isRegisterWx
    if wxU:
        # 如果用户已经存在则返回历史数据给用户
        user = wxU
    uv = UserViewModel(user)
    user.save()
    return ResponseModel(uv,
                         msg='保存用户信息成功',
                         check=False).to_response()


@api.route('/api/user/token/onLogin', methods=['POST'])
def on_login():
    code = request.json.get('code')
    if code is None:
        return ResponseModel({}, msg_code=4030, msg='code是必须参数').to_response()

    res = get_openid_and_session_key(app.config['APPID'], app.config['SECRET'], code)
    if res:
        openId = res.get('openid')
        if openId is None:
            return ResponseModel(code=403, msg_code=4030,
                                 msg='微信登录接口错误', check=False).to_response()

        secKey = Sessionkey().set_attrs(res)
        secKey.save()
        token = Token(openId).generate_auth_token()
        return ResponseModel(TokenViewModel(token, openId)).to_response()
    else:
        return ResponseModel(code=403, msg_code=4030,
                             msg='微信登录接口错误', check=False).to_response()


@api.route('/api/user/token/verify', methods=['POST'])
def verify():
    token = request.json.get('token')
    if token is None:
        return ResponseModel(dataObj={'isValid': False}, msg_code=4030, msg='token是必须参数', check=False).to_response()

    openId = Token.get_openid(token)
    if openId:
        return ResponseModel(dataObj={'isValid': True}, check=False).to_response()
    else:
        return ResponseModel(dataObj={'isValid': False}, code=401, msg_code=4012,
                             msg='登陆状态已失效', check=False).to_response()


@api.route('/api/user/info', methods=['GET'])
def update_user_info():
    token = request.headers['token']
    oid = Token.get_openid(token)
    if token is None or oid is None:
        return ResponseModel(code=200, msg_code=ErrorCode.TOKEN_IS_MUST,
                             msg='Token失效', check=False).to_response()

    user = User.find_user_by_openid(oid)
    if user is None:
        return ResponseModel(code=200, msg_code=ErrorCode.USER_NOT_EXIST,
                             msg='用户不存在', check=False).to_response()

    uv = UserViewModel(user)
    return ResponseModel(uv,
                         msg='更新用户信息成功',
                         check=False).to_response()
