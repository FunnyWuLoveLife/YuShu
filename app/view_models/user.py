#!/usr/bin/python
# encoding: utf-8

# @file: user.py
# @time: 2018/4/11 22:58
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm


class TokenViewModel:
    def __init__(self, data, openId):
        self.token = data
        self.openId = openId


class UserViewModel:
    def __init__(self, user):
        self.nickname = user.nickname
        self.beans = user.beans
        self.email = user.email
        self.send_receive = '{}/{}'.format(user.send_count, user.receive_count)
