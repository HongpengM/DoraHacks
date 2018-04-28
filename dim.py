import numpy as np


class Dim(object):
    """docstring for Dim"""

    def __init__(self, x=None, y=None):
        super(Dim, self).__init__()
        if not x:
            self.x = 0
            self.y = 0
            return
        if y:
            self.x = x
            self.y = y
            self._update()
        else:
            if (isinstance(x, list) or isinstance(x, tuple)) and len(x) == 2:
                self.x = x[0]
                self.y = x[1]
            else:
                print('Dim param error')

    def _update(self):
        self.shape = (self.x, self.y)

    def shape(self):
        return self.shape

    def isSquare(self):
        if x != 0:
            return x == y
        else:
            print('(0, 0) Square')

    def minSquare(self):
        x = min(self.x, self.y)
        return Dim(x, x)

    def minSquareOffset(self):
        return self - self.minSquare()

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)

    def __neg__(self):
        return Dim(-self.x, -self.y)

    def __pos__(self):
        return Dim(self.x, self.y)

    def __add__(self, other):
        if isinstance(other, Dim):
            return Dim(self.x + other.x, self.y + other.y)
        else:
            return Dim(self.x + other, self.y + other)

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, Dim):
            return Dim(self.x - other.x, self.y - other.y)
        else:
            return Dim(self.x - other, self.y - other)

    def __rsub__(self, other):
        return self - other

    def __isub__(self, other):
        return Dim(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, Dim):
            return Dim(self.x * other.x, self.y * other.y)
        else:
            return Dim(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        return self * other

    def __div__(self, other):
        if isinstance(other, Dim):
            return Dim(self.x / other.x, self.y / other.y)
        else:
            return Dim(self.x / other, self.y / other)

    def __rdiv__(self, other):
        return self - other

    def __idiv__(self, other):
        return self - other

    def __gt__(self, other):
        if isinstance(other, Dim):
            return self.x > other.x or self.y > other.y
        else:
            return self.x > other or self.y > other

    def __lt__(self, other):
        if isinstance(other, Dim):
            return self.x < other.x or self.y < other.y
        else:
            return self.x < other or self.y < other

    def __repr__(self):
        txt = '(' + str(self.x) + ',' + str(self.y) + ')'
        return txt


if __name__ == '__main__':
    a = Dim(1, 1)
    b = Dim(2, 3)
    a += b
    print(a - b * a)
