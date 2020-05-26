from flask import current_app
import requests

media_base_url = "https://media-server-staging-fiuba.herokuapp.com"
post_video_endpoint = f"{media_base_url}/video/"
get_feed_endpoint = f"{media_base_url}/video/"


def get_video_endpoint(id):
    return f"{media_base_url}/video/{id}"


auth_header = {"authorization": "Basic YWxhZGRpbjpvcGVuc2VzYW1l"}


def make_upload_video_request(data):
    response = requests.post(post_video_endpoint, headers=auth_header, json=data)
    return response


def make_feed_request():
    response = requests.get(get_feed_endpoint, headers=auth_header)
    return response


def make_get_video_request(id):
    response = requests.get(get_video_endpoint(id), headers=auth_header)
    return response


def upload_video(data):
    response = make_upload_video_request(data)
    if response.status_code == 200:
        return True
    else:
        raise BaseException


def get_feed(user):
    response = make_feed_request()
    if response.status_code == 200:
        return response.json()["videos"]
    else:
        raise BaseException


def get_video(id):
    response = make_get_video_request(id)
    if response.status_code == 200:
        return response.json()["video"]
    else:
        raise BaseException
