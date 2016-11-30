#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
from pyxray.parser.wikipedia import WikipediaElementNameParser

# Globals and constants variables.

class TestWikipediaElementNameParser(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.parser = WikipediaElementNameParser()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test__iter__(self):
        props = list(self.parser)
        self.assertGreater(2500, len(props))

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
