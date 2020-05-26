from flask import Blueprint, request, current_app
from services.video_service import upload_video, get_feed
from services import video_service, auth_service
import requests
from flask.json import jsonify

bp = Blueprint('media', __name__)

@bp.route('/video/', methods=["POST"])
def upload():
    token = request.headers.get('authorization')
    token_valid = auth_service.verify_token(token)
    if not token_valid: 
        return "UNAUTHORIZED", 403
    else:
        request_data = request.data
        data = upload_video(request.json)
        # data = video_service.upload_video(request_data)
        return "OK", data.status_code

@bp.route('/video/', methods=["GET"])
def feed():
    token = request.headers.get('authorization')
    token_valid = auth_service.verify_token(token)
    if not token_valid: 
        return "UNAUTHORIZED", 403
    else:
        videos = get_feed()
        return jsonify({"videos": videos}), 201