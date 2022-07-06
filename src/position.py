from constants import MAP_HEIGHT, MAP_WIDTH

from PyQt6.QtCore import QPointF

class Position(object):
    def __init__(self, x: int, y: int, mode="relative") -> None:
        super().__init__()
        
        assert mode in ["relative", "absolute"]
        self.mode = mode

        self.x = x
        self.y = y
        self.pos = (self.x, self.y)

    @staticmethod
    def from_QPointF(qpos: QPointF):
        return Position(int(qpos.x()), int(qpos.y()), mode="absolute")

    @property
    def x(self) -> int:
        if self.mode  == "absolute":
            return self._x
        elif self.mode == "relative":
            return round(MAP_WIDTH * self._x)

    @x.setter
    def x(self, val) -> None:
        self._x = val

    @property
    def y(self) -> int:
        if self.mode  == "absolute":
            return self._y
        elif self.mode == "relative":
            return round(MAP_HEIGHT * self._y)
    
    @y.setter
    def y(self, val) -> None:
        self._y = val

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y, mode="absolute")
    
    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y, mode="absolute")
        
    def is_in_bbox(self, left, right, top, bottom):
        if self.x >= left and self.y >= top and self.x <=right and self.y <= bottom:
            return True
        else:
            return False