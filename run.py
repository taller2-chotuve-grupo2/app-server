import app as flask_app
from config import Config

app = flask_app.create_app(Config)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
