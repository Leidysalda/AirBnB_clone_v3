#!/usr/bin/python3
""" Create a new view for State objects that handles
    all default RestFul API actions:
"""

from models import storage
from models.state import State
from flask import jsonify, request
from api.v1.views import app_views


@app_views.route("/states", methods=["GET"])
def get_states():
    """ list of all State objects """

    all_states = storage.all(State).values()
    states_dict = [state.to_dict() for state in all_states]

    return jsonify(states_dict)


@app_views.route("/states/<state_id>", methods=["GET"])
def get_states_by_id(state_id=None):
    """ list one state objecty by id"""

    state_object = storage.get(State, state_id)
    if state_object is None:
        return jsonify({'Error': 'Not found'}), 404

    return jsonify(state_object.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_states_by_id(state_id=None):
    """ delete one state objecty by id"""

    state_object = storage.get(State, state_id)
    if state_object is None:
        return jsonify({'Error': 'Not found'}), 404

    storage.delete(state_object)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"])
def create_new_state(state_id=None):
    """ create a new state """

    # body of request
    request_json = request.get_json()

    if request_json is None:
        return jsonify({'Error': 'Not a JSON'}), 400

    if 'name' not in request_json:
        return jsonify({'Error': 'Missing name'}), 400

    state = State(**request_json)
    state.save()

    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id=None):
    """ create a new state """

    # body of request
    request_json = request.get_json()
    if request_json is None:
        return jsonify({'Error': 'Not a JSON'}), 400

    state = storage.get(State, state_id)
    if state is None:
        return jsonify({'Error': 'Not found'}), 404

    ignore = ['id', 'created_at', 'updated_at']

    for key, value in request_json.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()

    return jsonify(state.to_dict()), 200
