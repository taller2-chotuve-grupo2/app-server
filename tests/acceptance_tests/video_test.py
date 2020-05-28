from unittest.mock import Mock, patch


def test_upload_video_with_no_token(client):
    response = client.post("/video", follow_redirects=True)
    assert response.status_code == 403


@patch("services.video_service.make_upload_video_request")
@patch("services.auth_service.make_verify_request")
def test_upload_video_with_valid_token(mock_verify, mock_upload, client):
    mock_upload.return_value.status_code = 200
    mock_verify.return_value.status_code = 200
    mock_verify.return_value.json.return_value = {"username": "RIC"}
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTg5MDg3MDQyfQ.6g8IcVXhfJ7nSIWSodqhC-wbNnoWkEW3MEY4pdrbpMg"
    headers = {"Authorization": f"{token}"}
    data = {"title": "video1"}
    response = client.post(
        "/video",
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
    data = {
        "name": "nuevovideo.mp4",
        "path": "www.google.com",
        "size": "35M",
        "title": "Gran video de Ricson",
        "description": "Uno de los grandes videos de ricson",
        "location": "Ricland",
        "owner": "RICH",
        "visibility": "public",
    }
    mock_feed.return_value.json.return_value = {"videos": [data, data]}
    mock_verify.return_value.status_code = 200
    mock_verify.return_value.json.return_value = {"username": "RIC"}
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTg5MDg3MDQyfQ.6g8IcVXhfJ7nSIWSodqhC-wbNnoWkEW3MEY4pdrbpMg"
    headers = {"Authorization": f"{token}"}
    data = dict(title="video1")
    response = client.get(
        "/video",
        headers=headers,
        content_type="application/json",
        follow_redirects=True,
    )
    assert response.status_code == 200


@patch("services.video_service.make_get_video_request")
@patch("services.auth_service.make_verify_request")
def test_get_video_with_valid_token(mock_verify, mock_get_video, client):
    mock_verify.return_value.status_code = 200
    mock_verify.return_value.json.return_value = {"username": "RIC"}
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
