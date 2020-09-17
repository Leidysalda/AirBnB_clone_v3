#!/usr/bin/python3
""" Creates a new view for the link between Place objects
"""

from api.v1.views import storage, Place, Amenity, app_views
from os import getenv
from flask import jsonify, request


@app_views.route('places/<place_id>/amenities', methods=['GET'])
def get_amenities_by_place_id(place_id):
    """ Lists all objects of the place """

    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({'Error': 'Not found'}), 404

    if getenv('HBNB_TYPE_STORAGE') == "db":
        all_amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        all_amenities = []
        for ids in place.amenity_ids:
            amenity = storage.get(Amenity, ids)
            all_amenities.append(amenity.to_dict())

    return jsonify(all_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_amenity_by_place_id(place_id, amenity_id):
    """  deletes a amenity object by place_id    """

    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({'Error': 'Not found'}), 404

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({'Error': 'Not found'}), 404

    if getenv('HBNB_TYPE_STORAGE') == "db":

        if amenity not in place.amenities:
            return jsonify({'Error': 'Not found'}), 404

        place.amenities.remove(amenity)

    else:
        if amenity_id not in place.amenity_ids:
            return jsonify({'Error': 'Not found'}), 404

        place.amenity_ids.remove(amenity_id)

    storage.save()

    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'])
def link_amenity_to_place(place_id=None, amenity_id=None):
    """ Link a Amenity object to a Place """

    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({'Error': 'Not found'}), 404

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({'Error': 'Not found'}), 404

    if getenv('HBNB_TYPE_STORAGE') == "db":

        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenities.append(amenity)
    else:

        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenity_ids.append(amenity_id)

    storage.save()

    return jsonify(amenity.to_dict()), 201
