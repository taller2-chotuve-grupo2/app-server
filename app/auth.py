from flask import Blueprint, current_app, json, jsonify, request
from exceptions.invalid_login import InvalidLogin, InvalidRegister

from services.auth_service import login_user, register_user
from services import auth_service
import requests
from flask_mail import Message
from app import mail

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
    try:
        json_request = request.get_json()
        if json_request == None:
            return "BAD LOGIN", 400
        else:
            username = json_request["username"]
            password = json_request["password"]
            email = json_request["email"]
            print(json_request)
            register_user(username, password, email)
            return "OK", 200
    except InvalidRegister as e:
        print(e)
        return "BAD REGISTER", 400


@bp.route("/profile/", methods=["GET"])
def profile():
    token = request.headers.get("authorization")
    try:
        user = auth_service.verify_token(token)
        current_app.logger.info(f"get profile for {user}")
        profile = auth_service.get_profile(user)
        # profile = {"username": user}
        current_app.logger.info(profile)

        profile = json.loads(profile)
        # print(profile2)

        return jsonify(profile), 200
    except BaseException as e:
        print(e)
        return "NO USERS", 400


@bp.route("/reset-password/", methods=["POST"])
def reset_password():
    try:
        json_request = request.get_json()
        new_password = auth_service.reset_password(json_request["username"])
        password = new_password["password"]
        current_app.logger.info("sending message")
        msg = Message(
            f"New Password {password}",
            sender="admin@chotuve.com",
            recipients=["juan.dambra@gmail.com"],
        )
        s = mail.send(msg)
        current_app.logger.info(s)
        return jsonify(new_password), 200
    except BaseException as e:
        current_app.logger.info(e)
        return "ERROR RESET PASSWORD", 400
