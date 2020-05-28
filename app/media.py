from flask import Blueprint, request, current_app
from services.video_service import upload_video, get_feed
from services import video_service, auth_service
import requests
from flask.json import jsonify

bp = Blueprint("media", __name__)


@bp.route("/video/", methods=["POST"])
def upload():
    token = request.headers.get("authorization")
    try:
        token_valid = auth_service.verify_token(token)
        data = upload_video(request.json)
        return "OK", 200
    except BaseException:
        return "UNAUTHORIZED", 403


@bp.route("/video/", methods=["GET"])
def feed():
    token = request.headers.get("authorization")
    try:
        user = auth_service.verify_token(token)
        videos = get_feed(user)
        return jsonify({"videos": videos}), 200
    except BaseException:
        return "UNAUTHORIZED", 403


@bp.route("/video/<id>", methods=["GET"])
def get_video(id):
    token = request.headers.get("authorization")
    try:
        auth_service.verify_token(token)
        video = video_service.get_video(id)
        return jsonify(video), 200
    except BaseException:
        return "UNAUTHORIZED", 403


@bp.route("/video/<id>/comment", methods=["POST"])
def post_comment(id):
    token = request.headers.get("authorization")
    try:
        auth_service.verify_token(token)
        print(request)
        data = video_service.post_comment(id, request.json)
        return "OK", 200
    except BaseException as e:
        return "UNAUTHORIZED", 403

@bp.route("/video/<id>/reaction", methods=["POST"])
def post_reaction(id):
    token = request.headers.get("authorization")
    try:
        auth_service.verify_token(token)
        print(request)
        data = video_service.post_reaction(id, request.json)
        return "OK", 200
    except BaseException as e:
        return "UNAUTHORIZED", 403
