from flask import Flask

def create_app():
    return Flask(__name__)

app = create_app()

@app.route('/')
def richard():
    return "Richard!"

if __name__ == '__main__':
    app.run(host='0.0.0.0')