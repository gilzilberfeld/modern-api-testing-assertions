from flask import Blueprint, jsonify, request
import store

books_bp = Blueprint("books", __name__)


@books_bp.route("/books", methods=["POST"])
def create_book():
    data = request.get_json(silent=True)
    if not data or "title" not in data or "author" not in data:
        return jsonify({"error": "title and author required"}), 400
    book = store.create_book(data["title"], data["author"])
    return jsonify(book), 201


@books_bp.route("/books/<book_id>", methods=["GET"])
def get_book(book_id):
    book = store.get_book(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book), 200


@books_bp.route("/books/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    if not store.delete_book(book_id):
        return jsonify({"error": "Book not found"}), 404
    return "", 204
