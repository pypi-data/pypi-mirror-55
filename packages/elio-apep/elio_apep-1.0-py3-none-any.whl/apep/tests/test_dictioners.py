# -*- coding: utf-8 -*-
import unittest
from apep.dictioners import filter_and, filter_or, multikeysort

x1_A1_01A1 = {"f1": "x", "f2": "1", "f3": "A", "f4": "A1", "f5": "01A1"}
x1_A1_02A1 = {"f1": "x", "f2": "1", "f3": "A", "f4": "A1", "f5": "02A1"}
x1_A1_03A1 = {"f1": "x", "f2": "1", "f3": "A", "f4": "A1", "f5": "03A1"}
y2_A2_01A2 = {"f1": "y", "f2": "2", "f3": "A", "f4": "A2", "f5": "01A2"}
y2_A2_02A2 = {"f1": "y", "f2": "2", "f3": "A", "f4": "A2", "f5": "02A2"}
y3_A3_01A3 = {"f1": "y", "f2": "3", "f3": "A", "f4": "A3", "f5": "01A3"}
y3_A3_02A3 = {"f1": "y", "f2": "3", "f3": "A", "f4": "A3", "f5": "02A3"}
x2_B1_01B1 = {"f1": "x", "f2": "2", "f3": "B", "f4": "B1", "f5": "01B1"}
x2_B1_02B1 = {"f1": "x", "f2": "2", "f3": "B", "f4": "B1", "f5": "02B1"}
x2_B1_03B1 = {"f1": "x", "f2": "2", "f3": "B", "f4": "B1", "f5": "03B1"}
y4_B2_01B2 = {"f1": "y", "f2": "4", "f3": "B", "f4": "B2", "f5": "01B2"}
y4_B2_02B2 = {"f1": "y", "f2": "4", "f3": "B", "f4": "B2", "f5": "02B2"}

json_db = [
    x1_A1_01A1,
    x1_A1_02A1,
    x1_A1_03A1,
    y2_A2_01A2,
    y2_A2_02A2,
    y3_A3_01A3,
    y3_A3_02A3,
    x2_B1_01B1,
    x2_B1_02B1,
    x2_B1_03B1,
    y4_B2_01B2,
    y4_B2_02B2,
]


class TestUtilsFilters(unittest.TestCase):
    def test_utils_filter_or(self):
        self.assertTrue(filter_or({"a": 1, "b": 2}, {"a": 1, "b": 2}))
        self.assertTrue(filter_or({"a": 1, "b": 2, "c": 3}, {"a": 1, "b": 2}))
        self.assertTrue(filter_or({"a": 1, "b": 2}, {"a": 2, "b": 2}))
        self.assertTrue(filter_or({"a": 1, "b": 2}, {"a": 1, "b": 1}))
        self.assertTrue(filter_or({"a": 1, "b": 2, "c": 3}, {"a": 1, "b": 2}))
        self.assertFalse(filter_or({"a": 1, "b": 2, "c": 3}, {"a": 4, "b": 5}))
        self.assertFalse(filter_or({"a": 1, "b": 2}, {"a": 2, "b": 1}))
        self.assertFalse(filter_or({}, {"a": 1, "b": 2}))
        self.assertFalse(filter_or({"a": 1, "b": 2}, {}))

    def test_utils_filter_and(self):
        self.assertTrue(filter_and({"a": 1, "b": 2}, {"a": 1, "b": 2}))
        self.assertTrue(filter_and({"a": 1, "b": 2, "c": 3}, {"a": 1, "b": 2}))
        self.assertFalse(filter_and({"a": 1, "b": 2}, {"a": 2, "b": 2}))
        self.assertFalse(filter_and({"a": 1, "b": 2}, {"a": 1, "b": 1}))
        self.assertFalse(filter_and({"a": 1, "b": 2}, {"a": 1, "b": 2, "c": 3}))
        self.assertFalse(filter_and({}, {"a": 1, "b": 2}))
        self.assertFalse(filter_and({"a": 1, "b": 2}, {}))


class TestUtilsMultiColumnSort(unittest.TestCase):
    def test_utils_multikeysort(self):
        self.assertListEqual(
            json_db,
            multikeysort(
                [
                    json_db[mixed]
                    for mixed in [9, 5, 2, 6, 8, 3, 7, 11, 4, 10, 1, 0]
                ],
                ["f3", "f4", "f5", "f1", "f2"],
            ),
        )
        self.assertListEqual(
            json_db,
            multikeysort(
                [
                    json_db[mixed]
                    for mixed in [3, 7, 11, 4, 0, 1, 2, 9, 5, 6, 10, 8]
                ],
                ["f3", "f4", "f5", "f1", "f2"],
            ),
        )
