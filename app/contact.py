from flask import Blueprint, request, jsonify, current_app
from exceptions.invalid_login import InvalidLogin

from services import user_service
import requests

bp = Blueprint("contact", __name__)


@bp.route("/contact", methods=["GET"])
def new_contact():
    try:
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
