from mpos import db


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    update_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class Category(Base):
    __tablename__ = 'category'
    category_name = db.Column(db.String(100))
    products = db.relationship('Product', backref='category', lazy='dynamic', foreign_keys='Product.cat_id')
    products_sub = db.relationship('Product', backref='sub', lazy='dynamic', foreign_keys='Product.subcat_id')

    def __init__(self, *args, **kwargs):
        super(Category, self).__init__(*args, **kwargs)

    def __repr__(self):
        return 'category %r' % self.category_name


class CategorySub(Base):
    __tablename__ = 'category_sub'
    cat_id = db.Column(db.Integer)
    subcat_id = db.Column(db.Integer)

    def __init__(self, *args, **kwargs):
        super(CategorySub, self).__init__(*args, **kwargs)

    def __repr__(self):
        return 'category_sub %r' % self.cat_id


class Product(Base):
    __tablename__ = 'product'
    cat_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    subcat_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    product_name = db.Column(db.String(100))
    detail = db.Column(db.String(500), nullable=True)
    sale_price = db.Column(db.Float, default=0)
    cost = db.Column(db.Float, default=0)
    size = db.Column(db.Integer)
    option_tag = db.Column(db.String(100), nullable=True)
    img = db.Column(db.String(50), nullable=True)
    img_path = db.Column(db.String(100), nullable=True)
    branch_types = db.relationship('BranchTypeProduct', backref='product', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)

    def __repr__(self):
        return 'product %r' % self.product_name


class BranchType(Base):
    __tablename__ = 'branch_type'
    branch_type_name = db.Column(db.String(100))
    branches = db.relationship('Branch', backref='branch_type', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super(BranchType, self).__init__(*args, **kwargs)

    def __repr__(self):
        return 'branch_type %r' % self.branch_type_name


class Branch(Base):
    __tablename__ = 'branch'
    branch_name = db.Column(db.String(100))
    branch_type_id = db.Column(db.Integer, db.ForeignKey('branch_type.id'))
    users = db.relationship('User', backref='branch', lazy='dynamic')
    members = db.relationship('Member', backref='branch', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super(Branch, self).__init__(*args, **kwargs)

    def __repr__(self):
        return 'branch %r' % self.branch_name


class BranchTypeProduct(Base):
    __tablename__ = 'branch_type_product'
    branch_type_id = db.Column(db.Integer, db.ForeignKey('branch_type.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    sale_price = db.Column(db.Float, default=0)
    cost = db.Column(db.Float, default=0)

    def __init__(self, *args, **kwargs):
        super(BranchTypeProduct, self).__init__(*args, **kwargs)

    def __repr__(self):
        return 'branch_type_product %r' % self.id


class Member(Base):
    __tablename__ = 'member'
    member_id = db.Column(db.String(50), unique=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    member_name = db.Column(db.String(100), nullable=True)
    gender = db.Column(db.String(1), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    tel = db.Column(db.String(20), nullable=True)

    def __init__(self, *args, **kwargs):
        super(Member, self).__init__(*args, **kwargs)

    def __repr__(self):
        return 'member %r' % self.member_name


class User(Base):
    __tablename__ = 'users'
    user_name = db.Column(db.String(50))
    user_password = db.Column(db.String(150))
    firstname = db.Column(db.String(100), nullable=True)
    lastname = db.Column(db.String(100), nullable=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    user_type = db.Column(db.String(10), nullable=True)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        return 'users %r' % self.user_name


class Bill(Base):
    __tablename__ = 'bill'
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    bill_no = db.Column(db.String(50))
    shift_id = db.Column(db.Integer)
    total_price = db.Column(db.Float, default=0)
    bill_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    money_received = db.Column(db.Float, default=0)
    status = db.Column(db.String(20))

    def __init__(self, *args, **kwargs):
        super(Bill, self).__init__(*args, **kwargs)

    def __repr__(self):
        return 'bill %r' % self.bill_no


class Transaction(Base):
    __tablename__ = 'transactions'
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    bill_no = db.Column(db.String(50))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    amount = db.Column(db.Integer)
    unit_price = db.Column(db.Float, default=0)
    status = db.Column(db.String(20))

    def __init__(self, *args, **kwargs):
        super(Transaction, self).__init__(*args, **kwargs)

    def __repr__(self):
        return 'transactions %r' % self.bill_no
