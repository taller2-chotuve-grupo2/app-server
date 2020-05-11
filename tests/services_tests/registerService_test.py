from unittest.mock import Mock, patch
from services.registerService import register_user
import requests


@patch('services.registerService.requests.post')
def test_login_service_status_200(mock_post):
    mock_post.return_value.ok = True
    mock_post.return_value.status_code = 200

    username = "RICHARDSON"
    password = "RICHARDSON"
    email = "RICH@RD.SON"
    response = register_user(username, password, email)
    assert response.status_code == 200

@patch('services.registerService.requests.post')
def test_login_service_bad_register(mock_post):
    mock_post.return_value.ok = True
    mock_post.return_value.status_code = 400

    username = "BAD_RICHARD"
    password = "BAD_RICHARD"
    email = "BAD.RICH@RD.SON"
    response = register_user(username, password, email)
    assert response.status_code == 400
