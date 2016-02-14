# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, flash, redirect, url_for, session
from app.models import Product, Category, Branch, User, Member, BranchType
from functools import wraps

admin = Blueprint('admin', __name__, url_prefix='/admin')


def logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in') is not None:
            return f(*args, **kwargs)
        else:
            flash(u'กรุณาล็อกอินเพื่อเข้าสู่ระบบ', 'error')
            return redirect(url_for('auth.login'))

    return decorated_function


@admin.before_request
@logged_in
def before_request():
    pass


@admin.route('/home')
def home():
    return render_template('admin/home.html')


@admin.route('/product')
def product():
    return render_template('admin/product/index.html')


@admin.route('/product/form', defaults={'id': ''})
@admin.route('/product/form/<id>')
def product_form(id):
    product = Product.query.get(id)
    return render_template('admin/product/form.html', id=id, product=product)


@admin.route('/category')
def category():
    return render_template('admin/category/index.html')


@admin.route('/category/form', defaults={'id': ''})
@admin.route('/category/form/<id>')
def category_form(id):
    category = Category.query.get(id)
    return render_template('admin/category/form.html', id=id, category=category)


@admin.route('/branch')
def branch():
    return render_template('admin/branch/index.html')


@admin.route('/branch/form', defaults={'id': ''})
@admin.route('/branch/form/<id>')
def branch_form(id):
    branch = Branch.query.get(id)
    return render_template('admin/branch/form.html', id=id, branch=branch)


@admin.route('/btype')
def btype():
    return render_template('admin/btype/index.html')


@admin.route('/btype/form', defaults={'id': ''})
@admin.route('/btype/form/<id>')
def btype_form(id):
    branch_type = BranchType.query.get(id)
    return render_template('admin/btype/form.html', id=id, branch_type=branch_type)


@admin.route('/btype/product', defaults={'id': ''})
@admin.route('/btype/product/<id>')
def btype_product(id):
    branch_type = BranchType.query.get(id)
    return render_template('admin/btype/product.html', id=id, branch_type=branch_type)


@admin.route('/member')
def member():
    return render_template('admin/member/index.html')


@admin.route('/member/form', defaults={'id': ''})
@admin.route('/member/form/<id>')
def member_form(id):
    member = Member.query.get(id)
    return render_template('admin/member/form.html', id=id, member=member)


@admin.route('/users')
def users():
    return render_template('admin/users/index.html')


@admin.route('/users/form', defaults={'id': ''})
@admin.route('/users/form/<id>')
def users_form(id):
    user = User.query.get(id)
    return render_template('admin/users/form.html', id=id, user=user)


@admin.route('/reports')
def reports():
    return render_template('admin/reports/index.html')


@admin.route('/synchronize')
def synchronize():
    return render_template('admin/synchronize/index.html')
