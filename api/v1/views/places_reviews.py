#!/usr/bin/python3
# reviews api

from api.v1.app import app_views
from flask import jsonify, request, abort
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews(place_id):
    """
    Returns a list of all reviews
    """

    if storage.get("Place", place_id):
        reviews = storage.all("Review").values()
        return jsonify([rev.to_dict() for rev in reviews if rev.place_id == place_id])
    return abort(404, "Not found")


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """
    Returns a city based on the id
    """
    rev = storage.get("Review", review_id)
    if rev:
        return jsonify(rev.to_dict())
    abort(404, "Not found")


@app_views.route('/api/v1/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """
    Deletes a place based on the id
    """
    rev = storage.get("Review", review_id)
    if rev:
        storage.delete(rev)
        storage.save()
        return jsonify({}), 200
    abort(404, "Not found")


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def post_review(place_id):
    """
    posts a new city
    """
    if request.content_type != 'application/json':
        abort(404, "Not a JSON")

    content = request.get_json()

    required_fields = ["user_id", "text"]

    for k in required_fields:
        if k not in content:
            abort(404, "Missing {}".format(k))

    user = storage.get("User", content["user_id"])
    if not user:
        abort(404, "Not found")

    place = storage.get("Place", place_id)
    if not place:
        abort(404, "Not found")

    content["place_id"] = place_id

    review = storage.models()['Review'](**content)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """
    Updates a city based on the id
    """
    if request.content_type != 'application/json':
        abort(404, "Not a JSON")
    content = request.get_json()

    review = storage.get("Review", review_id)

    for x in ["id", "created_at", "updated_at"]:
        content.pop(x, None)

    if review:
        for key, value in content.items():
            if hasattr(review.__class__, key):
                setattr(review, key, value)
            else:
                abort(404, "Bad key {}".format(key))
        review.save()
        return jsonify(review.to_dict()), 200
    abort(404, "Not found")
