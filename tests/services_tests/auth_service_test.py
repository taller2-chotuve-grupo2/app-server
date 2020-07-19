from unittest.mock import Mock, patch
from services.auth_service import register_user, login_user
from exceptions.invalid_login import InvalidLogin
import pytest
import requests


@patch("services.auth_service.make_register_request")
def test_register_service_status_200(mock_post):
    mock_post.return_value.ok = True
    mock_post.return_value.status_code = 200

    username = "RICHARDSON"
    password = "RICHARDSON"
    email = "RICH@RD.SON"
    register_ok = register_user(username, password, email)
    assert register_ok == True


@patch("services.auth_service.make_register_request")
def test_register_service_bad_register(mock_post):
    mock_post.return_value.ok = True
    mock_post.return_value.status_code = 400

    username = "BAD_RICHARD"
    password = "BAD_RICHARD"
    email = "BAD.RICH@RD.SON"
    with pytest.raises(BaseException):
        register_user(username, password, email)


@patch("services.auth_service.make_auth_request")
def test_login_service_returns_token(mock_auth_request):
    mock_auth_request.return_value.status_code = 200
    mock_auth_request.return_value.json.return_value = {
        "token": "123",
        "username": "Ric",
    }

    username = "RICHARD"
    password = "RICHARD"
    obj = login_user(username, password)
    assert obj["token"] == "123"
    assert obj["username"] == "Ric"


@patch("services.auth_service.make_auth_request")
def test_login_service_bad_login(mock_auth_request):
    mock_auth_request.return_value.status_code = 400

    username = "BAD_RICHARD"
    password = "BAD_RICHARD"
    with pytest.raises(InvalidLogin):
        login_user(username, password)
