#!/usr/bin/python3
"""-*- coding: utf-8 -*-"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage


@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    """
    Returns a list of all amenities
    """
    amenities = storage.all("Amenity").values()
    return jsonify([am.to_dict() for am in amenities])


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """
    Returns a amenity based on the id
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404, "Not found")


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """
    Deletes an amenity based on the id
    """
    if storage.get("Amenity", amenity_id):
        storage.delete(storage.get("Amenity", amenity_id))
        storage.save()
        return jsonify({}), 200
    abort(404, "Not found")


@app_views.route('/amenities', methods=['POST'])
def post_amenity():
    """
    posts a new state
    """
    if request.content_type != 'application/json':
        abort(400, "Not a JSON")
    content = request.get_json()

    if "name" not in content:
        abort(400, "Missing name")

    amenity = storage.models()['Amenity'](**content)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """
    Updates a state based on the id
    """
    if request.content_type != 'application/json':
        abort(400, "Not a JSON")
    content = request.get_json()
    amenity = storage.get("Amenity", amenity_id)

    for x in ["id", "created_at", "updated_at"]:
        content.pop(x, None)

    if amenity:
        for key, value in content.items():
            if hasattr(amenity.__class__, key):
                setattr(amenity, key, value)
            else:
                abort(404, "Not found")
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    abort(404, "Not found")
