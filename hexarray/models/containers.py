import attr


class Map(object):
    """
    For storing static things.  Dynamic things should maintain their own
    position.
    """

    def __init__(self, layers=None):
        layers = layers or []

        self._map = {layer: {} for layer in layers}

    def get_layers_by_kwargs(self, **kwargs):
        return (
            layer for layer in self._map.keys()
            if layer.matches_kwargs(kwargs)
        )


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
