from flask import Blueprint, request
from services.loginService import login_user
import requests

bp = Blueprint('auth', __name__)
login_endpoint = "https://chotuve-grupo2-auth-server-dev.herokuapp.com/login/"
register_endpoint = "https://chotuve-grupo2-auth-server-dev.herokuapp.com/user/"

@bp.route('/login/', methods=["POST","GET"])
def login():
    json_request = request.get_json()
    if json_request == None:
        return "BAD LOGIN", 400
    username = json_request['username']
    password = json_request['password']
    response = login_user(username, password)
    if response.status_code == 200:
        return response.json(), 200
    else:
        return "BAD LOGIN", 400

@bp.route('/user/', methods=["POST"])
def register():
    json_request = request.get_json()
    if json_request == None:
        return "BAD LOGIN", 400
    username = json_request['username']
    password = json_request['password']
    email = json_request['email']
    print(username, password, email)
    response = requests.post(register_endpoint, headers={'authorization': 'Basic YWxhZGRpbjpvcGVuc2VzYW1l'}, json={"username":username,"password":password,"email":email})
    if response.status_code == 200:
        return 'OK', 200
    else:
        return response.json(), 400
