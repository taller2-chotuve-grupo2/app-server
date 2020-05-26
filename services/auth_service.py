import requests
from exceptions.invalid_login import InvalidLogin

auth_base_url = "https://chotuve-grupo2-auth-server-dev.herokuapp.com"
login_endpoint = f"{auth_base_url}/login/"
register_endpoint = f"{auth_base_url}/user/"
auth_endpoint = f"{auth_base_url}/auth/"


def make_auth_request(username, password):
    return requests.post(
        login_endpoint,
        headers={"authorization": "Basic YWxhZGRpbjpvcGVuc2VzYW1l"},
        json={"username": username, "password": password},
    )


def make_register_request(username, password, email):
    response = requests.post(
        register_endpoint,
        headers={"authorization": "Basic YWxhZGRpbjpvcGVuc2VzYW1l"},
        json={"username": username, "password": password, "email": email},
    )
    return response


def make_verify_request(token):
    response = requests.post(
        auth_endpoint,
        headers={"authorization": "Basic YWxhZGRpbjpvcGVuc2VzYW1l"},
        json={"token": token},
    )
    return response


def login_user(username, password):
    """
        Login User must return a Token
    """
    response = make_auth_request(username, password)
    if response.status_code == 201:
        return response.json()["token"]
    else:
        raise InvalidLogin


def register_user(username, password, email):
    response = make_register_request(username, password, email)
    if response.status_code == 200:
        return True
    else:
        raise BaseException


def verify_token(token):
    response = make_verify_request(token)
    if response.status_code == 200:
        return response.json()["username"]
    else:
        raise BaseException
