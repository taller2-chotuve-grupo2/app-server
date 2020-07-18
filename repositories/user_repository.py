from app.models import User
from app.models import User
from app import db


def save_user(username, device_id=None):
    u = User(username=username)
    if device_id:
        u.device_id = device_id
    db.session.add(u)
    db.session.commit()
    return u


def list_users(username):
    return User.query.filter(User.username.contains(username)).all()


def find_by_username(username):
    return User.query.filter_by(username=username).first()
