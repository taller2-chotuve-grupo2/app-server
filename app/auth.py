from flask import Blueprint, current_app, json, jsonify, request
from exceptions.invalid_login import InvalidLogin, InvalidRegister

from services.auth_service import login_user, register_user
from services import auth_service, user_service
import requests
from flask_mail import Message
from app import mail

# Firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

import os
from os import environ

bp = Blueprint("auth", __name__)

if environ.get('FIREBASE_PROJECT_ID') is not None:
    # Instantiate Firebase app
    firebase_credentials = {
        "type": "service_account",
        "project_id": os.environ['FIREBASE_PROJECT_ID'],
        "private_key": os.environ['FIREBASE_PRIVATE_KEY'].replace('\\n', '\n'),
        "client_email": os.environ['FIREBASE_CLIENT_EMAIL'],
        "token_uri": os.environ['FIREBASE_TOKEN_URI']
    }
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred)

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

        # Reset user's password on Firebase
        current_app.logger.info("Resetting password for user on Firebase")

        email = json_request["username"] + "@chotuve.com" # FIXME: obtener el email a partir del username
        user = auth.get_user_by_email(email)
        current_app.logger.debug('Successfully fetched user data: {0}'.format(user.uid))
        user = auth.update_user(user.uid,
            password=response["newPassword"])
        current_app.logger.debug('Sucessfully updated user: uuid={0} - username={1} - email={2}'.format(user.uid, json_request["username"], email))

        return "EMAIL SENT", 200
    except BaseException as e:
        current_app.logger.error(e)
        return "ERROR RESET PASSWORD", 400
