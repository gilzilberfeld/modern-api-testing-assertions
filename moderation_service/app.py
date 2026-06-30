import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from routes import mod_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(mod_bp)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=5001, threaded=True)
