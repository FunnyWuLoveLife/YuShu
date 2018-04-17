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
        header = {
            'Accept': 'application/json; charset=utf-8',
            'Accept-Encoding': 'must-revalidate, no-cache, private',
            'Accept-Language': '',
            'Connection': 'keep-alive',
            'Cookie': 'bid=Uh02t4LfThg; ll="108296"; gr_user_id=478cbd72-82c7-4f8b-b3cd-789322938e52; '
                      '_vwo_uuid_v2=D8AF411E5F46FAA8B9E2450BD4C80DE6B|66a24eea02fe37b10a2c8c5833cc56d9; '
                      'viewed="26079463"; __utmz=30149280.1523516488.5.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic;'
                      ' __utma=30149280.1605453785.1522474186.1523516488.1523962567.6; __utmc=30149280',
            'Host': 'api.douban.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.3',
        }
        r = requests.get(url)
        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text
