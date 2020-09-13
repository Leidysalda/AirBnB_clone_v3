#!/usr/bin/python3
"""This module create view for City objects
"""

from api.v1.views import storage, City, Place, User, app_views
from flask import jsonify, request


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def get_cities_places(city_id=None):
    """  list of all City objects of a State """

    city = storage.get(City, city_id)
    if city is None:
        return jsonify({'Error': 'Not found'}), 404

    all_places = [place.to_dict() for place in city.places]

    return jsonify(all_places)


@app_views.route("/places/<place_id>", methods=["GET"])
def get_places_by_name(place_id=None):
    """ display a places object"""

    place_object = storage.get(Place, place_id)
    if place_object is None:
        return jsonify({'Error': 'Not found'}), 404

    return jsonify(place_object.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id=None):
    """ delete a place object by id """

    place_object = storage.get(Place, place_id)
    if place_object is None:
        return jsonify({'Error': 'Not found'}), 404

    storage.delete(place_object)
    storage.save()

    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_new_place(city_id=None):
    """ create new resource by my list of place """

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

    city = storage.get(City, city_id)
    if city is None:
        return jsonify({'Error': 'Not found'}), 404

    place_object_json = request.get_json()
    if place_object_json is None:
        return jsonify({'Error': 'Not a JSON'}), 400

    if 'user_id' not in place_object_json.keys():
        return jsonify({'Error': 'Missing user_id'}), 400

    user = storage.get(User, place_object_json.get("user_id"))
    if user is None:
        return jsonify({'Error': 'Not found'}), 404

    if 'name' not in place_object_json.keys():
        return jsonify({'Error': 'Missing name'}), 400

    place_object_json["city_id"] = city_id

    object_place = Place(**place_object_json)
    object_place.save()

    return jsonify(object_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_a_place(place_id=None):
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

    place_object_json = request.get_json()
    if place_object_json is None:
        return jsonify({'Error': 'Not a JSON'}), 400

    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({'Error': 'Not found'}), 404

    ignore = ['id', 'user_id', 'created_at', 'updated_at']

    for key, value in request.get_json().items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()

    return jsonify(place.to_dict()), 200
