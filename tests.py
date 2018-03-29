#!/usr/bin/env python

import unittest

from hexarray import version
from hexarray.models.containers import Layer, Map
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


class HexarrayModelsContainersMap(unittest.TestCase):

    def test_getitem_returns_correct_layers(self):
        layer_1, layer_2 = Layer(layer=1), Layer(layer=2)
        index = Hex(0, 0)

        map_ = Map([layer_1, layer_2])

        item = map_[index]

        self.assertIn(layer_1, item)
        self.assertIn(layer_2, item)

    def test_getitem_returns_correct_entity_ids(self):
        layer = Layer()
        index = Hex(0, 0)
        entity_ids = [0, 1, 2]

        map_ = Map([layer])

        # TODO:  Use an entity registration system instead.
        map_._map[layer][index] = entity_ids

        self.assertEqual(map_[index][layer], entity_ids)


class HexarrayModelsContainersLayer(unittest.TestCase):

    def test_layer_hashes_correctly(self):
        layer_1, layer_2 = Layer(), Layer()

        self.assertEqual(hash(layer_1), hash(layer_2))

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
