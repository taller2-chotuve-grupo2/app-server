from flask import Blueprint, request, jsonify, current_app
from exceptions.invalid_login import InvalidLogin
from services import user_service, auth_service
import requests

bp = Blueprint("contact", __name__)


@bp.route("/contact", methods=["GET"])
def list_contacts():
    token = request.headers.get("authorization")
    try:
        user = auth_service.verify_token(token)
        username = request.args.get("username")
        current_app.logger.info(f"Contact Search:: Username {username}")
        if username is None:
            username = ""
        users = user_service.list_users(username)
        current_app.logger.info(users)
        return jsonify(users), 200
    except BaseException as e:
        print(e)
        return "NO USERS", 400


@bp.route("/contact/", methods=["POST"])
def new_contact():
    token = request.headers.get("authorization")
    try:
        user = auth_service.verify_token(token)
        contact_data = request.json
        current_app.logger.info(
            f"Contact Request:: Username {user} wants to friend {contact_data['username']}"
        )
        contact_from = user_service.find_by_username(user)
        contact_to = user_service.find_by_username(contact_data["username"])
        user_service.send_request(contact_from, contact_to)
        return "OK", 200
    except BaseException as e:
        print(e)
        return "NO USERS", 400
