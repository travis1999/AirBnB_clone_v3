#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from api.v1.views import app_views
from flask import jsonify, request


@app_views.route('/status')
def index():
    return jsonify({'status': 'OK'})
