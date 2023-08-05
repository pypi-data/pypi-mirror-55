# PyJsonFriendly

PyJsonFriend facilitates conversion of custom made classes to JSON String using json.dumps


## Examples
### Example 1: Failing Example
Let's say you have the following class:
```python
class NotJsonFriendly:
    def __init__(self, field1, field2):
        self._field1 = field1
        self._field2 = field2
```

Now if you create an object of type ``NotJsonFriendly`` and try to make a JSON string out
of it by passing it to ``json.dumps``, you would get a ``TypeError``:

```commandline
>>> o = NotJsonFriendly(1, 2)
>>> json.dumps(o)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File ".../lib/python3.7/json/__init__.py", line 231, in dumps
    return _default_encoder.encode(obj)
  File ".../lib/python3.7/json/encoder.py", line 199, in encode
    chunks = self.iterencode(o, _one_shot=True)
  File ".../lib/python3.7/json/encoder.py", line 257, in iterencode
    return _iterencode(o, 0)
  File ".../lib/python3.7/json/encoder.py", line 179, in default
    raise TypeError(f'Object of type {o.__class__.__name__} '
TypeError: Object of type NotJsonFriendly is not JSON serializable

```

### Example 2: Deriving from ``JsonFriendly``
While implementing your class, you could add ``JsonFriendly`` as one of the basis. In another words, if 
your custom build object/class extends ``JsonFriendly``, then you could pass your object to ``json.dumps``. 
Let's say we have the following class:

```python
from PyJsonFriendly import JsonFriendly
class DerivedJsonFriendly(JsonFriendly):
    def __init__(self, field1, field2):
        self._field1 = field1
        self._field2 = field2
    
    # You would need to add the following method
    def _as_json_friendly_obj(self):
        return {"field1": self._field1, "field2": self._field2}
```

``JsonFriendly`` is an abstract class, which has only one abstract method called: ``_as_json_friendly_obj``.
Therefore, you wold need to implement this method as part of your class. Forgetting to do that you would get
an error or you are required to declare your class an abstract class as well. You could not instantiate an
object from an abstract class. Extending your classes from ``JsonFriendly`` is the recommended way,
because it prevents you from accidentally forgetting to implement the required method mentioned above, or
implementing it with wrong name.

Here is an example of using the above class which is json friendly:

```commandline
>>> o = DerivedJsonFriendly(3,4)
>>> json.dumps(o)
'{"field1": 3, "field2": 4}'
```

### Example 3: Not Deriving from ``JsonFriendly`` but not failing ``json.dumps``
if you have already imported ``JsonFriendly`` in your code, then any object containing 
``as_json_friendly_obj`` method will work properly with ``json.dumps``. Here is an example:

```python
class NonDerivedJsonFriendly:
    def __init__(self, field1, field2):
        self._field1 = field1
        self._field2 = field2
    
    def _as_json_friendly_obj(self):
        return {"field1": self._field1, "field2": self._field2}

```

Now if you use an object of this class you will get:

```commandline
>>> o = NonDerivedJsonFriendly(5, 6)


>>> # The following command would fail because we have not yet imported JsonFriendly
... json.dumps(o)  
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/mabouali/miniconda3/envs/PyJsonFriendly/lib/python3.7/json/__init__.py", line 231, in dumps
    return _default_encoder.encode(obj)
  File "/Users/mabouali/miniconda3/envs/PyJsonFriendly/lib/python3.7/json/encoder.py", line 199, in encode
    chunks = self.iterencode(o, _one_shot=True)
  File "/Users/mabouali/miniconda3/envs/PyJsonFriendly/lib/python3.7/json/encoder.py", line 257, in iterencode
    return _iterencode(o, 0)
  File "/Users/mabouali/miniconda3/envs/PyJsonFriendly/lib/python3.7/json/encoder.py", line 179, in default
    raise TypeError(f'Object of type {o.__class__.__name__} '
TypeError: Object of type NonDerivedJsonFriendly is not JSON serializable


>>> from PyJsonFriendly import JsonFriendly
>>> # However, the following command will work just fine; because we have imported the JsonFriendly
... json.dumps(o)  
'{"field1": 5, "field2": 6}'
```

Although, this would work, however, you are not prompted/notified to implement ``_as_json_friendly_obj``
in your class. And if you forget to implement that function then passing your object to ``json.dumps``
will lead to raising a ``TypeError`` exception. Also you could not use the ``isinstance`` method to 
successfully check if you could pass your object to ``json.dumps``:

```commandline
>>> o1 = DerivedJsonFriendly(3, 4)
>>> o2 = NonDerivedJsonFriendly(5, 6)
>>> isinstance(o1,PyJsonFriendly)
True
>>> isinstance(o2,PyJsonFriendly)
False
```

Although, you could still use ``hasattr`` method, but this is not so appealing:

```commandline
>>> hasattr(o1, "_as_json_friendly_obj")
True
>>> hasattr(o2, "_as_json_friendly_obj")
True
```

### Example 4: Making objects ``JsonFriendly`` during the runtime
What if you are not the author of the object; however, you want to make them ``JsonFriendly``? Python allows
you to amend the class definition during the runtime. Check the following example:


```commandline
>>> from PyJsonFriendly import JsonFriendly
>>> o = NotJsonFriendly(7, 8)
>>> # Any Attempt to use json.dumps(o) will fail. Because o is not JsonFriendly and
... # does not implement _as_json_friendly_obj
... # Let's modify the object though during the runtime:
... o.__class__._as_json_friendly_obj = lambda _: {"field1": _._field1, "field2": _._field2}
>>> json.dumps(o)
'{"field1": 7, "field2": 8}'
```

### Example 5: ``_as_json_friendly_obj`` does not need to return a dictionary
Note that ``_as_json_friendly_obj`` does not need to return a dictionary. You could return anything that
python's ``json`` accepts. For a table showing the objects that are accepted by ``json`` package by default
click [here](https://docs.python.org/3/library/json.html#json.JSONEncoder). The following is an example:

```python
from PyJsonFriendly import JsonFriendly
class JsonFriendlyNoneDictOutput(JsonFriendly):
    def __init__(self, field1, field2):
        self._field1 = field1
        self._field2 = field2

    def _as_json_friendly_obj(self):
        return [self._field1, self._field2]
```

This would also work as follows:

```commandline
>>> o = JsonFriendlyNoneDictOutput(9, 10)
>>> json.dumps(o)
'[9, 10]'
```

## Bonuses 
### JSON Friendly Numpy NDArray
Calling ``json.dumps`` on a ``numpy.ndarray`` would result into failure. 

```commandline
>>> np_arr = np.asarray([1, 2, 3, 4])
>>> json.dumps(np_arr)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "E:\ProgramData\Anaconda3\envs\PyJsonFriendly\lib\json\__init__.py", line 231, in dumps
    return _default_encoder.encode(obj)
  File "E:\ProgramData\Anaconda3\envs\PyJsonFriendly\lib\json\encoder.py", line 199, in encode
    chunks = self.iterencode(o, _one_shot=True)
  File "E:\ProgramData\Anaconda3\envs\PyJsonFriendly\lib\json\encoder.py", line 257, in iterencode
    return _iterencode(o, 0)
  File "E:\ProgramData\Anaconda3\envs\PyJsonFriendly\lib\json\encoder.py", line 179, in default
    raise TypeError(f'Object of type {o.__class__.__name__} '
TypeError: Object of type ndarray is not JSON serializable
```

If for whatever reason, you are interested to turn your ``numpy.ndarray`` into a json friendly,
all you need to do is import ``PyJsonFriendly.JsonFriendlyNumpyNDArray``, as follow:

```commandline
import PyJsonFriendly.JsonFriendlyNumpyNDArray
>>> json.dumps(np_arr)
'{"type": "np.ndarray", "dtype": "int32", "shape": [4], "size": 4, "data": [1, 2, 3, 4]}'


>>> np_arr = np_arr.reshape((2,2))
>>> json.dumps(np_arr)
'{"type": "np.ndarray", "dtype": "int32", "shape": [2, 2], "size": 4, "data": [[1, 2], [3, 4]]}'
```



  


