#!/usr/bin/env python

import unittest

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


unittest.main()
