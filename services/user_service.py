import requests
from exceptions.invalid_login import InvalidLogin, InvalidToken, NoFriendPending
from flask import current_app
from repositories import user_repository

auth_base_url = "https://chotuve-grupo2-auth-server-dev.herokuapp.com"
login_endpoint = f"{auth_base_url}/login/"
register_endpoint = f"{auth_base_url}/user/"
auth_endpoint = f"{auth_base_url}/auth/"

auth_header = "Basic YWxhZGRpbjpvcGVuc2VzYW1l"


def find_by_username(username):
    return user_repository.find_by_username(username)


def list_users(username=""):
    users = user_repository.list_users(username)
    if users is None:
        return []
    else:
        return [{"username": u.username} for u in users]


def send_request(contact_from, contact_to):
    contact_from.add_friend(contact_to)


def get_friend_requests(contact):
    return contact.pending_friends


def get_device_id(username):
    return user_repository.find_by_username(username).device_id


def set_device_id(username, device_id):
    user_repository.reset_device_id(device_id)
    user = user_repository.find_by_username(username)
    user.device_id = device_id
    user_repository.update_user(user)


def accept_request(contact_from, contact_accept):
    if contact_accept not in contact_from.pending_friends:
        raise NoFriendPending
    contact_from.accept_friend(contact_accept)


def get_friends(contact):
    return contact.all_friends


def are_friends(contact1, contact2):
    all_friends = contact1.all_friends
    return contact2 in all_friends
