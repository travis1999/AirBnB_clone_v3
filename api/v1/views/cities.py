#!/usr/bin/python3
"""# cities api"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """
    Returns a list of all states
    """

    if storage.get("State", state_id):
        cities = storage.all("City").values()
        return jsonify([city.to_dict() for city in cities if city.state_id == state_id])
    return abort(404, "Not found")


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """
    Returns a state based on the id
    """
    city = storage.get("City", city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404, "Not found")


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """
    Deletes a state based on the id
    """
    if storage.get("City", city_id):
        storage.delete(storage.get("City", city_id))
        storage.save()
        return jsonify({}), 200
    abort(404, "Not found")


@app_views.route('/api/v1/states/<state_id>/cities', methods=['POST'])
def post_city(state_id):
    """
    posts a new state
    """
    if request.content_type != 'application/json':
        abort(400, "Not a JSON")

    content = request.get_json()

    if "name" not in content:
        abort(400, "Missing name")

    state = storage.get("State", state_id)
    if not state:
        abort(404, "Not found")

    content["state_id"] = state_id
    city = storage.models()['City'](**content)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """
    Updates a state based on the id
    """
    if request.content_type != 'application/json':
        abort(400, "Not a JSON")
    content = request.get_json()

    city = storage.get("State", city_id)

    for x in ["id", "created_at", "updated_at"]:
        content.pop(x, None)

    if city:
        for key, value in content.items():
            if hasattr(city.__class__, key):
                setattr(city, key, value)
            else:
                abort(404, "Bad key {}".format(key))
        city.save()
        return jsonify(city.to_dict()), 200
    abort(404, "Not found")
