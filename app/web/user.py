#!/usr/bin/python
# encoding: utf-8

# @file: user.py
# @time: 2018/4/4 0:22
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from flask import render_template, request, redirect, url_for
from . import web
from ..forms import RegisterForm, LoginForm
from ..models import User

__author__ = '七月'


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        user.set_attrs(form.data)
        user.save()
        redirect(url_for('web.login'))  # 重定向到登录页面
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate():
        pass
    return render_template('auth/login.html', form={'data': {}})


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    pass


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    pass


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    pass


@web.route('/register/confirm/<token>')
def confirm(token):
    pass


@web.route('/register/ajax', methods=['GET', 'POST'])
def register_ajax():
    pass
