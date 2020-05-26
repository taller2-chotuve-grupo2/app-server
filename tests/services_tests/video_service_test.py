from unittest.mock import Mock, patch
from services.videoService import upload_video, get_feed
import requests


@patch('services.videoService.requests.post')
def test_upload_video_service_status_200(mock_post):
    mock_post.return_value.ok = True
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.resourceId = "123"

    data = {
        "name": "nuevovideo.mp4",
        "path": "www.google.com",
        "size": "35M",
        "owner": "1",
        "title": "Gran video de Ricson",
        "description": "Uno de los grandes videos de ricson",
        "location": "Ricland",
        "visibility": "public"
    }
    response = upload_video(data)
    assert response.status_code == 200
    assert response.json.resourceId == "123"



@patch('services.videoService.requests.post')
def test_upload_video_service_status_400(mock_post):
    mock_post.return_value.ok = True
    mock_post.return_value.status_code = 400
    mock_post.return_value.json.message = "No Owner Provided"

    data = {
        "name": "nuevovideo.mp4",
        "path": "www.google.com",
        "size": "35M",
        "title": "Gran video de Ricson",
        "description": "Uno de los grandes videos de ricson",
        "location": "Ricland",
        "visibility": "public"
    }
    
    response = upload_video(data)
    assert response.status_code == 400
    assert response.json.message == "No Owner Provided"




@patch('services.videoService.requests.get')
def test_get_feed_video_service_status_200(mock_get):
    data = {
        "name": "nuevovideo.mp4",
        "path": "www.google.com",
        "size": "35M",
        "title": "Gran video de Ricson",
        "description": "Uno de los grandes videos de ricson",
        "location": "Ricland",
        "visibility": "public"
    }

    user = {
        "name":"ric",
        "id": "1"
    }
    mock_get.return_value.ok = True
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.videos = [data, data]
    
    response = get_feed(user)
    assert response.status_code == 200
    assert response.json.videos == [data, data]


# @patch('services.auth_service.requests.post')
# def test_login_service_bad_register(mock_post):
#     mock_post.return_value.ok = True
#     mock_post.return_value.status_code = 400

#     username = "BAD_RICHARD"
#     password = "BAD_RICHARD"
#     email = "BAD.RICH@RD.SON"
#     response = register_user(username, password, email)
#     assert response.status_code == 400



# @patch('services.auth_service.requests.post')
# def test_login_service_status_200(mock_post):
#     mock_post.return_value.ok = True
#     mock_post.return_value.status_code = 200

#     username = "RICHARD"
#     password = "RICHARD"
#     response = login_user(username, password)
#     assert response.status_code == 200

# @patch('services.auth_service.requests.post')
# def test_login_service_returns_token(mock_post):

#     token = {
#         "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IlJJQ0hBUkRTRU4ifQ.Kka0x85is4xhH7e2CvxbMy8SYMwgIF7DISqgZBfYfKI"
#     }
#     mock_post.return_value.ok = True
#     mock_post.return_value.status_code = 200
#     mock_post.return_value.json.return_value = token

#     username = "RICHARD"
#     password = "RICHARD"
#     response = login_user(username, password)
#     print(response.status_code)
#     print(response.json())
#     assert response.json() == token

# @patch('services.auth_service.requests.post')
# def test_login_service_bad_login(mock_post):
#     mock_post.return_value.ok = True
#     mock_post.return_value.status_code = 400

#     username = "BAD_RICHARD"
#     password = "BAD_RICHARD"
#     response = login_user(username, password)
#     assert response.status_code == 400
