from unittest.mock import Mock, patch
from services.video_service import upload_video, get_feed
import requests
import pytest


@patch('services.video_service.make_upload_video_request')
def test_upload_video_service_status_200(mock_upload_request):
    mock_upload_request.return_value.status_code = 200

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
    upload_ok = upload_video(data)
    assert upload_ok == True



@patch('services.video_service.make_upload_video_request')
def test_upload_video_service_status_400(mock_upload_request):
    mock_upload_request.return_value.status_code = 400
    mock_upload_request.return_value.json.return_value = {"message": "Owner Required"}

    data = {
        "name": "nuevovideo.mp4",
        "path": "www.google.com",
        "size": "35M",
        "title": "Gran video de Ricson",
        "description": "Uno de los grandes videos de ricson",
        "location": "Ricland",
        "visibility": "public"
    }
    with pytest.raises(Exception):
        upload_video(data)

@patch('services.video_service.make_feed_request')
def test_get_feed_video_service_status_200(mock_feed_request):
    mock_feed_request.return_value.status_code = 200
    data = {
        "name": "nuevovideo.mp4",
        "path": "www.google.com",
        "size": "35M",
        "title": "Gran video de Ricson",
        "description": "Uno de los grandes videos de ricson",
        "location": "Ricland",
        "owner": "RICH",
        "visibility": "public"
    }

    mock_feed_request.return_value.json.return_value = {"videos": [data, data]}

    user = {
        "name":"ric",
        "id": "1"
    }
    
    videos = get_feed(user)
    assert videos == [data, data]

