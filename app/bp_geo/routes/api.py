from flask import Blueprint, request, jsonify, abort, g
from mongoengine import ValidationError
from app.bp_geo.models import Arena, Match

api = Blueprint('api', __name__)


# ----------------------------------------------------------------------------------------------------------------------
# URL Preprocessor
# ----------------------------------------------------------------------------------------------------------------------

@api.url_value_preprocessor
def preprocessor(endpoint, values):
    """parses url values to g object

    g.collection = collection class
    g.item = specific item

    can result in 404
    """

    collection = values.pop('collection', None)

    if collection == 'arenas':
        g.collection = Arena
    elif collection == 'matches':
        g.collection = Match
    else:
        abort(404)

    item_id = values.pop('item_id', None)
    if not item_id:
        return

    g.item = g.collection.objects(id=item_id).first()
    if not g.item:
        abort(404)

    return


# ----------------------------------------------------------------------------------------------------------------------
# Routes whole collection
# ----------------------------------------------------------------------------------------------------------------------

@api.route('/<collection>', methods=['POST'])
def post_collection():
    data = request.get_json(force=True)

    feature = g.collection()
    feature.from_dict(data)

    try:
        feature.save()
    except ValidationError as e:
        return abort(400, 'Valid JSON, but could not save as feature')

    resp = jsonify(feature.to_feature())
    resp.headers['Location'] = feature.to_feature().get('uri', None)

    return resp


@api.route('/<collection>', methods=['GET'])
def get_collection():
    return jsonify(g.collection.objects().to_collection())


# ----------------------------------------------------------------------------------------------------------------------
# Routes: single item
# ----------------------------------------------------------------------------------------------------------------------

@api.route('/<collection>/<objectid:item_id>', methods=['GET'])
def get_item():
    return jsonify(g.item.to_feature())


@api.route('/<collection>/<objectid:item_id>', methods=['PUT'])
def put_item():
    data = request.get_json(force=True)

    g.item.from_dict(data)

    try:
        g.item.save()
    except ValidationError as e:
        return abort(400, 'Valid JSON, but could not save as feature')

    return jsonify(g.item.to_feature())


@api.route('/<collection>/<objectid:item_id>', methods=['DELETE'])
def delete_item():
    g.item.delete()

    return jsonify({'response': 'Feature sucessfully deleted', 'feature': g.item.to_feature()})
