from werkzeug.routing import BaseConverter, ValidationError
import bson


class ObjectIDConverter(BaseConverter):
    def to_python(self, value):
        try:
            return bson.ObjectId(value)
        except (bson.errors.InvalidId, ValueError, TypeError):
            raise ValidationError()

    def to_url(self, value):
        return str(value)
