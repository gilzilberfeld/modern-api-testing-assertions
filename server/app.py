import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from routes_books import books_bp
from routes_reviews import reviews_bp


def create_app():
    app = Flask(__name__)
    app.config["MODERATION_URL"] = os.environ.get("MODERATION_URL", "http://localhost:5001")
    app.register_blueprint(books_bp)
    app.register_blueprint(reviews_bp)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=5000, threaded=True)
