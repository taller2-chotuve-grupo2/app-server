from unittest.mock import Mock, patch
from services import user_service

# from exceptions.invalid_login import InvalidLogin
from repositories import user_repository
import pytest
import requests


def test_new_contact_request():
    contact1 = user_repository.save_user("Ric")
    contact2 = user_repository.save_user("Charles")
    user_service.send_request(contact1, contact2)
    friend_requests = user_service.get_friend_requests(contact2)
    assert len(friend_requests) == 1


def test_new_send_request_only_adds_one_contact_request():
    contact1 = user_repository.save_user("Ric")
    contact2 = user_repository.save_user("Charles")
    user_service.send_request(contact1, contact2)
    user_service.send_request(contact1, contact2)
    friend_requests = user_service.get_friend_requests(contact2)
    assert len(friend_requests) == 1


def test_accept_contact_request():
    contact1 = user_repository.save_user("Ric")
    contact2 = user_repository.save_user("Charles")
    user_service.send_request(contact1, contact2)
    user_service.send_request(contact1, contact2)
    friend_requests = user_service.get_friend_requests(contact2)
    assert len(friend_requests) == 1
    user_service.accept_request(contact2, contact1)
    friend_requests = user_service.get_friend_requests(contact2)
    assert len(friend_requests) == 0
    friends_contact2 = user_service.get_friends(contact2)
    assert len(friends_contact2) == 1
    assert contact1 in friends_contact2
    friends_contact1 = user_service.get_friends(contact1)
    assert len(friends_contact1) == 1
    assert contact2 in friends_contact1


def test_list_available_users():
    contact2 = user_repository.save_user("Charles")
    user_list = user_service.list_users()
    assert len(user_list) == 4
    user_list = user_service.list_users("Charles")
    assert len(user_list) == 1
