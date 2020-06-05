from flask import Flask, send_file, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()

def create_app(config):

    import logging

    logging.basicConfig(filename="demo.log", level=logging.DEBUG)
    app = Flask(__name__)
    app.logger.info("STARTED APP SERVER")
    print("RIC")
    print(config)
    app.config.from_object(config)
    print(app.config)
    db.init_app(app)
    migrate = Migrate(app, db)

    from app import models
    from . import auth, media

    app.register_blueprint(auth.bp)
    app.register_blueprint(media.bp)

    @app.route("/")
    def richard():
        return "Richard!"

    @app.route("/docs")
    def docs():
        return send_file("../docs/index.html")

    @app.route("/javascripts/<path:path>")
    def send_js(path):
        return send_from_directory("../public/javascripts", path)

    @app.route("/stylesheets/<path:path>")
    def send_styles(path):
        return send_from_directory("../public/stylesheets", path)

    return app
