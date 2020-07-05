from flask import Blueprint, request, jsonify, current_app
from exceptions.invalid_login import InvalidLogin

from services.auth_service import login_user, register_user
from services import auth_service
import requests

bp = Blueprint("auth", __name__)


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
    except InvalidLogin:
        return "BAD LOGIN", 400


@bp.route("/user/", methods=["POST"])
def register():
    current_app.logger.info("RIC")
    json_request = request.get_json()
    if json_request == None:
        return "BAD LOGIN", 400
    username = json_request["username"]
    password = json_request["password"]
    email = json_request["email"]
    try:
        register_ok = register_user(username, password, email)
        if register_ok:
            return "OK", 200
    except BaseException:
        return "BAD REGISTER", 400


@bp.route("/profile/", methods=["GET"])
def profile():
    token = request.headers.get("authorization")
    try:
        user = auth_service.verify_token(token)
        current_app.logger.info(f"get profile for {user}")
        # profile = auth_service.get_profile(user)
        # current_app.logger.info(profile)
        profile = {"username": user}
        return jsonify(profile), 200
    except BaseException as e:
        print(e)
        return "NO USERS", 400
