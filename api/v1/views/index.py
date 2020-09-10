#!/usr/bin/python3
"""File index"""
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/')
@app_views.route('/status')
def status():
    """status"""
    return jsonify({"status": "OK"})
