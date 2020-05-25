from flask import Blueprint, request, jsonify

from services.authService import login_user, register_user
import requests

bp = Blueprint("auth", __name__)
login_endpoint = "https://chotuve-grupo2-auth-server-dev.herokuapp.com/login/"
register_endpoint = "https://chotuve-grupo2-auth-server-dev.herokuapp.com/user/"


@bp.route("/login/", methods=["POST", "GET"])
def login():
    json_request = request.get_json()
    if json_request == None:
        return "BAD LOGIN", 400
    username = json_request["username"]
    password = json_request["password"]
    try:
        token = login_user(username, password)
        return jsonify({"token": token}), 200
    # except InvalidLoginException:
    except Exception:
        return "BAD LOGIN", 400

    # if response.status_code == 200:
    #     return response.json(), 200
    # else:
    #     return "BAD LOGIN", 400


@bp.route("/user/", methods=["POST"])
def register():
    json_request = request.get_json()
    if json_request == None:
        return "BAD LOGIN", 400
    username = json_request["username"]
    password = json_request["password"]
    email = json_request["email"]
    response = register_user(username, password, email)
    if response.status_code == 200:
        return "OK", 200
    else:
        return response.json(), 400
