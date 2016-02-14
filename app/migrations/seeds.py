# -*- coding: utf-8 -*-

from app.models import *
from mpos import bcrypt


def branch_type_seeder():
    db.session.add(BranchType(branch_type_name=u'กลุ่มสาขา1'))
    db.session.add(BranchType(branch_type_name=u'กลุ่มสาขา2'))
    db.session.commit()


def branch_seeder():
    db.session.add(Branch(branch_name=u'สำนักงานใหญ่', branch_type_id=1))
    db.session.add(Branch(branch_name=u'ชลบุรี', branch_type_id=1))
    db.session.add(Branch(branch_name=u'สมุทรปราการ', branch_type_id=2))
    db.session.commit()


def user_seeder():
    db.session.add(
        User(user_name='admin', user_password=bcrypt.generate_password_hash('admin'), firstname=u'ผู้ดูแลระบบ',
             lastname='', branch_id=1, user_type='admin'))
    db.session.add(
        User(user_name='cashier', user_password=bcrypt.generate_password_hash('cashier'), firstname=u'แคชเชียร์',
             lastname='', branch_id=1, user_type='cashier'))
    db.session.add(
        User(user_name='staff', user_password=bcrypt.generate_password_hash('staff'), firstname=u'สตาฟ',
             lastname='', branch_id=1, user_type='staff'))
    db.session.commit()


def category_seeder():
    db.session.add(Category(category_name=u'กาแฟ'))
    db.session.add(Category(category_name=u'อาหาร'))
    db.session.add(Category(category_name=u'ขนม'))
    db.session.add(Category(category_name=u'ไอศกรีม'))
    db.session.add(Category(category_name=u'ร้อน'))
    db.session.add(Category(category_name=u'เย็น'))
    db.session.add(Category(category_name=u'ปั่น'))
    db.session.add(Category(category_name=u'อาหารไทย'))
    db.session.add(Category(category_name=u'อาหารจีน'))
    db.session.commit()

    db.session.add(CategorySub(cat_id=1, subcat_id=5))
    db.session.add(CategorySub(cat_id=1, subcat_id=6))
    db.session.add(CategorySub(cat_id=1, subcat_id=7))
    db.session.add(CategorySub(cat_id=2, subcat_id=8))
    db.session.add(CategorySub(cat_id=2, subcat_id=9))
    db.session.commit()


def run_seed():
    branch_type_seeder()
    branch_seeder()
    user_seeder()
    category_seeder()
    print 'All tables seeded'


if __name__ == '__main__':
    run_seed()
