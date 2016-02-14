import os

BASEDIR = os.path.dirname(os.path.abspath(__file__))
TEMP_PATH = os.path.join(BASEDIR, 'public/temp/')
UPLOAD_PATH = os.path.join(BASEDIR, 'public/upload/')

DEBUG = True

SECRET_KEY = 'secret'

BABEL_DEFAULT_LOCALE = 'th'

SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/mpos'
SQLALCHEMY_POOL_SIZE = 20

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'ekkazit@gmail.com'
MAIL_PASSWORD = ''

BLUEPRINTS = [
    'app.modules.auth.auth',
    'app.modules.admin.admin',
    'app.api.fileupload.fileupload_api',
    'app.api.echo.echo_api',
    'app.api.product.product_api',
    'app.api.category.category_api',
    'app.api.branchtype.branchtype_api',
    'app.api.branch.branch_api',
    'app.api.users.user_api',
    'app.api.member.member_api',
]
