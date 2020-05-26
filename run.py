import app as flask_app
import os

app = flask_app.create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
