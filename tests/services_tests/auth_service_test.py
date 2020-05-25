from unittest.mock import Mock, patch
from services.authService import register_user, login_user
from exceptions.invalid_login import InvalidLogin
import pytest
import requests


@patch('services.authService.requests.post')
def test_login_service_status_200(mock_post):
    mock_post.return_value.ok = True
    mock_post.return_value.status_code = 200

    username = "RICHARDSON"
    password = "RICHARDSON"
    email = "RICH@RD.SON"
    response = register_user(username, password, email)
    assert response.status_code == 200

@patch('services.authService.requests.post')
def test_login_service_bad_register(mock_post):
    mock_post.return_value.ok = True
    mock_post.return_value.status_code = 400

    username = "BAD_RICHARD"
    password = "BAD_RICHARD"
    email = "BAD.RICH@RD.SON"
    response = register_user(username, password, email)
    assert response.status_code == 400


@patch('services.authService.make_auth_request')
def test_login_service_returns_token(mock_auth_request):
    mock_auth_request.return_value.status_code = 201
    mock_auth_request.return_value.json.return_value = {"token":"123"}

    username = "RICHARD"
    password = "RICHARD"
    token = login_user(username, password)
    assert token == "123"

@patch('services.authService.make_auth_request')

def test_login_service_bad_login(mock_auth_request):
    mock_auth_request.return_value.status_code = 400

    username = "BAD_RICHARD"
    password = "BAD_RICHARD"
    with pytest.raises(InvalidLogin):
        login_user(username, password)
