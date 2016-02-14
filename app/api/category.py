from math import ceil
from flask import Blueprint, jsonify, request, g
from mpos import db
from app.models import Category, CategorySub
from app.schema import CategorySchema

category_api = Blueprint('category_api', __name__, url_prefix='/api/category')
categorySchema = CategorySchema(many=True)


@category_api.before_request
def before_request():
    pass


@category_api.route('/list')
def category_list():
    categories = Category.query.join(CategorySub, Category.id == CategorySub.cat_id).all()
    return jsonify({
        'categories': categorySchema.dump(categories).data
    })


@category_api.route('/all', defaults={'id': ''})
@category_api.route('/all/<id>')
def category_all(id):
    if id:
        categories = Category.query.filter(Category.id != id).all()
    else:
        categories = Category.query.all()
    return jsonify({
        'categories': categorySchema.dump(categories).data
    })


@category_api.route('/sublist', defaults={'id': ''})
@category_api.route('/sublist/<id>')
def categorysub_list(id):
    if id:
        subcategories = Category.query.join(CategorySub, Category.id == CategorySub.subcat_id).filter_by(
            cat_id=id).all()
    else:
        subcategories = Category.query.join(CategorySub, Category.id == CategorySub.subcat_id).all()
    return jsonify({
        'subcategories': categorySchema.dump(subcategories).data
    })


@category_api.route('/get', defaults={'id': ''})
@category_api.route('/get/<id>')
def category_get(id):
    if id:
        sql = "select c1.id, c1.category_name, c2.id as parent_id, c2.category_name as parent_name " \
              "from category c1 left join category_sub s1 on c1.id=s1.subcat_id left join category c2 on c2.id=s1.cat_id " \
              "where c1.id=" + str(id)
        r = db.session.execute(sql, {}).first()
        category = {
            'id': r[0],
            'category_name': r[1],
            'parent_id': r[2],
            'parent_name': r[3],
        }
    else:
        c = Category()
        category = CategorySchema().dump(c).data
    return jsonify({
        'category': category
    })


@category_api.route('/delete/<id>')
def category_delete(id):
    result = 0
    category = Category.query.filter_by(id=id).first()
    if category:
        result = category.id
        db.session.delete(category)
        db.session.commit()
    return jsonify({'result': result})


@category_api.route('/save', methods=['POST'])
def category_save():
    result = 0
    f = request.get_json()
    if f is None:
        f = request.form

    forms = {
        'category_name': f.get('category_name') or '',
    }

    id = f.get('id') or None
    parent_id = f.get('parent_id') or None
    if id:
        category = Category.query.get(id)
        for k, v in forms.iteritems():
            setattr(category, k, v)
        db.session.merge(category)
    else:
        category = Category()
        for k, v in forms.iteritems():
            setattr(category, k, v)
        db.session.add(category)

    db.session.commit()
    id = category.id
    if parent_id and id != parent_id:
        CategorySub.query.filter_by(subcat_id=id).delete()
        db.session.add(CategorySub(cat_id=parent_id, subcat_id=id))
    db.session.commit()

    if category: result = category.id
    return jsonify({'result': result})


@category_api.route('/search', methods=['POST'])
def category_search():
    f = request.get_json()
    if f is None:
        f = request.form
    page = f.get('page') or 1
    rp = f.get('rp') or 10
    term = f.get('term') or ''
    sort = f.get('sort') or None
    desc = f.get('desc') or False

    sql = "select c1.id, c1.category_name, c2.id as parent_id, c2.category_name as parent_name " \
          "from category c1 left join category_sub s1 on c1.id=s1.subcat_id left join category c2 on c2.id=s1.cat_id " \
          "where 1=1"

    results = db.session.execute(sql, {}).fetchall()

    if term:
        sql += " and c1.category_name like '%" + term + "%'"

    if sort:
        sql += " order by " + sort + " " + ("desc" if desc else "asc")

    total = len(results)
    total_pages = int(ceil(float(total) / rp))
    results = page * rp
    page_count = results if results <= total else total

    sql += " limit " + str((page - 1) * rp) + ", " + str(rp)
    results = db.session.execute(sql, {}).fetchall()
    categories = []
    for r in results:
        cols = {
            'id': r[0],
            'category_name': r[1],
            'parent_id': r[2],
            'parent_name': r[3],
        }
        categories.append(cols)

    return jsonify({
        'total': total,
        'total_pages': total_pages,
        'page_count': page_count,
        'categories': categories
    })


@category_api.route('/deleteall', methods=['POST'])
def category_deleteall():
    result = 0
    f = request.get_json()
    if request.method == 'POST':
        items = f.get('items').split(',');
        for id in items:
            CategorySub.query.filter_by(subcat_id=id).delete()
            db.session.commit()
            category = Category.query.get(id)
            db.session.delete(category)
            db.session.commit()
            result = 1
    return jsonify({'result': result})
