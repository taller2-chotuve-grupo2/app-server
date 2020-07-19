import requests
from exceptions.invalid_login import InvalidLogin, InvalidToken, InvalidRegister
from flask import current_app
from repositories import user_repository

auth_base_url = "https://chotuve-grupo2-auth-server-dev.herokuapp.com"
login_endpoint = f"{auth_base_url}/login/"
reset_password_endpoint = f"{auth_base_url}/reset-password/"
register_endpoint = f"{auth_base_url}/user/"
auth_endpoint = f"{auth_base_url}/auth/"


def get_video_endpoint(username):
    return f"{auth_base_url}/user/{username}"


auth_header = "Basic YWxhZGRpbjpvcGVuc2VzYW1l"


def make_auth_request(username, password):
    return requests.post(
        login_endpoint,
        headers={"authorization": auth_header},
        json={"username": username, "password": password},
    )


def make_reset_password_request(username):
    return requests.post(
        reset_password_endpoint,
        headers={"authorization": auth_header},
        json={"username": username},
    )


def make_register_request(username, password, email):
    response = requests.post(
        register_endpoint,
        headers={"authorization": auth_header},
        json={"username": username, "password": password, "email": email},
    )
    return response


def make_verify_request(token):
    response = requests.post(
        auth_endpoint, headers={"authorization": auth_header}, json={"token": token},
    )
    return response


def make_profile_request(username):
    response = requests.get(
        get_video_endpoint(username), headers={"authorization": auth_header}
    )
    return response


def login_user(username, password):
    """
        Login User must return a Token
    """
    response = make_auth_request(username, password)
    # current_app.logger.info(response.json()["token"])
    if response.status_code == 200:
        return response.json()
    else:
        raise InvalidLogin


def register_user(username, password, email):
    response = make_register_request(username, password, email)
    if response.status_code == 200:
        user_repository.save_user(username)
        return True
    else:
        raise InvalidRegister


def verify_token(token):
    response = make_verify_request(token)
    if response.status_code == 200:
        return response.json()["user"]
    else:
        raise InvalidToken


def get_profile(username):
    response = make_profile_request(username)
    if response.status_code == 200:
        return response.json()
    else:
        raise InvalidToken


def reset_password(username):
    response = make_reset_password_request(username)
    if response.status_code == 200:
        return response.json()
    else:
        raise InvalidToken
