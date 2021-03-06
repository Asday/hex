import random

from ..utils import lazy_set_generator, lerp


class Hex(object):
    _addition_error = NotImplementedError(
        f'You must provide a Hex subclass for addition.')
    _multiplication_error = NotImplementedError(
        f'This Hex can only be multiplied by a scalar.')

    def __init__(self, q, r):
        self.q = q
        self.r = r

    @property
    def x(self):
        return self.q

    @property
    def y(self):
        return -self.q -self.r  # noqa

    @property
    def z(self):
        return self.r

    def __str__(self):
        return f'{self.__class__.__name__}({self.q}, {self.r})'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.q == other.q and self.r == other.r

    def __hash__(self):
        return hash((self.q, self.r))

    def __add__(self, other):
        try:
            return self.__class__(self.q + other.q, self.r + other.r)
        except AttributeError:
            raise self._addition_error

    def __iadd__(self, other):
        try:
            self.q, self.r = self.q + other.q, self.r + other.r
        except AttributeError:
            raise self._addition_error

        return self

    def __mul__(self, other):
        try:
            return self.__class__(self.q * other, self.r * other)
        except TypeError:
            raise self._multiplication_error

    def __imul__(self, other):
        try:
            self.q, self.r = self.q * other, self.r * other
        except TypeError:
            raise self._multiplication_error

        return self

    @classmethod
    def from_cube(cls, x, y, z):
        return cls(x, z)

    def distance(self, to):
        return (
            abs(self.x - to.x)
            + abs(self.y - to.y)
            + abs(self.z - to.z)
        ) / 2

    def lerp(self, to, proportion):
        return self.__class__.from_cube(
            lerp(self.x, to.x, proportion),
            lerp(self.y, to.y, proportion),
            lerp(self.z, to.z, proportion),
        )

    def snap(self, in_place=False):
        results = {
            coord: {'original': getattr(self, coord)}
            for coord in ('x', 'y', 'z')
        }

        for coord in results.values():
            coord['rounded'] = round(coord['original'])

        if sum((coord['rounded'] for coord in results.values())) != 0:
            # We need to normalise the result.
            for coord in results.values():
                coord['delta'] = abs(coord['rounded'] - coord['original'])

            outlier_key = max(
                results.items(), key=lambda result: result[1]['delta'])[0]

            outlier = results.pop(outlier_key)
            outlier['rounded'] = sum(
                -coord['rounded'] for coord in results.values())

            results[outlier_key] = outlier

        if not in_place:
            return self.__class__.from_cube(
                *(results[coord]['rounded'] for coord in ('x', 'y', 'z')))

        self.q = results['x']['rounded']
        self.r = results['z']['rounded']

    def line(self, to, epsilon_type=None):
        epsilon = EPSILON_TYPES[epsilon_type]
        if callable(epsilon):
            epsilon = epsilon()

        to += epsilon

        samples = int(self.distance(to)) + 1

        return lazy_set_generator(
            self.lerp(to, (1 / samples) * sample).snap()
            for sample in range(samples + 1)
        )


DIRECTIONS = {
    'ul': Hex(+1, +0),
    'ur': Hex(+1, -1),
    'ml': Hex(-1, +0),
    'mr': Hex(+1, +0),
    'dl': Hex(-1, +1),
    'dr': Hex(+0, +1),
}

DIAGONALS = {
    'cu': Hex(+1, -2),
    'ul': Hex(-1, +1),
    'ur': Hex(+2, -1),
    'dl': Hex(-2, +1),
    'dr': Hex(+1, +1),
    'cd': Hex(-1, +2),
}


EPSILON_TYPES = {
    None: Hex(0, 0),
    'up': DIAGONALS['cu'] * 1e-6,
    'down': DIAGONALS['cd'] * 1e-6,
    'random': lambda: random.choice(
        (EPSILON_TYPES['up'], EPSILON_TYPES['down'])),
}
