from math import ceil
from flask import Blueprint, jsonify, request, g
from sqlalchemy import text
from sqlalchemy.sql import or_
from mpos import db, bcrypt
from app.models import User
from app.schema import UserSchema

user_api = Blueprint('user_api', __name__, url_prefix='/api/user')
userSchema = UserSchema(many=True)


@user_api.before_request
def before_request():
    g.sid = 1
    g.bid = 1


@user_api.route('/list')
def user_list():
    users = User.query.all()
    return jsonify({
        'users': userSchema.dump(users).data
    })


@user_api.route('/get', defaults={'id': ''})
@user_api.route('/get/<id>')
def user_get(id):
    user = User.query.filter_by(id=id).first()
    schema = UserSchema()
    return jsonify({
        'user': schema.dump(user).data
    })


@user_api.route('/delete/<id>')
def user_delete(id):
    result = 0
    user = User.query.filter_by(id=id).first()
    if user:
        result = user.id
        db.session.delete(user)
        db.session.commit()
    return jsonify({'result': result})


@user_api.route('/save', methods=['POST'])
def user_save():
    result = 0
    f = request.get_json()
    if f is None:
        f = request.form

    forms = {
        'user_name': f.get('user_name') or '',
        'user_password': bcrypt.generate_password_hash(f.get('user_password') or ''),
        'firstname': f.get('firstname') or '',
        'lastname': f.get('lastname') or '',
        'branch_id': f.get('branch_id') or None,
        'user_type': f.get('user_type') or '',
    }

    id = f.get('id') or None
    if id:
        user = User.query.get(id)
        for k, v in forms.iteritems():
            setattr(user, k, v)
        db.session.merge(user)
    else:
        user = User()
        for k, v in forms.iteritems():
            setattr(user, k, v)
        db.session.add(user)
    db.session.commit()

    if user: result = user.id
    return jsonify({'result': result})


@user_api.route('/search', methods=['POST'])
def user_search():
    f = request.get_json()
    if f is None:
        f = request.form
    page = f.get('page') or 1
    rp = f.get('rp') or 10
    term = f.get('term') or ''
    sort = f.get('sort') or None
    desc = f.get('desc') or False

    query = User.query
    if term:
        query = query.filter(or_(
            User.user_name.ilike('%' + term + '%'),
            User.firstname.ilike('%' + term + '%'),
            User.lastname.ilike('%' + term + '%'),
        ))

    if sort:
        query = query.order_by(text(sort + ' ' + ('desc' if desc else 'asc')))

    total = query.count()
    total_pages = int(ceil(float(total) / rp))
    results = page * rp
    page_count = results if results <= total else total

    users = query.limit(rp).offset((page - 1) * rp)
    return jsonify({
        'total': total,
        'total_pages': total_pages,
        'page_count': page_count,
        'users': userSchema.dump(users).data
    })


@user_api.route('/deleteall', methods=['POST'])
def user_deleteall():
    result = 0
    f = request.get_json()
    if request.method == 'POST':
        items = f.get('items').split(',');
        for id in items:
            user = User.query.get(id)
            db.session.delete(user)
            db.session.commit()
            result = 1
    return jsonify({'result': result})
