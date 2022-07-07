from constants import MAP_HEIGHT, MAP_WIDTH

from PyQt6.QtCore import QPointF

class Position(object):
    """Position object to easily compare and manipulate the positions of map elements

    Args:
        x (int): x coordinate
        y (int): y coordinate
        mode (str): can either be "relative" or "absolute". (NEVER change this after initialization)
            In "relative" mode the coordinates are internally defined on the interval [0,1]
            In "absolute" mode the coordinates are internally defined on the interval [0, MAP_SIZE]
    """
    def __init__(self, x: int, y: int, mode: str="relative") -> None:
        super().__init__()
        
        assert mode in ["relative", "absolute"]
        self.mode = mode

        self.x = x
        self.y = y

    @staticmethod
    def from_QPointF(qpos: QPointF):
        """generate a Position object with the coordinates of the given QPointF object

        Args:
            qpos (QPointF): PyQt6 position object relative to the map widget

        Returns:
            Position:  Instance of this class with the given coordinates
        """
        return Position(int(qpos.x()), int(qpos.y()), mode="absolute")

    @staticmethod
    def from_tuple(tuple: tuple, mode: str = "relative"):
        """generate a Position object with the coordinates of the given tuple

        Args:
            tuple (tuple): tuple of the for (x, y)
            mode (str, optional): specifies the mode of the position. Defaults to "relative"

        Returns:
            Position:  Instance of this class with the given coordinates
        """
        return Position(tuple[0], tuple[1], mode=mode)

    def is_in_bbox(self, left: int, right: int, top: int, bottom: int) -> bool:
        """Checks whether this position is contained in a given bounding box

        Args:
            left (int)  : left bound
            right (int) : right bound
            top (int)   : top bound
            bottom (int): bottom bound

        Returns:
            bool: True if this position is within the bounds
        """
        if self.x >= left and self.y >= top and self.x <=right and self.y <= bottom:
            return True
        else:
            return False

    @property
    def x(self) -> int:
        if self.mode  == "absolute":
            return self._x
        elif self.mode == "relative":
            return round(MAP_WIDTH * self._x)

    @x.setter
    def x(self, val: int) -> None:
        self._x = val

    @property
    def y(self) -> int:
        if self.mode  == "absolute":
            return self._y
        elif self.mode == "relative":
            return round(MAP_HEIGHT * self._y)
    
    @y.setter
    def y(self, val: int) -> None:
        self._y = val

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y, mode="absolute")
    
    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y, mode="absolute")