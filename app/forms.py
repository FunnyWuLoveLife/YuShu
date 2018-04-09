#!/usr/bin/python
# encoding: utf-8

# @file: book.py
# @time: 2018/4/4 0:42
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm

"""
表单验证
"""

from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired


class SearchForm(Form):
    q = StringField(validators=[DataRequired(), Length(min=1, max=30)])
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)
