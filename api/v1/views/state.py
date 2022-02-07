#!/usr/bin/python3
# state api

from api.v1.app import app_views
from flask import jsonify, request, abort
from models import storage


@app_views.route('/states', methods=['GET'])
def get_states():
    """
    Returns a list of all states
    """
    states = storage.all("State").values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """
    Returns a state based on the id
    """
    state = storage.get("State", state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404, "Not found")


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """
    Deletes a state based on the id
    """
    if storage.get("State", state_id):
        storage.delete(storage.get("State", state_id))
        storage.save()
        return jsonify({}), 200
    abort(404, "Not found")


@app_views.route('/states/', methods=['POST'])
def post_state():
    """
    posts a new state
    """
    if request.content_type != 'application/json':
        abort(404, "Not a JSON")
    content = request.get_json()

    if "name" not in content:
        abort(404, "Missing name")

    state = storage.models()['State'](**content)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """
    Updates a state based on the id
    """
    if request.content_type != 'application/json':
        abort(404, "Not a JSON")
    content = request.get_json()
    state = storage.get("State", state_id)

    for x in ["id", "created_at", "updated_at"]:
        content.pop(x, None)

    if state:
        for key, value in content.items():
            if hasattr(state.__class__, key):
                setattr(state, key, value)
            else:
                abort(404, "Not found")
        state.save()
        return jsonify(state.to_dict()), 200
    abort(404, "Not found")
