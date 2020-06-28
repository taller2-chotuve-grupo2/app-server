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
