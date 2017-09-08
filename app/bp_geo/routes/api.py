from flask import Blueprint, request, jsonify, abort, make_response
from mongoengine import ValidationError
from app.bp_geo.models import Arena, Match

api = Blueprint('api', __name__)


@api.route('/arena', methods=['GET', 'POST'])
def arena():
    """Post one Feature as Arena or retrieve all Arenas

    Feature has to be valid GeoJSON-Point (see Feature model):
    """

    if request.method == 'POST':
        a = Arena()
        a.from_dict(request.get_json())

        try:
            a.save()
        except ValidationError as e:
            return abort(make_response(jsonify(message=e.message), 400))

        return jsonify({'status': 'successfully posted Arena-feature'})
    else:
        return jsonify(Arena.objects.to_collection())


@api.route('/match', methods=['GET', 'POST'])
def match():
    """Post one Feature as Match or retrieve all Matches

    Feature has to be valid GeoJSON-Point (see Feature model):
    """

    if request.method == 'POST':
        m = Match()
        m.from_dict(request.get_json())

        try:
            m.save()
        except ValidationError as e:
            return abort(make_response(jsonify(message=e.message), 400))

        return jsonify({'status': 'successfully posted Match-feature'})
    else:
        return jsonify(Arena.objects.to_collection())


@api.route('/json')
def json():
    return jsonify(Arena.objects.to_collection())