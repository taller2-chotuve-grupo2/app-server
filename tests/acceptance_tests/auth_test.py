from unittest.mock import Mock, patch
from app.models import User


def test_home_page(client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = client.get("/")
    assert response.status_code == 200


def test_login_with_no_body(client):
    response = client.post("/login/")
    assert response.status_code == 400


@patch("services.auth_service.make_auth_request")
def test_login_with_right_args(mock_auth_request, client):
    mock_auth_request.return_value.status_code = 200
    mock_auth_request.return_value.json.return_value = {"token": "123"}
    response = client.post(
        "/login/", json={"username": "admin", "password": "admin"}, follow_redirects=True
    )
    assert response.status_code == 200
    assert response.json["token"] == "123"


@patch("services.auth_service.make_register_request")
def test_register_with_no_body(mock_register_request, client):
    mock_register_request.return_value.status_code = 400
    response = client.post("/user/")
    assert response.status_code == 400


@patch("services.auth_service.make_register_request")
def test_register_with_username_already_in_use(mock_register_request, client):
    mock_register_request.return_value.status_code = 400
    response = client.post(
        "/user/", data=dict(username="admin", password="admin"), follow_redirects=True
    )
    assert response.status_code == 400


@patch("services.auth_service.make_register_request")
def test_register_with_right_args(mock_register_request, client):
    mock_register_request.return_value.status_code = 200
    response = client.post(
        "/user/",
        json={"username": "adminadmin", "password": "admin", "email": "test@test.com"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    # user = User.query.filter_by(username="adminadmin").first()
    # assert user.username == "adminadmin"
