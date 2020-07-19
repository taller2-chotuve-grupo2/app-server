from flask import Blueprint, current_app, json, jsonify, request
from exceptions.invalid_login import InvalidLogin, InvalidRegister

from services.auth_service import login_user, register_user
from services import auth_service, user_service
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
    device_id = None
    if "device_id" in json_request:
        device_id = json_request["device_id"]
    try:
        response = login_user(username, password)
        user_service.set_device_id(response["username"], device_id)
        return jsonify({"token": response["token"]}), 200
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


@bp.route("/user/<id>/deviceid", methods=["DELETE"])
def delete_device_id(id):
    current_app.logger.info(f"Delete device id for user {id}")
    try:
        json_request = request.get_json()
        if json_request == None:
            return "BAD LOGIN", 400
        else:
            username = json_request["username"]
            password = json_request["password"]
            email = json_request["email"]
            register_user(username, password, email)
            return "OK", 200
    except InvalidRegister as e:
        print(e)
        return "BAD REGISTER", 400


@bp.route("/profile/", methods=["GET"])
def profile():
    token = request.headers.get("authorization")
    try:
        if "username" in request.args:
            user = request.args.get("username")
        else:
            user = auth_service.verify_token(token)
        current_app.logger.info(f"get profile for {user}")
        profile = auth_service.get_profile(user)
        current_app.logger.info(profile)

        profile["device_id"] = user_service.get_device_id(user)

        return jsonify(profile), 200
    except BaseException as e:
        print(e)
        return "NO USERS", 400


@bp.route("/profile/", methods=["POST"])
def update_profile():
    token = request.headers.get("authorization")
    try:
        user = auth_service.verify_token(token)
        current_app.logger.info(f"post profile for {user}")
        profileData = request.get_json()
        profile = auth_service.post_profile(user, profileData)
        return jsonify(profile), 200
    except BaseException as e:
        print(e)
        return "NO USERS", 400


@bp.route("/reset-password/", methods=["POST"])
def reset_password():
    try:
        json_request = request.get_json()
        response = auth_service.reset_password(json_request["username"])
        current_app.logger.info(response)
        password = response["newPassword"]
        current_app.logger.info("sending message")
        msg = Message(
            f"Your new Password is: '{password}'",
            sender="ric@chotuve.com",
            recipients=["juan.dambra@gmail.com", response["email"]],
        )
        s = mail.send(msg)
        current_app.logger.info(s)
        return "EMAIL SENT", 200
    except BaseException as e:
        current_app.logger.error(e)
        return "ERROR RESET PASSWORD", 400
