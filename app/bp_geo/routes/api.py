from flask import Blueprint, request, jsonify, abort, make_response
from mongoengine import ValidationError
from app.bp_geo.models import Arena, Match

api = Blueprint('api', __name__)


def abort_400(message=''):
    return abort(make_response(jsonify({'status': 'failed', 'message': message}), 400))


def success(message=''):
    return jsonify({'status': 'success', 'message': message})


def get_feature(model_cls, data):
    feature = model_cls.objects(data.get('id')).first()

    if not feature:
        return abort_400('feature not found')

    return feature


def process_request(model_cls):
    """Process a request

    GET: retrieve all features
    POST: save one feature as model_cls. Feature has to be valid GeoJSON-Point
    DELETE: delete one feature. data: {id: <id>}
    """

    data = request.get_json()

    if not data and request.method != 'GET':
        return abort_400('data is empty')

    if request.method == 'POST':
        feature = model_cls()
        feature.from_dict(data)

        try:
            feature.save()
        except ValidationError as e:
            return abort_400(e.message)

        return success('successfully posted feature')

    elif request.method == 'DELETE':
        feature = get_feature(model_cls, data)

        feature.delete()

        return success('feature successfully deleted')

    elif request.method == 'UPDATE':
        feature = get_feature(model_cls, data)

        feature.from_dict(data)

        try:
            feature.save()
        except ValidationError as e:
            return abort_400(e.message)

        return success('feature successfully updated')

    else:  # METHOD = GET
        if not data:
            return jsonify(model_cls.objects.to_collection())

        feature = get_feature(model_cls, data)

        return feature.to_json()


@api.route('/arena', methods=['GET', 'POST', 'DELETE', 'UPDATE'])
def arena():
    return process_request(Arena)


@api.route('/match', methods=['GET', 'POST', 'DELETE', 'UPDATE'])
def match():
    process_request(Match)
