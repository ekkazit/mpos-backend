from math import ceil
from flask import Blueprint, jsonify, request, g, json
from sqlalchemy import text
from sqlalchemy.sql import or_
from mpos import db
from app.models import BranchType, BranchTypeProduct
from app.schema import BranchTypeSchema, BranchTypeProductSchema

branchtype_api = Blueprint('branchtype_api', __name__, url_prefix='/api/branchtype')
branchTypeSchema = BranchTypeSchema(many=True)


@branchtype_api.before_request
def before_request():
    g.sid = 1


@branchtype_api.route('/list')
def branchtype_list():
    branchtype = BranchType.query.all()
    return jsonify({
        'branch_types': branchTypeSchema.dump(branchtype).data
    })


@branchtype_api.route('/get', defaults={'id': ''})
@branchtype_api.route('/get/<id>')
def branchtype_get(id):
    branch_type = BranchType.query.filter_by(id=id).first()
    schema = BranchTypeSchema()
    return jsonify({
        'branch_type': schema.dump(branch_type).data
    })


@branchtype_api.route('/getproduct', defaults={'id': ''})
@branchtype_api.route('/getproduct/<id>')
def branchtype_getproduct(id):
    product_items = BranchTypeProduct.query.filter_by(branch_type_id=id).all()
    schema = BranchTypeProductSchema(many=True)
    return jsonify({
        'product_items': schema.dump(product_items).data
    })


@branchtype_api.route('/delete/<id>')
def branchtype_delete(id):
    result = 0
    branch_type = BranchType.query.filter_by(id=id).first()
    if branch_type:
        result = branch_type.id
        db.session.delete(branch_type)
        db.session.commit()
    return jsonify({'result': result})


@branchtype_api.route('/save', methods=['POST'])
def branchtype_save():
    result = 0
    f = request.get_json()
    if f is None:
        f = request.form

    forms = {
        'branch_type_name': f.get('branch_type_name') or '',
    }

    id = f.get('id') or None
    if id:
        branch = BranchType.query.get(id)
        for k, v in forms.iteritems():
            setattr(branch, k, v)
        db.session.merge(branch)
    else:
        branch = BranchType()
        for k, v in forms.iteritems():
            setattr(branch, k, v)
        db.session.add(branch)
    db.session.commit()

    if branch: result = branch.id
    return jsonify({'result': result})


@branchtype_api.route('/formsave', methods=['POST'])
def branchtype_formsave():
    result = 0
    f = request.get_json()
    if f is None:
        f = request.form

    product_items = json.loads(f.get('product_items'))
    id = f.get('id') or None
    if id:
        BranchTypeProduct.query.filter_by(branch_type_id=id).delete()
        db.session.commit()
        for elem in product_items:
            bt = BranchTypeProduct(branch_type_id=id, product_id=elem.get('id'), sale_price=elem.get('price'),
                                   cost=elem.get('cost'))
            db.session.add(bt)
            db.session.commit()
        result = id
    return jsonify({'result': result})


@branchtype_api.route('/search', methods=['POST'])
def branchtype_search():
    f = request.get_json()
    if f is None:
        f = request.form
    page = f.get('page') or 1
    rp = f.get('rp') or 10
    term = f.get('term') or ''
    sort = f.get('sort') or None
    desc = f.get('desc') or False

    query = BranchType.query
    if term:
        query = query.filter(or_(
            BranchType.branch_type_name.ilike('%' + term + '%'),
        ))

    if sort:
        query = query.order_by(text(sort + ' ' + ('desc' if desc else 'asc')))

    total = query.count()
    total_pages = int(ceil(float(total) / rp))
    results = page * rp
    page_count = results if results <= total else total

    branch_types = query.limit(rp).offset((page - 1) * rp)
    return jsonify({
        'total': total,
        'total_pages': total_pages,
        'page_count': page_count,
        'branch_types': branchTypeSchema.dump(branch_types).data
    })


@branchtype_api.route('/deleteall', methods=['POST'])
def branchtype_deleteall():
    result = 0
    f = request.get_json()
    if request.method == 'POST':
        items = f.get('items').split(',');
        for id in items:
            BranchTypeProduct.query.filter_by(branch_type_id=id).delete()
            db.session.commit()
            category = BranchType.query.get(id)
            db.session.delete(category)
            db.session.commit()
            result = 1
    return jsonify({'result': result})
