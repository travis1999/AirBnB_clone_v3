#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask
from api.v1.views import app_views
from models import storage
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def on_exit(context):
    """
    This function is called when the application context is about to be
    destroyed.
    """
    storage.close()


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port,threaded=True)
