from unittest.mock import Mock, patch
from services import video_service
import requests
import pytest


@patch("services.video_service.make_upload_video_request")
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
        "visibility": "public",
    }
    upload_ok = video_service.upload_video(data)
    assert upload_ok == True


@patch("services.video_service.make_upload_video_request")
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
        "visibility": "public",
    }
    with pytest.raises(BaseException):
        video_service.upload_video(data)


@patch("services.video_service.make_feed_request")
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
        "visibility": "public",
    }

    mock_feed_request.return_value.json.return_value = [data, data]

    user = {"name": "ric", "id": "1"}

    videos = video_service.get_feed(user)
    assert videos == [data, data]


@patch("services.video_service.make_get_video_request")
def test_get_video_service_status_200(mock_get_video_request):
    mock_get_video_request.return_value.status_code = 200
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

    mock_get_video_request.return_value.json.return_value = {"video": data}

    videos = video_service.get_video("12")
    assert videos == data


@patch("services.video_service.make_get_video_request")
def test_get_video_service_status_400(mock_get_video_request):
    mock_get_video_request.return_value.status_code = 400
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

    with pytest.raises(BaseException):
        videos = video_service.get_video("12")


@patch("services.video_service.make_post_comment_request")
def test_post_comment_service_status_200(mock_upload_request):
    mock_upload_request.return_value.status_code = 200

    data = {
        "message": "un comentario cualquiera",
    }

    upload_ok = video_service.post_comment(12, data)
    assert upload_ok == True


@patch("services.video_service.make_post_comment_request")
def test_post_comment_service_status_400(mock_upload_request):
    mock_upload_request.return_value.status_code = 400

    data = {
        "message": "un comentario cualquiera",
    }

    with pytest.raises(BaseException):
        upload_ok = video_service.post_comment(12, data)


@patch("services.video_service.make_post_reaction_request")
def test_post_reaction_service_status_200(mock_upload_request):
    mock_upload_request.return_value.status_code = 200

    data = {
        "message": "un comentario cualquiera",
    }

    upload_ok = video_service.post_reaction(12, data)
    assert upload_ok == True


@patch("services.video_service.make_post_reaction_request")
def test_post_reaction_service_status_400(mock_upload_request):
    mock_upload_request.return_value.status_code = 400

    data = {
        "message": "un comentario cualquiera",
    }

    with pytest.raises(BaseException):
        video_service.post_reaction(12, data)
