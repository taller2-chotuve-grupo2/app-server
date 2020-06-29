from unittest.mock import Mock, patch
from repositories import user_repository


@patch("services.auth_service.make_verify_request")
def test_get_all_contacts(mock_verify, client):
    user_repository.save_user("Ric")
    mock_verify.return_value.status_code = 200
    mock_verify.return_value.json.return_value = {"user": "Ric"}
    response = client.get("/contact")
    assert response.status_code == 200
    print(response)
