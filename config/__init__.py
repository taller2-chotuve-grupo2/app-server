import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv()


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")


class TestConfig(object):
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = "test"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "test.db")

    MAIL_SERVER: "smtp.sendgrid.net"
    MAIL_PORT: 587
    MAIL_USE_TLS: True
    # MAIL_USE_SSL : True
    MAIL_USERNAME: "apikey"
    MAIL_PASSWORD: "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"
