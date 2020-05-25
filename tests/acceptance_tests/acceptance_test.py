from unittest.mock import Mock, patch

def test_home_page(client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = client.get('/')
    assert response.status_code == 200

def test_login_with_no_body(client):
    response = client.post('/login/')
    assert response.status_code == 400

@patch('services.authService.make_auth_request')
def test_login_with_right_args(mock_auth_request, client):
    
    mock_auth_request.return_value.status_code = 201
    mock_auth_request.return_value.json.return_value = {"token":"123"}
    response = client.post('/login', json={"username":'admin',"password":'admin'},
                                follow_redirects=True)

    assert response.status_code == 200
    assert response.json["token"] == "123"

def test_register_with_no_body(client):
    response = client.post('/user/')
    assert response.status_code == 400

def test_register_with_username_already_in_use(client):
    response = client.post('/user',data=dict(username='admin', password='admin'),
                                follow_redirects=True)
    assert response.status_code == 400    
