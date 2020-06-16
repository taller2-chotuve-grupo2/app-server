import requests
from exceptions.invalid_login import InvalidLogin, InvalidToken
from flask import current_app
from repositories import user_repository

auth_base_url = "https://chotuve-grupo2-auth-server-dev.herokuapp.com"
login_endpoint = f"{auth_base_url}/login/"
register_endpoint = f"{auth_base_url}/user/"
auth_endpoint = f"{auth_base_url}/auth/"

auth_header = "Basic YWxhZGRpbjpvcGVuc2VzYW1l"


def list_users(username):
    users = user_repository.list_users(username)
    return [u.as_dict() for u in users]
