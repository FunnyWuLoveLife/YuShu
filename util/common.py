#!/usr/bin/python
# encoding: utf-8

# @file: common.py
# @time: 2018/4/1 23:51
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm


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
