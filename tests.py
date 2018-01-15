#!/usr/bin/env python

import unittest

from hexarray import version
from hexarray.models.containers import Layer
from hexarray.models.coordinates import Hex


class HexarrayModelsCoordinatesHex(unittest.TestCase):

    def test_line_with_up_epsilon_is_correct(self):
        line = list(Hex(0, 1).line(Hex(2, 3), epsilon_type='up'))

        self.assertEqual(
            line,
            [Hex(0, 1), Hex(1, 1), Hex(1, 2), Hex(2, 2), Hex(2, 3)],
        )

    def test_line_with_down_epsilon_is_correct(self):
        line = list(Hex(0, 1).line(Hex(2, 3), epsilon_type='down'))

        self.assertEqual(
            line,
            [Hex(0, 1), Hex(0, 2), Hex(1, 2), Hex(1, 3), Hex(2, 3)],
        )


class HexarrayModelsContainersLayer(unittest.TestCase):

    def test_layer_hashes_correctly(self):
        layer_1, layer_2 = Layer(), Layer()

        value = object()
        test_dict = {layer_1: value}

        self.assertEqual(test_dict[layer_2], value)

    def test_layer_matches_kwargs(self):
        layer = Layer()

        self.assertEqual(layer.matches_kwargs(layer=0), True)
        self.assertEqual(layer.matches_kwargs(layer__lt=1), True)


class HexarrayVersion(unittest.TestCase):

    def setUp(self):
        self.version = version()

    def test_version_returns_tuple(self):
        self.assertIsInstance(self.version, tuple)

    def test_version_has_release_feature_fix_format(self):
        self.assertEqual(len(self.version), 3)


unittest.main()
