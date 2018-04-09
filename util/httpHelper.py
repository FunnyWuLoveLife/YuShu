#!/usr/bin/python
# encoding: utf-8

# @file: http.py
# @time: 2018/4/1 23:58
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
import requests


class HTTP:
    @staticmethod
    def get(url, return_json=True):
        """
        get 获取数据
        :param url: <str>:获取地址
        :param return_json: <bool>:是否返回json格式的数据
        :return: <dict> or str
        """
        r = requests.get(url)
        if r.status_code != 200:
            return {} if return_json else ''

        return r.json() if return_json else r.text
