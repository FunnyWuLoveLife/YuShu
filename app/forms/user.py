#!/usr/bin/python
# encoding: utf-8

# @file: user.py
# @time: 2018/4/14 0:16
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError

from ..models import User


class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                    Email(message='电子邮件不符合规范')])


class RegisterForm(EmailForm):
    password = PasswordField(validators=[
        DataRequired(message='密码不能为空，请输入你的密码'), Length(6, 32)])
    nickname = StringField(validators=[
        DataRequired(), Length(2, 10, message='昵称至少需要两个字符，最多10个字符')])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮件已被注册')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('该昵称已存在')


class LoginForm(EmailForm):
    password = PasswordField(validators=[
        DataRequired(message='密码不能为空，请输入你的密码'), Length(6, 32)])


class ChangePasswordForm(Form):
    password1 = PasswordField(validators=[
        DataRequired(message='密码不能为空，请输入你的密码'), Length(6, 32, message='密码应该是6到32位字符串，请重新输入')])
    password2 = PasswordField(validators=[
        DataRequired(message='密码不能为空，请输入你的密码'), Length(6, 32, message='密码应该是6到32位字符串，请重新输入')])

    def validate_password2(self, field):
        if self.password1.data != field.data:
            raise ValidationError('两次密码不一致，请重新输入')
