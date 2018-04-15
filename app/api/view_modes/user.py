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
        self.nickname = ''
        self.email = ''
        self.phone_number = ''
        self.beans = 0
        self.send_counter = 0
        self.receive_counter = 0

        # 微信
        self.avatarUrl = ""
        self.gender = ""
        self.city = ""
        self.province = ""
        self.country = ""
        self.language = ""

        self.fill(user)

    def fill(self, user):
        self.set_attrs(user.__dict__)

    def set_attrs(self, attrs_dict):
        for k, v in attrs_dict.items():
            if hasattr(self, k):
                setattr(self, k, v)  # 动态赋值
        return self
