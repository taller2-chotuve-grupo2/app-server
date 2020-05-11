from flask import Blueprint, request
import requests

bp = Blueprint('media', __name__)
auth_endpoint = "https://chotuve-grupo2-auth-server-dev.herokuapp.com/auth/"
valid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTg5MDg3MDQyfQ.6g8IcVXhfJ7nSIWSodqhC-wbNnoWkEW3MEY4pdrbpMg"

@bp.route('/upload/', methods=["POST","GET"])
def upload():
    token = request.headers.get('authorization')
    response = requests.post(auth_endpoint, headers={'authorization': 'Basic YWxhZGRpbjpvcGVuc2VzYW1l'}, json={"token":token})
    if response.status_code == 200:
        return response.json(), 201
    else:
        return "BAD LOGIN", 403