#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status')
def index():
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def stats():
    return jsonify({key: storage.count(value) for key, value in storage.models().items()})
