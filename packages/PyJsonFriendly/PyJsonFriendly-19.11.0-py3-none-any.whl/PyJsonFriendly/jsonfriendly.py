from abc import ABCMeta, abstractmethod
from json import JSONEncoder


class JsonFriendly(metaclass=ABCMeta):
    JSONEncoder.default = lambda self, obj: (setattr(JSONEncoder, "default_backup", JSONEncoder.default), getattr(obj.__class__, "_as_json_friendly_obj", JSONEncoder.default)(obj))[1]

    @abstractmethod
    def _as_json_friendly_obj(self):
        pass
