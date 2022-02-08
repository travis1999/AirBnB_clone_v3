#!/usr/bin/python3
"""# places api"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage


@app_views.route('/places/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """
    Returns a list of all places
    """

    if storage.get("City", city_id):
        places = storage.all("Place").values()
        return jsonify([place.to_dict() for place in places if place.city_id == city_id])
    return abort(404, "Not found")


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """
    Returns a city based on the id
    """
    place = storage.get("Place", place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404, "Not found")


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """
    Deletes a place based on the id
    """
    if storage.get("Place", place_id):
        storage.delete(storage.get("Place", place_id))
        storage.save()
        return jsonify({}), 200
    abort(404, "Not found")


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def post_place(city_id):
    """
    posts a new city
    """
    if request.content_type != 'application/json':
        abort(404, "Not a JSON")

    content = request.get_json()

    if "user_id" not in content:
        abort(404, "Missing user_id")

    if "name" not in content:
        abort(404, "Missing name")

    user = storage.get("User", content["user_id"])
    if not user:
        abort(404, "Not found")

    city = storage.get("City", city_id)
    if not city:
        abort(404, "Not found")

    content["city_id"] = city_id

    place = storage.models()['Place'](**content)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """
    Updates a city based on the id
    """
    if request.content_type != 'application/json':
        abort(404, "Not a JSON")
    content = request.get_json()

    place = storage.get("Place", place_id)

    for x in ["id", "created_at", "updated_at"]:
        content.pop(x, None)

    if place:
        for key, value in content.items():
            if hasattr(place.__class__, key):
                setattr(place, key, value)
            else:
                abort(404, "Bad key {}".format(key))
        place.save()
        return jsonify(place.to_dict()), 200
    abort(404, "Not found")
