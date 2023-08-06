import json


class Serializer(json.JSONEncoder):
    # TODO(jay): added except for schema errors
    def default(self, o):
        try:
            return self.schema.validate(o.to_dict())
        except AttributeError:
            return super().default(o)
