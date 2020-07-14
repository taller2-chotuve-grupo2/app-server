from flask import Flask, send_file, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_cors import CORS
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()


def create_app(config):

    import logging, logging.config, yaml

    logging.config.dictConfig(
        yaml.load(open("app/logging.conf"), Loader=yaml.FullLoader)
    )

    # logging.basicConfig(filename="demo.log", level=logging.DEBUG)
    # logging.config.fileConfig("logging.conf")
    app = Flask(__name__)
    CORS(app)
    app.logger.info("STARTED APP SERVER")
    app.config.from_object(config)
    mail.init_app(app)
    db.init_app(app)
    from app import models

    migrate = Migrate(app, db)

    from . import auth, media, contact

    app.register_blueprint(auth.bp)
    app.register_blueprint(media.bp)
    app.register_blueprint(contact.bp)

    @app.route("/")
    def richard():
        return "Richard!"

    @app.route("/ping/")
    def health():
        return "OK"

    @app.route("/docs")
    def docs():
        return send_file("../docs/index.html")

    @app.route("/yml")
    def yml():
        return send_file("../docs/openapi.yml")

    @app.route("/javascripts/<path:path>")
    def send_js(path):
        return send_from_directory("../public/javascripts", path)

    @app.route("/stylesheets/<path:path>")
    def send_styles(path):
        return send_from_directory("../public/stylesheets", path)

    return app
