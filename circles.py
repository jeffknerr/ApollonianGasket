"""
Circle class for gasket drawing.

J. Knerr
May 2021
"""


class Circle():
    """circle objects"""

    def __init__(self, x, y, radius):
        """construct, given xy coords and radius"""
        self.x = x
        self.y = y
        self.radius = radius


    def getX(self): return self.x
    def getY(self): return self.y
    def getR(self): return self.radius

    def __repr__(self):
        """every class should have one..."""
        # thanks to Dan Bader for this!
        return (f'{self.__class__.__name__}('
                f'{self.x!r}, {self.y!r}, {self.radius!r})')

    def __hash__(self):
        """hash the data for easy comparing"""
        strcircle = "x:%.4f y:%.4f r:%.4f" % (self.x, self.y, self.radius)
        self._hash = hash(strcircle)
        return self._hash


    def __eq__(self, other):
        """for testing if two objects are equal"""
        return hash(self) == hash(other)


def main():
    """test code for the class"""
    C1 = Circle(1,2,4)
    print(C1)
    C2 = Circle(0.5,2.6,8)
    print(C2)
    C3 = Circle(1.0,2,4.0)
    print(C3)
    assert(C1==C3)
    print(C3.getX(), C3.getY(), C3.getR())
    print("all tests passed!")


if __name__ == "__main__":
    main()
