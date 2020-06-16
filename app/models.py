from app import db

friends = db.Table(
    "friends",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column(
        "user_request_id", db.Integer, db.ForeignKey("user.id"), primary_key=True
    ),
    db.Column("active", db.Boolean),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    friends = db.relationship(
        "User",
        secondary=friends,
        lazy="joined",
        primaryjoin=(friends.c.user_id == id),
        secondaryjoin=(friends.c.user_request_id == id),
    )

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
