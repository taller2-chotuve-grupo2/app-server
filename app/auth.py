from flask import Blueprint, request

bp = Blueprint('auth', __name__)

@bp.route('/login/', methods=["POST","GET"])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == "admin" and password == "admin":
        return "OK", 200
    else:
        return "BAD LOGIN", 400