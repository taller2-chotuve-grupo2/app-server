from flask import current_app
import requests
import json
from models import Feed, updateVideosWithCount

media_base_url = "https://media-server-staging-fiuba.herokuapp.com"
post_video_endpoint = f"{media_base_url}/resource/"
get_feed_endpoint = f"{media_base_url}/resource/feed"
feed = Feed()


def get_video_endpoint(id):
    return f"{media_base_url}/resource/{id}"


def post_comment_endpoint(id):
    return f"{media_base_url}/resource/{id}/comment/"


def reaction_endpoint(id):
    return f"{media_base_url}/resource/{id}/reaction/"


auth_header = {"authorization": "Basic YWxhZGRpbjpvcGVuc2VzYW1l"}


def make_upload_video_request(data):
    response = requests.post(post_video_endpoint, headers=auth_header, json=data)
    return response


def make_feed_request(query_params):
    response = requests.get(get_feed_endpoint, headers=auth_header, params=query_params)
    return response


def make_get_video_request(id, username):
    user_query = {"username": username}
    response = requests.get(
        get_video_endpoint(id), headers=auth_header, params=user_query
    )
    return response


def make_post_comment_request(id, data):
    response = requests.post(post_comment_endpoint(id), headers=auth_header, json=data)
    return response


def make_post_reaction_request(id, data):
    response = requests.post(reaction_endpoint(id), headers=auth_header, json=data)
    return response


def make_get_video_reactions_request(id, query_params):
    response = requests.get(
        reaction_endpoint(id), headers=auth_header, params=query_params
    )
    return response


def upload_video(data):
    # current_app.logger.info(data)
    response = make_upload_video_request(data)
    if response.status_code == 200:
        return response.json()["id"]
    else:
        raise BaseException


def get_feed(user, query_params):
    if feed.expired():
        feed.regenerate(query_params)
    return feed.videosSortedImportance()


def get_video(id, username=""):
    response = make_get_video_request(id, username)
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


def get_video_reaction(id, query_params):
    response = make_get_video_reactions_request(id, query_params)
    if response.status_code == 200:
        return response.json()
    else:
        raise BaseException


def get_videos_by_username(username, private=False):
    query_params = {"owner": username}
    if private:
        query_params["visibility"] = "private"
    response = make_feed_request(query_params)
    videos_feed = response.json()
    videos = updateVideosWithCount(videos_feed)
    videos = [video.__dict__ for video in videos]
    if response.status_code == 200:
        return videos
    else:
        raise BaseException
