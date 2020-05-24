from flask import Blueprint, request, current_app
import requests

bp = Blueprint('media', __name__)
base_auth_url = "https://chotuve-grupo2-auth-server-dev.herokuapp.com"
base_media_url = "https://media-server-staging-fiuba.herokuapp.com"
auth_endpoint = f"{base_auth_url}/auth/"
video_upload_endpoint = f"{base_media_url}/video/"
valid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTg5MDg3MDQyfQ.6g8IcVXhfJ7nSIWSodqhC-wbNnoWkEW3MEY4pdrbpMg"

@bp.route('/video/', methods=["POST","GET"])
def upload():
    token = request.headers.get('authorization')
    response = requests.post(auth_endpoint, headers={'authorization': 'Basic YWxhZGRpbjpvcGVuc2VzYW1l'}, json={"token":token})
    if response.status_code == 200:
        print("RIC")
        current_app.logger.info("RIC")
        requests.post(video_upload_endpoint, headers={'authorization': 'Basic YWxhZGRpbjpvcGVuc2VzYW1l'}, json=request.json)

        return response.json(), 201
    else:
        return "BAD LOGIN", 403