from flask import Blueprint, request
import requests

bp = Blueprint('media', __name__)
auth_endpoint = "https://chotuve-grupo2-auth-server-dev.herokuapp.com/auth/"

@bp.route('/upload/', methods=["POST","GET"])
def upload():
    token = request.headers.get('authorization')
    response = requests.post(auth_endpoint, json={"token":token})
    if response.status_code == 200:
        return response.json(), 200
    else:
        return "BAD LOGIN", 403