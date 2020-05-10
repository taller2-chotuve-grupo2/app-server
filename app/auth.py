from flask import Blueprint, request
import requests

bp = Blueprint('auth', __name__)
login_endpoint = "https://chotuve-grupo2-auth-server-dev.herokuapp.com/login/"

@bp.route('/login/', methods=["POST","GET"])
def login():
    username = request.form['username']
    password = request.form['password']
    response = requests.post(login_endpoint, json={"username":username,"password":password})
    if response.status_code == 200:
        return response.json(), 200
    else:
        return "BAD LOGIN", 400