#!/usr/bin/python
# encoding: utf-8

# @file: book.py
# @time: 2018/4/9 17:08
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm

from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired


class SearchForm(Form):
    q = StringField(validators=[DataRequired(), Length(min=1, max=30)])
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)


class IsbnForm(Form):
    isbn = StringField(validators=[DataRequired(), Length(min=10, max=13)])


class ReqDonateForm(Form):
    tid = IntegerField(validators=[DataRequired(message='uid是必须参数')])


class DetailForm(IsbnForm):
    gid = IntegerField()
    wid = IntegerField()
