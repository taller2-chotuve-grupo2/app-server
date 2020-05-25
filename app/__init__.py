from flask import Flask, send_file, send_from_directory

def create_app():
    
    import logging
    logging.basicConfig(filename='demo.log', level=logging.DEBUG)
    app = Flask(__name__)
    # app.logger.info("STARTED")

    from . import auth, media
    app.register_blueprint(auth.bp)
    app.register_blueprint(media.bp)

    @app.route('/')
    def richard():
        return "Richard!"

    @app.route('/docs')
    def docs():
        return send_file('../public/index.html')

    @app.route('/javascripts/<path:path>')
    def send_js(path):
        return send_from_directory('../public/javascripts', path)

    @app.route('/stylesheets/<path:path>')
    def send_styles(path):
        return send_from_directory('../public/stylesheets', path)
    
    
    return app