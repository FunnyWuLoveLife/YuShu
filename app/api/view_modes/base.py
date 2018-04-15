#!/usr/bin/python
# encoding: utf-8

# @file: base.py
# @time: 2018/4/10 18:02
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
import json


class ResponseViewModel:
    def __init__(self, code=None, msg=None, data=None, check=True):
        self.code = code or 200
        self.msg = msg or '请求成功'

        if check and code == 200:
            self.data = data

        else:
            self.data = data

        # 数据不为None和检测的情况下执行
        if data and check:
            if isinstance(data, dict):
                self.msg = {k: ''.join(v) for k, v in data.items()}
                self.code = 400


class ResponseModel:
    default_header = {
        'content-type': 'application/json',
    }

    def __init__(self, dataObj=None, code=200, msg_code=200, msg=None, check=True):
        self.code = 200
        if check:
            # 参数错误

            if dataObj is None:
                self.code = 404
                msg = msg or '请求的资源不存在'
                msg_code = msg_code or 404

            self.data = json.dumps(ResponseViewModel(code=msg_code, msg=msg,
                                                     data=dataObj, check=check),
                                   default=lambda o: o.__dict__)

            if isinstance(dataObj, dict):
                self.code = 400
        else:
            self.code = code
            self.data = json.dumps(ResponseViewModel(code=msg_code, msg=msg,
                                                     data=dataObj, check=check),
                                   default=lambda o: o.__dict__)

    def to_response(self):
        return self.data, self.code, self.default_header
