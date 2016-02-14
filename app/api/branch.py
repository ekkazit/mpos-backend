from math import ceil
from flask import Blueprint, jsonify, request, g
from sqlalchemy import text
from sqlalchemy.sql import or_
from mpos import db
from app.models import Branch
from app.schema import BranchSchema

branch_api = Blueprint('branch_api', __name__, url_prefix='/api/branch')
branchSchema = BranchSchema(many=True)


@branch_api.before_request
def before_request():
    g.sid = 1


@branch_api.route('/list')
def branch_list():
    branches = Branch.query.all()
    return jsonify({
        'branches': branchSchema.dump(branches).data
    })


@branch_api.route('/get', defaults={'id': ''})
@branch_api.route('/get/<id>')
def branch_get(id):
    branch = Branch.query.filter_by(id=id).first()
    schema = BranchSchema()
    return jsonify({
        'branch': schema.dump(branch).data
    })


@branch_api.route('/delete/<id>')
def branch_delete(id):
    result = 0
    branch = Branch.query.filter_by(id=id).first()
    if branch:
        result = branch.id
        if branch.is_active == 'N':
            db.session.delete(branch)
        else:
            branch.is_active = 'N'
            db.session.merge(branch)
        db.session.commit()
    return jsonify({'result': result})


@branch_api.route('/save', methods=['POST'])
def branch_save():
    result = 0
    f = request.get_json()
    if f is None:
        f = request.form

    forms = {
        'branch_type_id': f.get('branch_type_id') or None,
        'branch_name': f.get('branch_name') or '',
    }

    id = f.get('id') or None
    if id:
        branch = Branch.query.get(id)
        for k, v in forms.iteritems():
            setattr(branch, k, v)
        db.session.merge(branch)
    else:
        branch = Branch()
        for k, v in forms.iteritems():
            setattr(branch, k, v)
        db.session.add(branch)
    db.session.commit()

    if branch: result = branch.id
    return jsonify({'result': result})


@branch_api.route('/search', methods=['POST'])
def branch_search():
    f = request.get_json()
    if f is None:
        f = request.form
    page = f.get('page') or 1
    rp = f.get('rp') or 10
    term = f.get('term') or ''
    sort = f.get('sort') or None
    desc = f.get('desc') or False

    query = Branch.query
    if term:
        query = query.filter(or_(
            Branch.branch_name.ilike('%' + term + '%'),
        ))

    if sort:
        query = query.order_by(text(sort + ' ' + ('desc' if desc else 'asc')))

    total = query.count()
    total_pages = int(ceil(float(total) / rp))
    results = page * rp
    page_count = results if results <= total else total

    branches = query.limit(rp).offset((page - 1) * rp)
    return jsonify({
        'total': total,
        'total_pages': total_pages,
        'page_count': page_count,
        'branches': branchSchema.dump(branches).data
    })


@branch_api.route('/deleteall', methods=['POST'])
def branch_deleteall():
    result = 0
    f = request.get_json()
    if request.method == 'POST':
        items = f.get('items').split(',');
        for id in items:
            branch = Branch.query.get(id)
            db.session.delete(branch)
            db.session.commit()
            result = 1
    return jsonify({'result': result})
