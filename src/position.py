from constants import MAP_SIZE

class Position(object):
    def __init__(self, x: int, y: int, mode="relative") -> None:
        super().__init__()
        
        assert mode in ["relative", "absolute"]
        self.mode = mode

        self.x = x
        self.y = y
        self.pos = (self.x, self.y)

    @property
    def x(self) -> int:
        if self.mode  == "absolute":
            return self._x
        elif self.mode == "relative":
            return round(MAP_SIZE[0] * self._x)

    @x.setter
    def x(self, val) -> None:
        self._x = val

    @property
    def y(self) -> int:
        if self.mode  == "absolute":
            return self._y
        elif self.mode == "relative":
            return round(MAP_SIZE[1] * self._y)
    
    @y.setter
    def y(self, val) -> None:
        self._y = val

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y, mode="absolute")