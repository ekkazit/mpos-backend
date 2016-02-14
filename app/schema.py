from mpos import ma
from marshmallow import fields
from app.models import Category, Product, Branch, BranchType, User, Member, BranchTypeProduct


def get_fields(cl, include=None, exclude=None):
    base = []
    if exclude:
        base += exclude
    cols = [k for k in cl.__dict__.keys() if not k.startswith('_') and not k.endswith('_')]
    result_fields = list(set(cols) - set(base))
    if include:
        result_fields += include
    return result_fields


class CategorySchema(ma.Schema):
    class Meta:
        fields = get_fields(Category, exclude=['products', 'products_sub'])


class CategorySubSchema(ma.Schema):
    class Meta:
        fields = get_fields(Category, exclude=['products', 'products_sub'])


class ProductSchema(ma.Schema):
    category = fields.Nested(CategorySchema, only=('id', 'category_name'))
    sub = fields.Nested(CategorySubSchema, only=('id', 'category_name'))

    class Meta:
        fields = get_fields(Product, include=['category', 'sub'], exclude=['transactions', 'branch_types'])


class BranchTypeSchema(ma.Schema):
    class Meta:
        fields = get_fields(BranchType, exclude=['branches'])


class BranchTypeProductSchema(ma.Schema):
    product = fields.Nested(ProductSchema, only=('id', 'product_name'))

    class Meta:
        fields = get_fields(BranchTypeProduct, include=['product'])


class BranchSchema(ma.Schema):
    branch_type = fields.Nested(BranchTypeSchema, only=('id', 'branch_type_name'))

    class Meta:
        fields = get_fields(Branch, include=['branch_type'], exclude=['users', 'members'])


class UserSchema(ma.Schema):
    branch = fields.Nested(BranchSchema, only=('id', 'branch_name'))

    class Meta:
        fields = get_fields(User, include=['branch'])


class MemberSchema(ma.Schema):
    branch = fields.Nested(BranchSchema, only=('id', 'branch_name'))

    class Meta:
        fields = get_fields(Member, include=['branch'])
