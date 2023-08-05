import json
import numpy as np
from unittest import TestCase
import PyJsonFriendly.JsonFriendlyNumpyNDArray


class TestJsonFriendlyNumpyNDArray(TestCase):
    def test_01(self):
        np_arr = np.asarray([1, 2, 3, 4])

        self.assertEqual(
            '{"type": "np.ndarray", "dtype": "int32", "shape": [4], "size": 4, "data": [1, 2, 3, 4]}',
            json.dumps(np_arr)
        )

        np_arr = np_arr.reshape((2, 2))
        self.assertEqual(
            '{"type": "np.ndarray", "dtype": "int32", "shape": [2, 2], "size": 4, "data": [[1, 2], [3, 4]]}',
            json.dumps(np_arr)
        )

    def test_02(self):
        np_arr = np.asarray([1, 2, 3, 4], dtype=np.int64)
        self.assertEqual(
            '{"type": "np.ndarray", "dtype": "int64", "shape": [4], "size": 4, "data": [1, 2, 3, 4]}',
            json.dumps(np_arr)
        )

        np_arr = np_arr.reshape((2, 2))
        self.assertEqual(
            '{"type": "np.ndarray", "dtype": "int64", "shape": [2, 2], "size": 4, "data": [[1, 2], [3, 4]]}',
            json.dumps(np_arr)
        )

    def test_03(self):
        np_arr = np.asarray([1, 2, 3, 4], dtype=np.float64)
        self.assertEqual(
            '{"type": "np.ndarray", "dtype": "float64", "shape": [4], "size": 4, "data": [1.0, 2.0, 3.0, 4.0]}',
            json.dumps(np_arr)
        )

        np_arr = np_arr.reshape((2, 2))
        self.assertEqual(
            '{"type": "np.ndarray", "dtype": "float64", "shape": [2, 2], "size": 4, "data": [[1.0, 2.0], [3.0, 4.0]]}',
            json.dumps(np_arr)
        )





