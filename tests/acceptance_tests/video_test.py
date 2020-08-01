from unittest.mock import Mock, patch
from tests import fakedata


@patch("services.auth_service.make_verify_request")
def test_upload_video_with_no_token(mock_verify, client):
    mock_verify.return_value.status_code = 400
    response = client.post("/video/")
    assert response.status_code == 403


@patch("services.video_service.make_upload_video_request")
@patch("services.auth_service.make_verify_request")
def test_upload_video_with_valid_token(mock_verify, mock_upload, client):
    mock_upload.return_value.status_code = 200
    mock_upload.return_value.json.return_value = {"id": "RIC"}
    mock_verify.return_value.status_code = 200
    mock_verify.return_value.json.return_value = {"user": "RIC"}
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTg5MDg3MDQyfQ.6g8IcVXhfJ7nSIWSodqhC-wbNnoWkEW3MEY4pdrbpMg"
    headers = {"Authorization": f"{token}"}
    data = {"title": "video1"}
    response = client.post(
        "/video/",
        headers=headers,
        content_type="application/json",
        json=data,
        follow_redirects=True,
    )
    assert response.status_code == 200


@patch("services.video_service.make_feed_request")
@patch("services.auth_service.make_verify_request")
def test_get_feed_with_valid_token(mock_verify, mock_feed, client):
    mock_feed.return_value.status_code = 200
    data = fakedata.feed
    mock_feed.return_value.json.return_value = data
    mock_verify.return_value.status_code = 200
    mock_verify.return_value.json.return_value = {"user": "RIC"}
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTg5MDg3MDQyfQ.6g8IcVXhfJ7nSIWSodqhC-wbNnoWkEW3MEY4pdrbpMg"
    headers = {"Authorization": f"{token}"}
    response = client.get(
        "/video/",
        headers=headers,
        content_type="application/json",
        follow_redirects=True,
    )
    assert response.status_code == 200


@patch("services.video_service.make_feed_request")
@patch("services.auth_service.make_verify_request")
def test_get_feed_with_invalid_token(mock_verify, mock_feed, client):
    mock_verify.return_value.status_code = 400
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTg5MDg3MDQyfQ.6g8IcVXhfJ7nSIWSodqhC-wbNnoWkEW3MEY4pdrbpMg"
    headers = {"Authorization": f"{token}"}
    data = dict(title="video1")
    response = client.get(
        "/video/",
        headers=headers,
        content_type="application/json",
        follow_redirects=True,
    )
    assert response.status_code == 403


@patch("services.video_service.make_get_video_request")
@patch("services.auth_service.make_verify_request")
def test_get_video_with_valid_token(mock_verify, mock_get_video, client):
    mock_verify.return_value.status_code = 200
    mock_verify.return_value.json.return_value = {"user": "RIC"}
    mock_get_video.return_value.status_code = 200
    data = {
        "id": "12",
        "name": "nuevovideo.mp4",
        "path": "www.google.com",
        "size": "35M",
        "title": "Gran video de Ricson",
        "description": "Uno de los grandes videos de ricson",
        "location": "Ricland",
        "owner": "RICH",
        "visibility": "public",
    }
    mock_get_video.return_value.json.return_value = {"video": data}
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTg5MDg3MDQyfQ.6g8IcVXhfJ7nSIWSodqhC-wbNnoWkEW3MEY4pdrbpMg"
    headers = {"Authorization": f"{token}"}
    response = client.get(
        "/video/12",
        headers=headers,
        content_type="application/json",
        follow_redirects=True,
    )
    assert response.status_code == 200


@patch("services.video_service.make_feed_request")
@patch("services.auth_service.make_verify_request")
def test_get_video_id_with_invalid_token(mock_verify, mock_feed, client):
    mock_verify.return_value.status_code = 400
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTg5MDg3MDQyfQ.6g8IcVXhfJ7nSIWSodqhC-wbNnoWkEW3MEY4pdrbpMg"
    headers = {"Authorization": f"{token}"}
    data = dict(title="video1")
    response = client.get(
        "/video/12",
        headers=headers,
        content_type="application/json",
        follow_redirects=True,
    )
    assert response.status_code == 403


@patch("services.video_service.make_post_comment_request")
@patch("services.auth_service.make_verify_request")
def test_post_comment_with_valid_token(mock_verify, mock_post_comment, client):
    mock_verify.return_value.status_code = 200
    mock_verify.return_value.json.return_value = {"user": "RIC"}
    mock_post_comment.return_value.status_code = 200
    data = {"message": "Un mensaje cualquiera"}
    mock_post_comment.return_value.json.return_value = data
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTg5MDg3MDQyfQ.6g8IcVXhfJ7nSIWSodqhC-wbNnoWkEW3MEY4pdrbpMg"
    headers = {"Authorization": f"{token}"}
    response = client.post(
        "/video/12/comment",
        headers=headers,
        content_type="application/json",
        json=data,
        follow_redirects=True,
    )
    assert response.status_code == 200


@patch("services.video_service.make_post_reaction_request")
@patch("services.auth_service.make_verify_request")
def test_post_reaction_with_valid_token(mock_verify, mock_post_reaction, client):
    mock_verify.return_value.status_code = 200
    mock_verify.return_value.json.return_value = {"user": "RIC"}
    mock_post_reaction.return_value.status_code = 200
    data = {"message": "Me gusta"}
    mock_post_reaction.return_value.json.return_value = data
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTg5MDg3MDQyfQ.6g8IcVXhfJ7nSIWSodqhC-wbNnoWkEW3MEY4pdrbpMg"
    headers = {"Authorization": f"{token}"}
    response = client.post(
        "/video/12/reaction",
        headers=headers,
        content_type="application/json",
        json=data,
        follow_redirects=True,
    )
    assert response.status_code == 200


@patch("services.video_service.make_get_video_reactions_request")
@patch("services.auth_service.make_verify_request")
def test_get_reaction_with_valid_token(mock_verify, mock_get_video_reaction, client):
    mock_verify.return_value.status_code = 200
    mock_verify.return_value.json.return_value = {"user": "RIC"}
    mock_get_video_reaction.return_value.status_code = 200
    data = {"status": "Me gusta"}
    mock_get_video_reaction.return_value.json.return_value = data
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTg5MDg3MDQyfQ.6g8IcVXhfJ7nSIWSodqhC-wbNnoWkEW3MEY4pdrbpMg"
    headers = {"Authorization": f"{token}"}
    response = client.get(
        "/video/12/reaction",
        headers=headers,
        content_type="application/json",
        follow_redirects=True,
    )
    assert response.status_code == 200


@patch("services.video_service.make_feed_request")
@patch("services.auth_service.make_verify_request")
def test_get_video_by_user_with_valid_token(mock_verify, mock_get_feed, client):
    mock_verify.return_value.status_code = 200
    mock_verify.return_value.json.return_value = {"user": "Rich"}
    mock_get_feed.return_value.status_code = 200
    data = {
        "id": "37bfb94e-8a2a-4bfa-8d42-5f1c44fa7dbb",
        "owner": "admin1005",
        "createdAt": "2020-07-19T04:01:37.037Z",
        "thumbnail": "asd",
        "title": "un video",
        "likesCount": 1,
        "dislikesCount": 0,
        "commentsCount": 1,
    }
    video_data = [data]
    mock_get_feed.return_value.json.return_value = video_data
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTg5MDg3MDQyfQ.6g8IcVXhfJ7nSIWSodqhC-wbNnoWkEW3MEY4pdrbpMg"
    headers = {"Authorization": f"{token}"}
    username = "Ricson"
    response = client.get(
        f"/video/user/{username}",
        headers=headers,
        content_type="application/json",
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert response.json == video_data
