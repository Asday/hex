import threading

import attr

from ..utils import lazy_set_generator

from .exceptions import EntityInUseError


class Map(object):
    """
    Collections of entity IDs indexed by `Hex`es, indexed by `Layer`s.

    Also contains an entity pool within which to register entities to
    later place on, and move around, the map.
    """

    def __init__(self, layers=None):
        layers = layers or []

        self._map = {layer: {} for layer in layers}
        self._entity_pool = {}
        self._next_id = 0
        self._next_id_lock = threading.Lock()

    @property
    def all_active_entities(self):
        """
        Generator which produces every `entity_id` currently on the
        `Map`.

        Will report each `entity_id` a maximum of one time.
        """
        def generator():
            for layer_contents in self._map.values():
                for entity_ids in layer_contents.values():
                    for entity_id in entity_ids:
                        yield entity_id

        return lazy_set_generator(generator())

    def register_entity(self, entity, fail_silently=True):
        """
        Takes any object and registers it within the internal entity
        pool.

        If possible, sets `map_entity_id` on the object.  If it wasn't
        possible, and you'd like to see why, set `fail_silently=False`.

        Returns the created `entity_id`.
        """
        with self._next_id_lock:
            entity_id = self._next_id
            self._next_id += 1

        self._entity_pool[entity_id] = entity

        try:
            entity.map_entity_id = entity_id
        except Exception:
            if not fail_silently:
                raise

        return entity_id

    def deregister_entity(self, entity_id, validate=True):
        """
        Removes a previously registered entity from the internal entity
        pool.  Can only be accomplished if the entity doesn't exist on
        the map.

        For production, disable existence checks by setting
        `validate=False` for a performance boost.  You are not allowed
        to whine at me when you break your own game like that.

        Can raise `EntityInUseError`.

        Returns the deregistered entity.
        """
        if validate:
            if entity_id in self.all_active_entities:
                raise EntityInUseError(
                    f'Entity {self._entity_pool[entity_id]} (id'
                    f' {entity_id}) is currently in use.  The attempt'
                    f' to deregister it has failed.'
                )

        return self._entity_pool.pop(entity_id)

    def get_layers_by_kwargs(self, **kwargs):
        return (
            layer for layer in self._map.keys()
            if layer.matches_kwargs(kwargs)
        )

    def __getitem__(self, index):
        """
        `index` must be a `Hex`.

        Will always return a dict of `{Layer: [entity_id, ...]}`, even
        for indices out of bounds.
        """

        out = {}
        for layer, entities in self._map.items():
            out[layer] = entities.get(index)

        return out


@attr.s(frozen=True)
class Layer(object):
    name = attr.ib(default='')
    obstacle_movement = attr.ib(default=False)
    obstacle_los = attr.ib(default=False)
    layer = attr.ib(default=0)

    def matches_kwargs(self, **kwargs):
        for selector, value in kwargs.items():
            attribute, *method = selector.split('__')
            method = f'__{method[0] if len(method) else "eq"}__'

            if not getattr(getattr(self, attribute), method)(value):
                return False

        return True
