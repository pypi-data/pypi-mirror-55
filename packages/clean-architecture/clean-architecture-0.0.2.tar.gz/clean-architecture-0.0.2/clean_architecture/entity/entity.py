import abc
from enum import Enum
from datetime import datetime


class Entity:

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, adict):
        pass

    def entity2dict(self, entity):
        def _type_switcher(value):
            if isinstance(value, Entity):
                return self.entity2dict(value)
            elif isinstance(value, Enum):
                return value.name
            elif isinstance(value, dict):
                return value
            elif isinstance(value, datetime):
                return str(value)
            elif isinstance(value, list):
                if len(value) == 0:
                    return []
                else:
                    if all(isinstance(e, Entity) for e in value):
                        return [self.entity2dict(e) for e in value]
                    else:
                        return str(value)
            else:
                return value

        if isinstance(entity, list):
            if all(isinstance(elem, Entity) for elem in entity):
                return [self.entity2dict(elem) for elem in entity]
            else:
                return entity

        if not isinstance(entity, Entity):
            return entity

        to_serialize = vars(entity)
        return {key: _type_switcher(value) for key, value in to_serialize.items() if value is not None}

    def to_dict(self):
        return self.entity2dict(self)

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()