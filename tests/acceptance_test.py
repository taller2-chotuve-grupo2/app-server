def test_home_page(client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    # print(client.__dict__)    
    response = client.get('/')
    assert response.status_code == 200

def test_login_with_no_body(client):
    response = client.post('/login/')
    assert response.status_code == 400


def test_login_with_right_args(client):
    response = client.post('/login', json={"username":'admin',"password":'admin'},
                                follow_redirects=True)
    assert response.status_code == 200


def test_register_with_no_body(client):
    response = client.post('/user/')
    assert response.status_code == 400

def test_register_with_username_already_in_use(client):
    response = client.post('/user',data=dict(username='admin', password='admin'),
                                follow_redirects=True)
    assert response.status_code == 400    

def test_upload_video_with_no_token(client):
    response = client.post('/upload', follow_redirects=True)
    assert response.status_code == 403


def test_upload_video_with_valid_token(client):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTg5MDg3MDQyfQ.6g8IcVXhfJ7nSIWSodqhC-wbNnoWkEW3MEY4pdrbpMg"
    headers = {
        'Authorization': '{}'.format(token)
    }
    response = client.post('/upload', headers=headers, follow_redirects=True)
    assert response.status_code == 201

