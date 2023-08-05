import json
from unittest import TestCase

# import PyJsonFriendly
from PyJsonFriendly import JsonFriendly


class NotJsonFriendly:
    """
        Using ``json.dumps(o)`` where ``o`` is an object of ``NotJsonFriendly`` will fail with a ``TypeError``
        exception.
    """
    def __init__(self, field1, field2):
        self._field1 = field1
        self._field2 = field2


class DerivedJsonFriendly(JsonFriendly):
    """
        Using ``json.dumps(o)`` where ``o`` is an object of ``DerivedJsonFriendly`` will not fail. Since this class is
        derived from ``PyJsonFriendly`` you would be forced to implement ``_as_json_friendly_obj(self)`` within the
        class; or you must declare the class as an Abstract class, which means you would not be able to instantiate an
        object of it directly.
        you would need to add ``from PyJsonFriendly import PyJsonFriendly`` to your code as well.
        This is the preferred approach.
    """
    def __init__(self, field1, field2):
        self._field1 = field1
        self._field2 = field2

    def _as_json_friendly_obj(self):
        return {"field1": self._field1, "field2": self._field2}


class NonDerivedJsonFriendly:
    """
        Using ``json.dumps(o)`` where ``o`` is an object of ``NonDerivedJsonFriendly`` will not fail, as long as
        you have ``from PyJsonFriendly import PyJsonFriendly`` in your code and the object has implemented a method
        called: ``_as_json_friendly_obj(self):``.
        Unlike the ``DerivedJsonFriendly`` class, this class is not extending ``PyJsonFriendly``. Hence, you are not
        forced to implement the ``_as_json_friendly_obj(self):``. However, forgetting to implement this method in your
        class will result in failing calls to ``json.dumps(o)`` if ``o`` is an object
        of ``NonDerivedJsonFriendly``
    """
    def __init__(self, field1, field2):
        self._field1 = field1
        self._field2 = field2

    def _as_json_friendly_obj(self):
        return {"field1": self._field1, "field2": self._field2}


class JsonFriendlyNoneDictOutput(JsonFriendly):
    def __init__(self, field1, field2):
        self._field1 = field1
        self._field2 = field2

    def _as_json_friendly_obj(self):
        return [self._field1, self._field2]


class TestPyJsonFriendly(TestCase):
    def test_01(self):
        o = NotJsonFriendly(1, 2)
        with self.assertRaises(TypeError):
            json.dumps(o)

    def test_02(self):
        o = DerivedJsonFriendly(3, 4)
        self.assertEqual('{"field1": 3, "field2": 4}', json.dumps(o))

    def test_03(self):
        o = NonDerivedJsonFriendly(5, 6)
        self.assertEqual('{"field1": 5, "field2": 6}', json.dumps(o))

    def test_04(self):
        o = NotJsonFriendly(7, 8)
        with self.assertRaises(TypeError):
            json.dumps(o)

        # you could add the necessary function during the runtime as well. (A python thing)
        o.__class__._as_json_friendly_obj = lambda _: {"field1": _._field1, "field2": _._field2}
        self.assertEqual('{"field1": 7, "field2": 8}', json.dumps(o))

    def test_05(self):
        o = JsonFriendlyNoneDictOutput(9, 10)

        self.assertEqual('[9, 10]', json.dumps(o))


