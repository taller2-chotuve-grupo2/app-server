from flask import Blueprint

bp = Blueprint('auth', __name__)

@bp.route('/login/', methods=["POST","GET"])
def login():
    return "BAD LOGIN", 400