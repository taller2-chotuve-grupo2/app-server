from unittest.mock import Mock, patch
from repositories import user_repository


@patch("services.auth_service.make_verify_request")
def test_get_all_contacts(mock_verify, client):
    mock_verify.return_value.status_code = 200
    mock_verify.return_value.json.return_value = {"user": "Rich"}
    response = client.get("/contact")
    assert response.status_code == 200
    print(response)
    user_lists = response.json
    assert {"username": "Rich"} in user_lists


@patch("services.auth_service.make_verify_request")
def test_get_contacts_query(mock_verify, client):
    mock_verify.return_value.status_code = 200
    mock_verify.return_value.json.return_value = {"user": "Rich"}
    response = client.get("/contact?username=ric")
    assert response.status_code == 200
    print(response)
    user_lists = response.json
    assert {"username": "Rich"} in user_lists


@patch("services.auth_service.make_verify_request")
def test_new_contact(mock_verify, client):
    mock_verify.return_value.status_code = 200
    mock_verify.return_value.json.return_value = {"user": "Roc"}
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTg5MDg3MDQyfQ.6g8IcVXhfJ7nSIWSodqhC-wbNnoWkEW3MEY4pdrbpMg"
    headers = {"Authorization": f"{token}"}
    data = {"username": "Ricson"}
    response = client.post(
        "/contact/",
        headers=headers,
        content_type="application/json",
        json=data,
        follow_redirects=True,
    )
    assert response.status_code == 200


@patch("services.auth_service.make_verify_request")
def test_get_pending_requests(mock_verify, client):
    mock_verify.return_value.status_code = 200
    mock_verify.return_value.json.return_value = {"user": "Roc"}
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTg5MDg3MDQyfQ.6g8IcVXhfJ7nSIWSodqhC-wbNnoWkEW3MEY4pdrbpMg"
    headers = {"Authorization": f"{token}"}
    response = client.get("/contact/pending", headers=headers, follow_redirects=True,)
    assert response.status_code == 200
    user_lists = response.json
    assert {"username": "Rich"} in user_lists
