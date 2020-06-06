from flask import current_app
import requests

media_base_url = "https://media-server-staging-fiuba.herokuapp.com"
post_video_endpoint = f"{media_base_url}/resource/"
get_feed_endpoint = f"{media_base_url}/resource/"


def get_video_endpoint(id):
    return f"{media_base_url}/resource/{id}"


def post_comment_endpoint(id):
    return f"{media_base_url}/resource/{id}/comment/"


def post_reaction_endpoint(id):
    return f"{media_base_url}/resource/{id}/reaction/"


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


def make_post_comment_request(id, data):
    response = requests.post(post_comment_endpoint(id), headers=auth_header, json=data)
    return response


def make_post_reaction_request(id, data):
    response = requests.post(post_reaction_endpoint(id), headers=auth_header, json=data)
    return response


def upload_video(data):
    # current_app.logger.info(data)
    response = make_upload_video_request(data)
    if response.status_code == 200:
        return True
    else:
        raise BaseException


def get_feed(user):
    response = make_feed_request()
    current_app.logger.info("GET FEED")
    if response.status_code == 200:
        return response.json()
    else:
        raise BaseException


def get_video(id):
    response = make_get_video_request(id)
    if response.status_code == 200:
        return response.json()
    else:
        raise BaseException


def post_comment(id, data):
    response = make_post_comment_request(id, data)
    if response.status_code == 200:
        return True
    else:
        raise BaseException


def post_reaction(id, data):
    response = make_post_reaction_request(id, data)
    if response.status_code == 200:
        return True
    else:
        raise BaseException
