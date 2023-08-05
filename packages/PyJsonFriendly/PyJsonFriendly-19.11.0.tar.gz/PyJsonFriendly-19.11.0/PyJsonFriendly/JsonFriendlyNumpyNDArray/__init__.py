import numpy as np

from json import JSONEncoder

JSONEncoder.default = lambda self, obj: {
            "type": "np.ndarray",
            "dtype": str(obj.dtype),
            "shape": obj.shape,
            "size": obj.size,
            "data": obj.tolist()
        } if isinstance(obj, np.ndarray) else getattr(obj.__class__, '_as_json_friendly_obj', JSONEncoder.default)(obj)
