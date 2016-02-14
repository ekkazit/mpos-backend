from math import ceil
from flask import Blueprint, jsonify, request, g
from sqlalchemy import text
from sqlalchemy.sql import or_
from mpos import db
from app.models import Product
from app.schema import ProductSchema

product_api = Blueprint('product_api', __name__, url_prefix='/api/product')
productSchema = ProductSchema(many=True)


@product_api.before_request
def before_request():
    pass


@product_api.route('/list')
def product_list():
    products = Product.query.all()
    return jsonify({
        'products': productSchema.dump(products).data
    })


@product_api.route('/get', defaults={'id': ''})
@product_api.route('/get/<id>')
def product_get(id):
    product = Product()
    if id:
        product = Product.query.filter_by(id=id).first()
    schema = ProductSchema()
    return jsonify({
        'product': schema.dump(product).data
    })


@product_api.route('/delete/<id>')
def product_delete(id):
    result = 0
    product = Product.query.filter_by(id=id).first()
    if product:
        db.session.delete(product)
        db.session.commit()
    return jsonify({'result': result})


@product_api.route('/deleteall', methods=['POST'])
def product_deleteall():
    result = 0
    f = request.get_json()
    if request.method == 'POST':
        items = f.get('items').split(',');
        for id in items:
            product = Product.query.get(id)
            db.session.delete(product)
            db.session.commit()
            result = 1
    return jsonify({'result': result})


@product_api.route('/save', methods=['POST'])
def product_save():
    result = 0
    f = request.get_json()
    if f is None:
        f = request.form

    forms = {
        'product_name': f.get('product_name') or '',
        'size': f.get('size') or '',
        'detail': f.get('detail') or '',
        'cat_id': f.get('cat_id') or None,
        'subcat_id': f.get('subcat_id') or None,
        'sale_price': f.get('sale_price') or 0,
        'cost': f.get('cost') or 0,
        'img': f.get('img') or None,
        'img_path': f.get('img_path') or None,
        'option_tag': f.get('option_tag') or ''
    }

    id = f.get('id') or None
    if id:
        product = Product.query.get(id)
        for k, v in forms.iteritems():
            setattr(product, k, v)
        db.session.merge(product)
    else:
        product = Product()
        for k, v in forms.iteritems():
            setattr(product, k, v)
        db.session.add(product)
    db.session.commit()

    if product: result = product.id
    return jsonify({'result': result})


@product_api.route('/search', methods=['POST'])
def product_search():
    f = request.get_json()
    if f is None:
        f = request.form

    page = f.get('page') or 1
    rp = f.get('rp') or 10
    term = f.get('term') or ''
    sort = f.get('sort') or None
    desc = f.get('desc') or False
    cat_id = f.get('cat_id') or None

    query = Product.query
    if term:
        query = query.filter(or_(
            Product.product_name.ilike('%' + term + '%'),
            Product.detail.ilike('%' + term + '%'),
        ))

    if cat_id:
        query = query.filter_by(cat_id=cat_id)

    total = query.count()
    total_pages = int(ceil(float(total) / rp))
    results = page * rp
    page_count = results if results <= total else total

    if sort:
        query = query.order_by(text(sort + ' ' + ('desc' if desc else 'asc')))

    products = query.limit(rp).offset((page - 1) * rp)
    return jsonify({
        'total': total,
        'total_pages': total_pages,
        'page_count': page_count,
        'products': productSchema.dump(products).data
    })


@product_api.route('/term', methods=['POST'])
def product_term():
    f = request.get_json()
    if f is None:
        f = request.form

    page = f.get('page') or 1
    rp = f.get('rp') or 10
    term = f.get('term') or ''
    cat_id = f.get('cat_id') or ''
    query = Product.query
    if cat_id:
        query = query.filter_by(cat_id=cat_id)

    if term:
        query = query.filter(or_(
            Product.product_name.ilike('%' + term + '%'),
            Product.detail.ilike('%' + term + '%'),
        ))

    total = query.count()
    total_pages = int(ceil(float(total) / rp))
    results = page * rp
    page_count = results if results <= total else total
    products = query.limit(rp).offset((page - 1) * rp)
    return jsonify({
        'total': total,
        'total_pages': total_pages,
        'page_count': page_count,
        'products': productSchema.dump(products).data
    })
