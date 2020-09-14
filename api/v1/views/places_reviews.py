#!/usr/bin/python3
"""This module create view for City objects
"""

from api.v1.views import storage, Review, Place, User, app_views
from flask import jsonify, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews_by_place_id(place_id=None):
    """  list of all Review objects of a Place """

    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({'Error': 'Not found'}), 404

    all_reviews = [review.to_dict() for review in place.reviews]

    return jsonify(all_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review_by_review_id(review_id=None):
    """display a reviews objects """

    review = storage.get(Review, review_id)
    if review is None:
        return jsonify({'Error': 'Not found'}), 404

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """delete review by id  """

    review = storage.get(Review, review_id)
    if review is None:
        return jsonify({'Error': 'Not found'}), 404

    storage.delete(review)
    storage.save()

    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_a_new_review(place_id):
    """ create new resource by my list of place """

    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({'Error': 'Not found'}), 404

    review_object_json = request.get_json()
    if review_object_json is None:
        return jsonify({'Error': 'Not a JSON'}), 400

    if 'user_id' not in review_object_json:
        return jsonify({'Error': 'Missing user_id'}), 400

    user_id = review_object_json.get('user_id')

    user = storage.get(User, user_id)
    if user is None:
        return jsonify({'Error': 'Not found'}), 404

    if 'text' not in review_object_json:
        return jsonify({'Error': 'Missing text'}), 400

    review_object_json['place_id'] = place_id
    instance = Review(**review_object_json)
    instance.save()

    return jsonify(instance.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def put_review(review_id):
    """ Updates a Review object resouce by id """

    review = storage.get(Review, review_id)
    if review is None:
        return jsonify({'Error': 'Not found'}), 404

    review_object_json = request.get_json()
    if review_object_json is None:
        return jsonify({'Error': 'Not a JSON'}), 400

    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    for key, value in review_object_json.items():
        if key not in ignore:
            setattr(review, key, value)
    storage.save()

    return jsonify(review.to_dict()), 200
