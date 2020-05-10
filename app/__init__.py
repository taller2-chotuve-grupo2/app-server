from flask import Flask

def create_app():
    
    app = Flask(__name__)

    from . import auth
    app.register_blueprint(auth.bp)

    @app.route('/')
    def richard():
        return "Richard!"


    return app