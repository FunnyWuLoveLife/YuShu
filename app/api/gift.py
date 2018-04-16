#!/usr/bin/python
# encoding: utf-8

# @file: gift.py
# @time: 2018/4/16 18:42
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from flask import request

from . import api, Token
from .view_modes import ResponseModel, BookCollection
from ..models import Gift, User, BookModel, Wish
from ..error import ErrorCode


@api.route('/api/my/gifts')
def my_gifts():
    token = request.headers.get('token')
    openId = Token.get_openid(token)
    user = User.find_user_by_openid(openId)
    if user is None:
        return ResponseModel(msg_code=ErrorCode.TOKEN_IS_MUST,
                             msg='Token无效请登录',
                             check=False).to_response()

    gifts = Gift.find_user_gift(user.id)

    books = BookCollection().fill_by_book_list([BookModel.find_book_by_id(gift.bid) for gift in gifts])

    return ResponseModel(dataObj=books, check=False).to_response()


@api.route('/api/my/wishes')
def my_wishes():
    token = request.headers.get('token')
    openId = Token.get_openid(token)
    user = User.find_user_by_openid(openId)
    if user is None:
        return ResponseModel(msg_code=ErrorCode.TOKEN_IS_MUST,
                             msg='Token无效请登录',
                             check=False).to_response()
    wishes = Wish.find_user_wishes(user.id)

    books = BookCollection().fill_by_book_list([BookModel.find_book_by_id(wish.bid) for wish in wishes])

    return ResponseModel(dataObj=books, check=False).to_response()
