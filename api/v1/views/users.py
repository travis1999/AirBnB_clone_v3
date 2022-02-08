#!/usr/bin/python3
"""# users api"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage


@app_views.route('/users', methods=['GET'])
def get_users():
    """
    Returns a list of all users
    """
    users = storage.all("User").values()
    return jsonify([am.to_dict() for am in users])


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    Returns a amenity based on the id
    """
    user = storage.get("User", user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404, "Not found")


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes an user based on the id
    """
    if storage.get("user", user_id):
        storage.delete(storage.get("User", user_id))
        storage.save()
        return jsonify({}), 200
    abort(404, "Not found")


@app_views.route('/users', methods=['POST'])
def post_user():
    """
    posts a new state
    """
    if request.content_type != 'application/json':
        abort(404, "Not a JSON")
    content = request.get_json()

    required_keys = ["email", "password"]

    for key in required_keys:
        if key not in content:
            abort(404, "Missing {}".format(key))

    user = storage.models()['User'](**content)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Updates a state based on the id
    """
    if request.content_type != 'application/json':
        abort(404, "Not a JSON")
    content = request.get_json()
    user = storage.get("User", user_id)

    for x in ["id", "created_at", "updated_at"]:
        content.pop(x, None)

    if user:
        for key, value in content.items():
            if hasattr(user.__class__, key):
                setattr(user, key, value)
            else:
                abort(404, "Not found")
        user.save()
        return jsonify(user.to_dict()), 200
    abort(404, "Not found")
