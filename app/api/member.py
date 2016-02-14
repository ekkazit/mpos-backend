from math import ceil
from flask import Blueprint, jsonify, request, g
from sqlalchemy import text
from sqlalchemy.sql import or_
from mpos import db
from app.models import Member
from app.schema import MemberSchema

member_api = Blueprint('member_api', __name__, url_prefix='/api/member')
memberSchema = MemberSchema(many=True)


@member_api.before_request
def before_request():
    g.sid = 1
    g.bid = 1


@member_api.route('/list')
def member_list():
    members = Member.query.all()
    return jsonify({
        'members': memberSchema.dump(members).data
    })


@member_api.route('/get', defaults={'id': ''})
@member_api.route('/get/<id>')
def member_get(id):
    member = Member.query.filter_by(id=id).first()
    schema = MemberSchema()
    return jsonify({
        'member': schema.dump(member).data
    })


@member_api.route('/delete/<id>')
def member_delete(id):
    result = 0
    member = Member.query.filter_by(id=id).first()
    if member:
        result = member.id
        db.session.delete(member)
        db.session.commit()
    return jsonify({'result': result})


@member_api.route('/save', methods=['POST'])
def member_save():
    result = 0
    f = request.get_json()
    if f is None:
        f = request.form
    forms = {
        'member_id': f.get('member_id') or '',
        'branch_id': f.get('branch_id') or None,
        'member_name': f.get('member_name') or '',
        'gender': f.get('gender') or '',
        'email': f.get('email') or '',
        'tel': f.get('tel') or '',
    }
    id = f.get('id') or None
    if id:
        member = Member.query.get(id)
        for k, v in forms.iteritems():
            setattr(member, k, v)
        db.session.merge(member)
    else:
        member = Member()
        for k, v in forms.iteritems():
            setattr(member, k, v)
        db.session.add(member)
    db.session.commit()

    if member: result = member.id
    return jsonify({'result': result})


@member_api.route('/search', methods=['POST'])
def member_search():
    f = request.get_json()
    if f is None:
        f = request.form
    page = f.get('page') or 1
    rp = f.get('rp') or 10
    term = f.get('term') or ''
    sort = f.get('sort') or None
    desc = f.get('desc') or False

    query = Member.query
    if term:
        query = query.filter(or_(
            Member.member_name.ilike('%' + term + '%'),
            Member.email.ilike('%' + term + '%'),
        ))

    if sort:
        query = query.order_by(text(sort + ' ' + ('desc' if desc else 'asc')))

    total = query.count()
    total_pages = int(ceil(float(total) / rp))
    results = page * rp
    page_count = results if results <= total else total

    members = query.limit(rp).offset((page - 1) * rp)
    return jsonify({
        'total': total,
        'total_pages': total_pages,
        'page_count': page_count,
        'members': memberSchema.dump(members).data
    })


@member_api.route('/deleteall', methods=['POST'])
def member_deleteall():
    result = 0
    f = request.get_json()
    if request.method == 'POST':
        items = f.get('items').split(',');
        for id in items:
            member = Member.query.get(id)
            db.session.delete(member)
            db.session.commit()
            result = 1
    return jsonify({'result': result})
