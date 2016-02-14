from flask import Blueprint, jsonify

echo_api = Blueprint('echo_api', __name__, url_prefix='/api/echo')


@echo_api.route('/print')
def echo_print():
    return jsonify({'echo': 'echo from api'})
