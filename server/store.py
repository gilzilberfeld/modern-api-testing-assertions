import threading

_lock = threading.Lock()
_books = {}
_reviews = {}
_book_counter = [0]
_review_counter = [0]


def create_book(title, author):
    with _lock:
        _book_counter[0] += 1
        book_id = str(_book_counter[0])
        book = {"id": book_id, "title": title, "author": author}
        _books[book_id] = book
        _reviews[book_id] = []
        return dict(book)


def get_book(book_id):
    with _lock:
        return dict(_books[book_id]) if book_id in _books else None


def delete_book(book_id):
    with _lock:
        if book_id not in _books:
            return False
        del _books[book_id]
        _reviews.pop(book_id, None)
        return True


def create_review(book_id, rating, comment, user_id, timestamp):
    with _lock:
        if book_id not in _books:
            return None
        _review_counter[0] += 1
        review = {
            "id": str(_review_counter[0]),
            "book_id": book_id,
            "rating": rating,
            "comment": comment,
            "user_id": user_id,
            "timestamp": timestamp,
        }
        _reviews[book_id].append(review)
        return dict(review)


def get_reviews_for_book(book_id):
    with _lock:
        return [dict(r) for r in _reviews.get(book_id, [])]


def get_all_reviews():
    with _lock:
        result = []
        for reviews in _reviews.values():
            result.extend(dict(r) for r in reviews)
        return result


def get_review(book_id, review_id):
    with _lock:
        for r in _reviews.get(book_id, []):
            if r["id"] == review_id:
                return dict(r)
        return None


def update_review(book_id, review_id, rating, comment):
    with _lock:
        for r in _reviews.get(book_id, []):
            if r["id"] == review_id:
                r["rating"] = rating
                r["comment"] = comment
                return dict(r)
        return None


def delete_review(book_id, review_id):
    with _lock:
        reviews = _reviews.get(book_id, [])
        for i, r in enumerate(reviews):
            if r["id"] == review_id:
                reviews.pop(i)
                return True
        return False
