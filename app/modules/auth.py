# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from mpos import bcrypt
from app.models import User

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    f = request.form
    if request.method == 'POST':
        username = f.get('username')
        password = f.get('password')
        user = User.query.filter_by(user_name=username).first()
        if user and bcrypt.check_password_hash(user.user_password, password):
            session['logged_in'] = username
            return redirect(url_for('admin.home'))
        flash(u'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง', 'error')
    return render_template('login.html', error=error)


@auth.route('/logout')
def logout():
    session.clear()
    flash(u'คุณได้ออกจากระบบแล้ว', 'success')
    return redirect(url_for('auth.login'))
