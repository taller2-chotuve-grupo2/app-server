from unittest.mock import Mock, patch
from services.videoService import upload_video
import requests


@patch('services.videoService.requests.post')
def test_upload_video_service_status_200(mock_post):
    mock_post.return_value.ok = True
    mock_post.return_value.status_code = 200
    
    data = {
        "title": "VIDEO1"
    }
    response = upload_video(data)
    assert response.status_code == 200

# @patch('services.authService.requests.post')
# def test_login_service_bad_register(mock_post):
#     mock_post.return_value.ok = True
#     mock_post.return_value.status_code = 400

#     username = "BAD_RICHARD"
#     password = "BAD_RICHARD"
#     email = "BAD.RICH@RD.SON"
#     response = register_user(username, password, email)
#     assert response.status_code == 400



# @patch('services.authService.requests.post')
# def test_login_service_status_200(mock_post):
#     mock_post.return_value.ok = True
#     mock_post.return_value.status_code = 200

#     username = "RICHARD"
#     password = "RICHARD"
#     response = login_user(username, password)
#     assert response.status_code == 200

# @patch('services.authService.requests.post')
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

# @patch('services.authService.requests.post')
# def test_login_service_bad_login(mock_post):
#     mock_post.return_value.ok = True
#     mock_post.return_value.status_code = 400

#     username = "BAD_RICHARD"
#     password = "BAD_RICHARD"
#     response = login_user(username, password)
#     assert response.status_code == 400
