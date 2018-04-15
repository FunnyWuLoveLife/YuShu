#!/usr/bin/python
# encoding: utf-8

# @file: error.py
# @time: 2018/4/15 19:01
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm


class ErrorCode:
    BOOK_NOT_FIND = 6000  # 书籍未找到
    ISBN_CODE_ERROR = 6001  # isbn编号错误
    IS_REGISTER_WX = 6002  # 已经注册过微信信息
    TOKEN_IS_MUST = 6003  # 无效的Token
    ALREADY_IN_GIFT_OR_WISH = 6004  # 书籍已经添加至赠送清单或存在于心意清单
