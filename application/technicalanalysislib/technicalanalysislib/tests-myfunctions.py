from unittest import TestCase
from FindAscendingTriangles import AscendingTriangles
import numpy as np


class TryTesting(TestCase):
    def test_always_passes(self):
        self.assertTrue(True)

    def test_always_fails(self):
        self.assertTrue(False)

    def test_import_static_csv_data(self):
        data = AscendingTriangles.import_static_csv_data()
        self.assertEquals(type(data), np.array())
        print(data)

    def test_clean_data(self):
        data = AscendingTriangles.import_static_csv_data()
        AscendingTriangles.clean_data(data)
        print(data[20])

    def test_pivot_id(self):
        data = AscendingTriangles.import_static_csv_data()
        data["pivot"] = data.apply(
            lambda x: AscendingTriangles.pivotid(data, x.name, 3, 3), axis=1
        )
