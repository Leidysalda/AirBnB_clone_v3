#!/usr/bin/python3
"""This module create view for City objects
"""

from api.v1.views import storage, User, app_views
from flask import jsonify, request


@app_views.route("/users", methods=["GET"])
def get_user():
    """  list of all Users objects """

    all_user = storage.all(User).values()
    all_users = [user.to_dict() for user in all_user]

    return jsonify(all_users)


@app_views.route("/users/<user_id>", methods=["GET"])
def get_user_by_name(user_id=None):
    """ display a resource of my list of amenities """

    user_object = storage.get(User, user_id)
    if user_object is None:
        return jsonify({'Error': 'Not found'}), 404

    return jsonify(user_object.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id=None):
    """ delete a resource of my list of states """

    user_object = storage.get(User, user_id)
    if user_object is None:
        return jsonify({'Error': 'Not found'}), 404

    storage.delete(user_object)
    storage.save()

    return jsonify({}), 200


@app_views.route("/users", methods=["POST"])
def create_new_user(state_id=None):
    """ create new resource by my list of amenities """

    user_object_json = request.get_json()
    if user_object_json is None:
        return jsonify({'Error': 'Not a JSON'}), 400

    if 'email' not in user_object_json:
        return jsonify({'Error': 'Missing email'})

    if 'password' not in user_object_json.keys():
        return jsonify({'Error': 'Missing password'}), 400

    user_object = User(**user_object_json)
    user_object.save()

    return jsonify(user_object.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_a_user(user_id=None):
    """ update a resource of my objects """

    user_object_json = request.get_json()
    if user_object_json is None:
        return jsonify({'Error': 'Not a JSON'}), 400

    user = storage.get(User, user_id)
    if user is None:
        return jsonify({'Error': 'Not found'}), 404

    ignore = ['id', 'email', 'created_at', 'updated_at']

    for key, value in user_object_json.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()

    return jsonify(user.to_dict()), 200
