#!/usr/bin/python
# encoding: utf-8

# @file: trade.py
# @time: 2018/4/16 13:34
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm


class TradeInfo:
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self._parse(goods)

    def _parse(self, goods):
        self.total = len(goods)
        self.trades = [self._map_to_tread(single) for single in goods]
        pass

    def _map_to_tread(self, single):
        """
        把一个Gift或者wish的对象转换为需要的数据格式返回
        :param single:
        :return:
        """
        return dict(
            user_name=single.user.nickname,
            time=single.create_datetime.strftime('%Y-%m-%d'),
            id=single.id
        )
