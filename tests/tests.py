#!/usr/bin/env python

import unittest

from hexarray import version
from hexarray.models.containers import Layer, Map
from hexarray.models.coordinates import Hex
from hexarray.models.exceptions import EntityInUseError


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

    def test_all_active_entities_returns_correct_ids(self):
        layer_1, layer_2 = Layer(layer=1), Layer(layer=2)
        map_ = Map([layer_1, layer_2])
        entity_1, entity_2, entity_3 = object(), object(), object()
        entity_1_id = map_.register_entity(entity_1)
        entity_2_id = map_.register_entity(entity_2)
        entity_3_id = map_.register_entity(entity_3)

        map_.spawn(entity_1_id, layer_1, Hex(0, 1))
        map_.spawn(entity_2_id, layer_1, Hex(0, 1))
        map_.spawn(entity_2_id, layer_2, Hex(0, 1))
        map_.spawn(entity_3_id, layer_2, Hex(0, 1))

        entity_ids = sorted(list(map_.all_active_entities))

        self.assertEqual(
            entity_ids,
            sorted([entity_1_id, entity_2_id, entity_3_id]),
        )

    def test_register_entity_reraises_correctly(self):
        map_ = Map()

        with self.assertRaises(AttributeError):
            map_.register_entity(int(), fail_silently=False)

        try:
            map_.register_entity(int())
        except Exception as e:
            self.fail(
                f'`Map().register_entity()` incorrectly raised an'
                f' exception:  {e}'
            )

    def test_deregister_entity_validates_correctly(self):
        layer = Layer()
        map_ = Map([layer])
        entity_1, entity_2 = object(), object()

        entity_1_id = map_.register_entity(entity_1)
        entity_2_id = map_.register_entity(entity_2)

        map_.spawn(entity_1_id, layer, Hex(0, 1))
        map_.spawn(entity_2_id, layer, Hex(0, 1))

        with self.assertRaises(EntityInUseError):
            map_.deregister_entity(entity_1_id)

        try:
            map_.deregister_entity(entity_1_id, validate=False)
        except Exception as e:
            self.fail(
                f'`Map().deregister_entity()` incorrectly raised an'
                f' exception:  {e}'
            )

    def test_move(self):
        layer = Layer()
        map_ = Map([layer])
        entity = object()

        entity_id = map_.register_entity(entity)

        map_.spawn(entity_id, layer, Hex(0, 1))

        self.assertEqual(map_[Hex(0, 1)][layer], [entity_id])

        map_.move(entity_id, layer, Hex(0, 1), Hex(2, 4))

        self.assertEqual(map_[Hex(0, 1)][layer], [])
        self.assertEqual(map_[Hex(2, 4)][layer], [entity_id])

    def test_move_raises_correctly(self):
        map_ = Map()

        with self.assertRaises(ValueError):
            map_.move(0, Layer(), None, None)

    def test_getitem_returns_correct_layers(self):
        layer_1, layer_2 = Layer(layer=1), Layer(layer=2)
        index = Hex(0, 0)

        map_ = Map([layer_1, layer_2])

        item = map_[index]

        self.assertIn(layer_1, item)
        self.assertIn(layer_2, item)

    def test_getitem_returns_correct_entity_ids(self):
        layer = Layer()
        map_ = Map([layer])
        index = Hex(0, 0)
        entity_1, entity_2 = object(), object()
        entity_1_id = map_.register_entity(entity_1)
        entity_2_id = map_.register_entity(entity_2)

        map_.spawn(entity_1_id, layer, index)
        map_.spawn(entity_2_id, layer, index)

        self.assertEqual(
            sorted(map_[index][layer]),
            sorted([entity_1_id, entity_2_id]),
        )


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
