#!/usr/bin/python3
"""creates a new for city"""
from models.state import State
from models.city import City
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_state_cities(state_id):
    """retrieves all cities"""
    state = storage.get(State, state_id)
    if not state:
        return abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>',  methods=['GET'],
                 strict_slashes=False)
def get_city_id(city_id):
    """retrieves city object"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        return abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """delete city objects"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/states/<state_id>/<city>',
                 methods=['POST'], strict_slashes=False)
def create_city(city_id):
    """create city objects"""
    if request.content_type != 'application/json':
        return abort(400, "Not a JSON")
    state = storage.get(State, state_id)

    if not state:
        return abort(404, "Not a JSON")
    data = request.get_json()
    if "name" not in data:
        return abort(400, "Missing name")

    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """create city objects"""
    if request.content_type != 'application/json':
        return abort(400, "Not a JSON")
    city = storage.get(City, city_id)
    if city:
        if not request.get_json():
            return abort(400, "Not a JSON")
        data = request.get_json()
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
    return abort(404)
