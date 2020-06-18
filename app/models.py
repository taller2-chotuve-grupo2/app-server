from app import db
from sqlalchemy import (
    Integer,
    Table,
    Column,
    ForeignKey,
    create_engine,
    String,
    select,
    or_,
)
from sqlalchemy.orm import Session, relationship


class Friendship(db.Model):
    __tablename__ = "friendships"
    friend_a = db.Column(Integer, db.ForeignKey("users.id"), primary_key=True)
    friend_b = db.Column(Integer, db.ForeignKey("users.id"), primary_key=True)
    status = db.Column(String, default="pending")


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(Integer, primary_key=True)
    username = db.Column(String, unique=True)

    # this relationship is used for persistence
    friends = relationship(
        "User",
        secondary="friendships",
        primaryjoin=id == Friendship.friend_a,
        secondaryjoin=id == Friendship.friend_b,
    )
    pending_friends = relationship(
        "User",
        secondary="friendships",
        primaryjoin=id == Friendship.friend_b,
        secondaryjoin=((id == Friendship.friend_a) & (Friendship.status=="pending")),
        viewonly=True
    )

    friends_a_accepted = relationship(
        "User",
        secondary="friendships",
        primaryjoin=id == Friendship.friend_a,
        secondaryjoin=((id == Friendship.friend_b) & (Friendship.status=="accepted")),
        viewonly=True
    )
    friends_a_accepted = relationship(
        "User",
        secondary="friendships",
        primaryjoin=id == Friendship.friend_b,
        secondaryjoin=((id == Friendship.friend_a) & (Friendship.status=="accepted")),
        viewonly=True
    )

    def __repr__(self):
        return "User(%r)" % self.username

    @property
    def all_friends(self):
        return self.friends_a_accepted + self.friends_b_accepted

    def add_friend(self, friend):
        self.friends.append(friend)
        db.session.commit()

    def accept_friend(self, friend):
        Friendship.query.filter_by(friend_a=friend.id, friend_b=self.id).update(dict(status="accepted"))
        db.session.commit()

