#!/usr/bin/python
# encoding: utf-8

# @file: user.py
# @time: 2018/4/4 0:22
# @author: FunnyWu
# @contact: agiot1026@163.com
# @Software: PyCharm
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user

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
        return redirect(url_for('web.login'))  # 重定向到登录页面
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            return render_template('auth/register.html', form={'data': {}})
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)  # 默认是365天
            next_url = request.args.get('next')
            # 判断是否是跳转过来的url
            if not next_url or not next_url.startswith('/'):
                next_url = url_for('web.index')
            return redirect(next_url)
        else:
            flash(form.errors)

    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    pass


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    return render_template('auth/forget_password_request.html')


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    return render_template('auth/forget_password.html')


@web.route('/logout')
def logout():
    return render_template('index.html')


@web.route('/register/confirm/<token>')
def confirm(token):
    pass


@web.route('/register/ajax', methods=['GET', 'POST'])
def register_ajax():
    pass
