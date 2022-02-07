#!/usr/bin/python3
"""-*- coding: utf-8 -*-"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def index():
    """
    returns the status of the API
    """
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def stats():
    """
    returns the number of objects in the storage
    """
    return jsonify({key: storage.count(value) 
            for key, value in storage.models().items()})
