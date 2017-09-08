from mongoengine import QuerySet

from ext import db, bcrypt


class FeatureQuerySet(QuerySet):
    """Extends QuerySet by a to_collection method"""
    def to_collection(self):
        data = {
            'type': 'FeatueCollection',
            'features': [f.to_feature() for f in self]
        }
        return data


class Feature(db.Document):
    """A Point Feature

    valid Feature:
    - geometry: type: "Point", coordinates: <two-dim Array>
    - type: "Feature"
    - properties: a dict

    """

    type = db.StringField(default='Feature', choices=['Feature'])
    geometry = db.PointField(null=False)
    properties = db.DictField()

    meta = {
        'allow_inheritance': True,
        'abstract': True,
        'queryset_class': FeatureQuerySet
    }

    def to_feature(self):
        data = {
            'id': str(self.id),
            'type': self.type,
            'geometry': self.geometry,
            'properties': self.properties,
            'timestamp': str(self.id.generation_time)
        }
        return data

    def from_dict(self, data):
        self.geometry = data.get('geometry')
        self.properties = data.get('properties')


class Arena(Feature):
    confirmed = db.BooleanField(default=False)


class Match(Feature):
    active = db.BooleanField(default=True)


class Admin(db.Document):
    _pwd = db.StringField(db_field='pwd')

    @property
    def pwd(self):
        return self._pwd

    @pwd.setter
    def pwd(self, value):
        try:
            self._pwd = bcrypt.generate_password_hash(value.encode('utf-8'))
        except (ValueError, AttributeError):
            raise ValueError('Cant set password. Probably empty value')

    def auth(self, plaintext):
        try:
            return bcrypt.check_password_hash(self._pwd.encode('utf-8'), plaintext.encode('utf-8'))
        except (ValueError, AttributeError, KeyError):
            return False
