from ext import db


class Arena(db.Document):
    name = db.StringField()
    geometry = db.PointField()
    properties = db.DictField()