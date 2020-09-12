#!/usr/bin/python3
"""This module create view for City objects
"""

from api.v1.views import storage, Amenity, app_views
from flask import jsonify, request


@app_views.route("/amenities", methods=["GET"])
def get_amenities():
    """  list of all Amenity objects """

    all_amenitie = storage.all(Amenity).values()
    all_amenities = [state.to_dict() for state in all_amenitie]

    return jsonify(all_amenities)


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def get_amenity_by_name(amenity_id=None):
    """ display a resource of my list of amenities """

    amenity_object = storage.get(Amenity, amenity_id)
    if amenity_object is None:
        return jsonify({'Error': 'Not found'}), 404

    return jsonify(amenity_object.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id=None):
    """ delete a resource of my list of states """

    amenity_object = storage.get(Amenity, amenity_id)
    if amenity_object is None:
        return jsonify({'Error': 'Not found'}), 404

    storage.delete(amenity_object)
    storage.save()

    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"])
def create_new_amenity(state_id=None):
    """ create new resource by my list of amenities """

    amenity_object_json = request.get_json()
    if amenity_object_json is None:
        return jsonify({'Error': 'Not a JSON'}), 400

    if 'name' not in amenity_object_json.keys():
        return jsonify({'Error': 'Missing name'}), 400

    amenity_object = Amenity(**amenity_object_json)
    amenity_object.save()

    return jsonify(amenity_object.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_a_amenity(amenity_id=None):
    """ update a resource of my objects """

    amenity_object_json = request.get_json()
    if amenity_object_json is None:
        return jsonify({'Error': 'Not a JSON'}), 400

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({'Error': 'Not found'}), 404

    ignore = ['id', 'created_at', 'updated_at']

    for key, value in amenity_object_json.items():
        if key not in ignore:
            setattr(amenity, key, value)
    storage.save()

    return jsonify(amenity.to_dict()), 200
