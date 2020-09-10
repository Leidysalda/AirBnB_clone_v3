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

@app_views.route('/')
@app_views.route('/stats')
def count_all():
    """number of each objects"""

    return jsonify({"amenities": storage.count('Amenity'),
                    "cities": storage.count('City'),
                    "places": storage.count('Place'),
                    "reviews": storage.count('Review'),
                    "states": storage.count('State'),
                    "users": storage.count('User')})
