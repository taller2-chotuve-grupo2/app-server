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
