from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash, session
from flask_babel import Babel
from flask_mail import Mail
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object('config')

babel = Babel(app)
mail = Mail(app)
manager = Manager(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['th'])


@app.route('/public/<path:filename>')
def base_static(filename):
    return send_from_directory(app.root_path + '/public', filename)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.route('/')
def index():
    return redirect(url_for('auth.login'))


from werkzeug.utils import import_string

for blueprint in app.config['BLUEPRINTS']:
    app.register_blueprint(import_string(blueprint))
