from flask import Blueprint, jsonify, request, current_app
from datetime import datetime, timezone
import requests as http
import store
import auth as auth_module

reviews_bp = Blueprint("reviews", __name__)


@reviews_bp.route("/books/<book_id>/reviews", methods=["POST"])
def create_review(book_id):
    user_id = auth_module.get_user_id(request)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    if not store.get_book(book_id):
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    if "rating" not in data or "comment" not in data:
        return jsonify({"error": "rating and comment are required"}), 400

    if not isinstance(data["rating"], int) or data["rating"] < 1 or data["rating"] > 5:
        return jsonify({"error": "rating must be an integer between 1 and 5"}), 422

    moderation_url = current_app.config["MODERATION_URL"]
    try:
        mod_resp = http.post(
            f"{moderation_url}/moderate",
            json={"rating": data["rating"], "comment": data["comment"]},
            timeout=3,
        )
        if mod_resp.status_code >= 500:
            return jsonify({"error": "Moderation service error"}), 503
        result = mod_resp.json()
        if not result.get("approved"):
            return jsonify({"error": "Review rejected", "reason": result.get("reason")}), 422
    except http.exceptions.Timeout:
        return jsonify({"error": "Moderation service timed out"}), 504
    except http.exceptions.ConnectionError:
        return jsonify({"error": "Moderation service unavailable"}), 503

    timestamp = datetime.now(timezone.utc).isoformat()
    review = store.create_review(
        book_id=book_id,
        rating=data["rating"],
        comment=data["comment"],
        user_id=user_id,
        timestamp=timestamp,
    )
    return jsonify(review), 201


@reviews_bp.route("/books/<book_id>/reviews", methods=["GET"])
def list_reviews(book_id):
    if not store.get_book(book_id):
        return jsonify({"error": "Book not found"}), 404
    return jsonify(store.get_reviews_for_book(book_id)), 200


@reviews_bp.route("/reviews", methods=["GET"])
def list_all_reviews():
    return jsonify(store.get_all_reviews()), 200


@reviews_bp.route("/books/<book_id>/reviews/<review_id>", methods=["PUT"])
def update_review(book_id, review_id):
    user_id = auth_module.get_user_id(request)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    if not store.get_book(book_id):
        return jsonify({"error": "Book not found"}), 404

    review = store.get_review(book_id, review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404

    if review["user_id"] != user_id:
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    rating = data.get("rating", review["rating"])
    comment = data.get("comment", review["comment"])

    if not isinstance(rating, int) or rating < 1 or rating > 5:
        return jsonify({"error": "rating must be an integer between 1 and 5"}), 422

    updated = store.update_review(book_id, review_id, rating, comment)
    return jsonify(updated), 200


@reviews_bp.route("/books/<book_id>/reviews/<review_id>", methods=["DELETE"])
def delete_review(book_id, review_id):
    user_id = auth_module.get_user_id(request)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    if not store.get_book(book_id):
        return jsonify({"error": "Book not found"}), 404

    review = store.get_review(book_id, review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404

    if review["user_id"] != user_id:
        return jsonify({"error": "Forbidden"}), 403

    store.delete_review(book_id, review_id)
    return "", 204
