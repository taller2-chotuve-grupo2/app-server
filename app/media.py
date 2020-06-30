import requests
from flask import Blueprint, request, current_app
from flask.json import jsonify
from services.video_service import upload_video, get_feed
from services import video_service, auth_service
from exceptions.invalid_login import InvalidToken

bp = Blueprint("media", __name__)


@bp.route("/video/", methods=["POST"])
def upload():
    token = request.headers.get("authorization")
    try:
        user = auth_service.verify_token(token)
        video_data = request.json
        video_data["owner"] = user
        video_id = video_service.upload_video(video_data)
        return jsonify({"id": video_id}), 200
    except InvalidToken:
        return "UNAUTHORIZED", 403
    except BaseException as e:
        return "Unable to handle request", 400


@bp.route("/video/", methods=["GET"])
def feed():
    token = request.headers.get("authorization")
    try:
        current_app.logger.info("RIC")
        user = auth_service.verify_token(token)
        print(user)
        videos = get_feed(user, request.args)
        return videos, 200
    except InvalidToken:
        return "UNAUTHORIZED", 403
    except BaseException:
        return "Unable to handle request", 400


@bp.route("/video/<id>", methods=["GET"])
def get_video(id):
    token = request.headers.get("authorization")
    try:
        auth_service.verify_token(token)
        video = video_service.get_video(id)
        return jsonify(video), 200
    except InvalidToken:
        return "UNAUTHORIZED", 403
    except BaseException:
        return "Unable to handle request", 400


@bp.route("/video/<id>/comment", methods=["POST"])
def post_comment(id):
    token = request.headers.get("authorization")
    try:
        auth_service.verify_token(token)
        print(request)
        data = video_service.post_comment(id, request.json)
        return "OK", 200
    except InvalidToken:
        return "UNAUTHORIZED", 403
    except BaseException:
        return "Unable to handle request", 400


@bp.route("/video/<id>/reaction", methods=["POST"])
def post_reaction(id):
    token = request.headers.get("authorization")
    try:
        auth_service.verify_token(token)
        print(request)
        data = video_service.post_reaction(id, request.json)
        return "OK", 200
    except InvalidToken:
        return "UNAUTHORIZED", 403
    except BaseException:
        return "Unable to handle request", 400
