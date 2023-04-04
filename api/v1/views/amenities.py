#!/usr/bin/python3
""" Amenities for the viewssss"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity

"""
This module defines the routes for interacting with Amenity objects in the API.

Routes:
- GET /amenities: retrieves a list of all Amenity objects
- GET /amenities/<amenity_id>: retrieves a specific Amenity object by ID
- POST /amenities: creates a new Amenity object
- PUT /amenities/<amenity_id>: updates an existing Amenity object
- DELETE /amenities/<amenity_id>: deletes an Amenity object by ID
"""

@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def amenities():
    """method retrieves list of all Amenity objects in JSON format"""
    amenities = storage.all(Amenity)
    list_amenities = []
    for amenity in amenities.values():
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)


@app_views.route("/amenities/<amenity_id>", methods=['GET'], strict_slashes=False)
def amenity(amenity_id):
    """method retrieves an Amenity object in JSON format"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'], strict_slashes=False)
def del_amenity(amenity_id):
    """method deletes an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def post_amenity():
    """method creates a new Amenity object"""
    if not request.json or not request.is_json:
        abort(400, 'Not a JSON')
    elif 'name' not in request.json:
        abort(400, 'Missing name')
    else:
        new_amenity = Amenity(**request.json)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """method updates an existing Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    elif not request.json or not request.is_json:
        abort(400, 'Not a JSON')
    else:
        ignore = ['id', 'created_at', 'updated_at']
        for key, value in request.json.items():
            if key not in ignore:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
