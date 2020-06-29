import requests
from exceptions.invalid_login import InvalidLogin, InvalidToken
from flask import current_app
from repositories import user_repository

auth_base_url = "https://chotuve-grupo2-auth-server-dev.herokuapp.com"
login_endpoint = f"{auth_base_url}/login/"
register_endpoint = f"{auth_base_url}/user/"
auth_endpoint = f"{auth_base_url}/auth/"

auth_header = "Basic YWxhZGRpbjpvcGVuc2VzYW1l"


def list_users(username=""):
    users = user_repository.list_users(username)
    if users is None:
        return []
    else:
        # return [u.as_dict() for u in users]
        return users


def send_request(contact_from, contact_to):
    contact_from.add_friend(contact_to)


def get_friend_requests(contact):
    return contact.pending_friends


def accept_request(contact_from, contact_accept):
    contact_from.accept_friend(contact_accept)


def get_friends(contact):
    return contact.all_friends
