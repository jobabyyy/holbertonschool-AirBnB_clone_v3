#!/usr/bin/python3
"""View for review objects: handles default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=[
    'GET'], strict_slashes=False)
def get_reviews(place_id=None):
    """get all reviews"""
    place = storage.get(Place, place_id)
    if request.method == 'GET':
        if place is None:
            abort(404)
        return jsonify([reviews.to_dict() for reviews in place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def review_get_or_delete(review_id=None):
    """deletes a review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(review.to_dict())
    elif request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        if request.is_json:
            review_data = request.get_json()
        else:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        ignore_list = ['id', 'created_at', 'updated_at', 'place_id']
        for key, val in review_data.items():
            if key not in ignore_list:
                setattr(review, key, val)
        storage.save()
        return make_response(jsonify(review.to_dict()), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def review_post(place_id=None):
    """creates a review"""
    review_data = request.get_json()
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not review_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in review_data.keys():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    if storage.get(User, review_data['user_id']) is None:
        abort(404)
    if 'text' not in review_data.keys():
        return make_response(jsonify({'error': 'Missing text'}), 400)
    new_review = Review(**review_data)
    storage.save()
    return make_response(jsonify(new_review.to_dict()), 201)
