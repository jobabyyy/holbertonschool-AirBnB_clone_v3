#!/usr/bin/python3
""" Amenities views """

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenities():
    """ Retrieves the list of all Amenity objects """
    amenities = storage.all(Amenity)
    amenities_list = [amenity.to_dict() for amenity in amenities.values()]
    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def amenity(amenity_id):
    """ Retrieves a Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """ Deletes a Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def post_amenity():
    """ Creates a new Amenity object """
    if not request.json or not request.is_json:
        abort(400, 'Not a JSON')
    elif 'name' not in request.json:
        abort(400, 'Missing name')
    else:
        data = request.get_json()
        amenity = Amenity(**data)
        storage.new(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """ Updates a Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    elif not request.json or not request.is_json:
        abort(400, 'Not a JSON')
    else:
        data = request.get_json()
        ignore = ["id", "created_at", "updated_at"]
        for key, value in data.items():
            if key not in ignore:
                setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
