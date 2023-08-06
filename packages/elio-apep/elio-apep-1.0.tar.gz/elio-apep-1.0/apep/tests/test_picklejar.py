# -*- coding: utf-8 -*-
import unittest
from apep.picklejar import PickleJar


class TestPickling(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.jAR = PickleJar("apep/tests", "PickleJarTest")
        self.jAR.wipe()

    def tearDown(self):
        super().tearDown()
        self.jAR.wipe()

    def test_cmdata_jar_is_saved(self):
        data = {"lemons": 3, "onions": 300}
        saved_data = self.jAR.pickle(data)
        self.assertEqual(saved_data, data)
        """Tests: `pickle` returns what you pickled."""
        saved_data = self.jAR.open()
        self.assertEqual(saved_data, data)
        """Tests: `open` opens what you pickled."""
        saved_data["lemons"] = 300
        self.jAR.pickle(saved_data)
        self.assertNotEqual(self.jAR.open(), data)
        """Tests: `open` opens saved_data."""

    def test_cmdata_jar_starts_ripe(self):
        self.assertFalse(self.jAR.ripe)

    def test_cmdata_jar_wipes(self):
        data = {"lemons": 3, "onions": 300}
        self.jAR.pickle(data)
        self.assertTrue(self.jAR.ripe)
        """Tests: Presence of pickle file."""
        self.jAR.wipe()
        self.assertFalse(self.jAR.ripe)
        """Tests: Absence of pickle file."""
