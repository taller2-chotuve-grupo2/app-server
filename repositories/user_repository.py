from app.models import User
from app import db


def save_user(username):
    u = User(username=username)
    db.session.add(u)
    db.session.commit()
