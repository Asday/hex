import attr


class Map(object):

    def __init__(self, layers=None):
        layers = layers or []

        self._map = {layer: {} for layer in layers}


@attr.s(frozen=True)
class Layer(object):
    name = attr.ib(default='')
    obstacle = attr.ib(default=False)
    layer = attr.ib(default=0)
