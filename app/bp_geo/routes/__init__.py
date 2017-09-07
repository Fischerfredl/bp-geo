from flask import Blueprint
from app.bp_geo.models import Arena

api = Blueprint('api', __name__)


@api.route('/')
def test():
    return 'Index'


@api.route('/arena', methods=['GET'])
def create():
    a = Arena(name='peter').save()
    return 'success'


@api.route('/list')
def list():
    return
