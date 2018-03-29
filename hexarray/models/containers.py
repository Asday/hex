import attr


class Map(object):
    """
    Collections of entity IDs indexed by `Hex`es, indexed by `Layer`s.
    """

    def __init__(self, layers=None):
        layers = layers or []

        self._map = {layer: {} for layer in layers}

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
