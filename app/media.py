from flask import Blueprint, request, current_app
from services.videoService import upload_video, get_feed
import requests

bp = Blueprint('media', __name__)
base_auth_url = "https://chotuve-grupo2-auth-server-dev.herokuapp.com"
base_media_url = "https://media-server-staging-fiuba.herokuapp.com"
auth_endpoint = f"{base_auth_url}/auth/"
video_upload_endpoint = f"{base_media_url}/video/"
valid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTg5MDg3MDQyfQ.6g8IcVXhfJ7nSIWSodqhC-wbNnoWkEW3MEY4pdrbpMg"

@bp.route('/video/', methods=["POST"])
def upload():
    token = request.headers.get('authorization')
    response = requests.post(auth_endpoint, headers={'authorization': 'Basic YWxhZGRpbjpvcGVuc2VzYW1l'}, json={"token":token})
    if response.status_code == 200:
        data = upload_video(request.json)
        return "OK", data.status_code
    else:
        return "BAD LOGIN", 403

@bp.route('/video/', methods=["GET"])
def feed():
    token = request.headers.get('authorization')
    response = requests.post(auth_endpoint, headers={'authorization': 'Basic YWxhZGRpbjpvcGVuc2VzYW1l'}, json={"token":token})
    if response.status_code == 200:
        current_app.logger.info(response.json)
        response = upload_video(request.json)
        return response.json(), 201
    else:
        return "BAD LOGIN", 403