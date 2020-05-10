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
    response = client.post('/login',data=dict(username='admin', password='admin'),
                                follow_redirects=True)
    assert response.status_code == 200

def test_upload_video_with_no_token(client):
    response = client.post('/upload', follow_redirects=True)
    assert response.status_code == 403
