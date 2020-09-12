#!/usr/bin/python3
"""This module create view for City objects
"""

from api.v1.views import storage, State, City, app_views
from flask import jsonify, request


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def get_cities(state_id=None):
    """  list of all City objects of a State """

    state = storage.get(State, state_id)
    if state is None:
        return jsonify({'Error': 'Not found'}), 404

    all_cities = [city.to_dict() for city in state.cities]

    return jsonify(all_cities)


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_cities_by_name(city_id=None):
    """ display a city object by name"""

    city_object = storage.get(City, city_id)
    if city_object is None:
        return jsonify({'Error': 'Not found'}), 404

    return jsonify(city_object.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id=None):
    """ delete a city object by id """

    city_object = storage.get(City, city_id)
    if city_object is None:
        return jsonify({'Error': 'Not found'}), 404

    storage.delete(city_object)
    storage.save()

    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_new_city(state_id=None):
    """ create new resource by my list of cities """

    print("New request:")
    # print("\t-path: {}".format(path))
    print("\t-verb: {}".format(request.method))

    print("\t-headers: ")
    for k, v in request.headers:
        print("\t\t{} = {}".format(k, v))

    print("\t-query parameters: ")
    for qp in request.args:
        print("\t\t{} = {}".format(qp, request.args.get(qp)))

    print("\t-raw body: ")
    print("\t\t{}".format(request.data))

    print("\t-form body: ")
    for fb in request.form:
        print("\t\t{} = {}".format(fb, request.form.get(fb)))

    print("\t-json body: ")
    print("\t\t{}".format(request.json))

    state = storage.get(State, state_id)
    if state is None:
        return jsonify({'Error': 'Not found'}), 404

    city_object_json = request.get_json()
    if city_object_json is None:
        return jsonify({'Error': 'Not a JSON'}), 400

    if 'name' not in city_object_json.keys():
        return jsonify({'Error': 'Missing Name'}), 400

    city_object_json["state_id"] = state_id

    object_city = City(**city_object_json)
    object_city.save()

    return jsonify(object_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_a_city(city_id=None):
    """ update a object city by id """

    print("New request:")
    # print("\t-path: {}".format(path))
    print("\t-verb: {}".format(request.method))

    print("\t-headers: ")
    for k, v in request.headers:
        print("\t\t{} = {}".format(k, v))

    print("\t-query parameters: ")
    for qp in request.args:
        print("\t\t{} = {}".format(qp, request.args.get(qp)))

    print("\t-raw body: ")
    print("\t\t{}".format(request.data))

    print("\t-form body: ")
    for fb in request.form:
        print("\t\t{} = {}".format(fb, request.form.get(fb)))

    print("\t-json body: ")
    print("\t\t{}".format(request.json))

    city_object_json = request.get_json()
    if city_object_json is None:
        return jsonify({'Error': 'Not a JSON'}), 400

    city = storage.get(City, city_id)
    if city is None:
        return jsonify({'Error': 'Not found'}), 404

    ignore = ['id', 'state_id', 'created_at', 'updated_at']

    for key, value in request.get_json().items():
        if key not in ignore:
            setattr(city, key, value)
    storage.save()

    return jsonify(city.to_dict()), 200
