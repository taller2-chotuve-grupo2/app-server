from flask import current_app
import requests

media_base_url = "https://media-server-staging-fiuba.herokuapp.com"
post_video_endpoint = f"{media_base_url}/video/"
get_video_endpoint = f"{media_base_url}/video/"
auth_header = {"authorization": "Basic YWxhZGRpbjpvcGVuc2VzYW1l"}


def upload_video(data):
    response = requests.post(post_video_endpoint, headers=auth_header, json=data)
    return response

def get_feed(user):
    response = requests.get(get_video_endpoint, headers=auth_header)
    return response


# def login_user(username, password):
#     response = requests.post(login_endpoint,headers=auth_header,
#      json={"username":username,"password":password})
#     return response

# def register_user(username, password, email):
#     response = requests.post(register_endpoint, headers=auth_header,
#      json={"username":username,"password":password, "email":email})
#     return response
