#!/usr/bin/python
# encoding: utf-8

# @file: error.py
# @time: 2018/4/15 19:01
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm


class ErrorCode:
    SERVER_ERROR = 500  # 服务器内部错误

    PARAMETERS_ERROR = 5999  # 参数错误

    BOOK_NOT_FIND = 6000  # 书籍未找到
    ISBN_CODE_ERROR = 6001  # isbn编号错误
    IS_REGISTER_WX = 6002  # 已经注册过微信信息
    TOKEN_IS_MUST = 6003  # 无效的Token
    ALREADY_IN_GIFT_OR_WISH = 6004  # 书籍已经添加至赠送清单或存在于心意清单
    USER_NOT_EXIST = 6005  # 用户不存在
    BEANS_NOT_ENOUGH = 6006  # 书豆不足
    CAN_NOT_OPER_OTHERS = 6007  # 不能操作其他用户的数据
