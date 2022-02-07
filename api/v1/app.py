#!/usr/bin/python3
"""# -*- coding: utf-8 -*"""

from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["0.0.0.0"]}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def on_exit(context):
    """
    This function is called when the application context is about to be
    destroyed.
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    This function is called when the application encounters a 404 error.
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
