# -*- coding: utf-8 -*-
import unittest
from apep.numero import roundy, is_number


class TestNumero(unittest.TestCase):
    def test_roundy(self):
        num = 987654321.123456789
        testsets = [
            (4, 0.0001, 987654321.1235),
            (4, 0.0005, 987654321.1235),
            (8, 0.0000005, 987654321.123457),
            (8, 0.000000001, 987654321.1234568),
            (4, 0.001, 987654321.123),
            (4, 0.1, 987654321.1),
            (4, 0.5, 987654321.0),
        ]
        for tset in testsets:
            self.assertEqual(tset[2], roundy(num, tset[0], tset[1]))

    def test_is_number(self):
        testsets = [
            (0, True),
            (1, True),
            (10, True),
            (0.1, True),
            (1.1, True),
            (10.01, True),
            ("0", True),
            ("1", True),
            ("10", True),
            ("0.1", True),
            ("1.1", True),
            ("10.01", True),
            ("01", True),
            ("0000001.1", True),
            ("1,100", False),  # Should be true? Reg Expression to fix?
            ("1,100.001", False), # Should be true? Reg Expression to fix?
            ("1,1", False), # Yet: Should be false
            ("0a", False),
            ("0.1.1", False),
            ("A", False),
            ("one", False),
        ]
        for tset in testsets:
            self.assertEqual(tset[1], is_number(tset[0]))
