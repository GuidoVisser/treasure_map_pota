import cv2
import numpy as np
from math import sin, cos

from utils import Position
from constants import MAP_SIZE, MAP_WIDTH

TREASURE_POSITION = Position(0.35, 0.35)

class Icon(object):
    def __init__(self, 
                 true_position: Position, 
                 radius_func: object, 
                 angle_func: object,
                 img_path: str = "") -> None:
        super().__init__()
       
        self.true_position = true_position
        self.radius_func = radius_func
        self.angle_func = angle_func
        
        center_x = true_position.x - radius_func(TREASURE_POSITION) * cos(angle_func(TREASURE_POSITION))
        center_y = true_position.y - radius_func(TREASURE_POSITION) * sin(angle_func(TREASURE_POSITION))
        self.center_position = Position(center_x, center_y, mode="absolute")

    def location(self, position: Position):
        
        radius = self.radius_func(position)
        angle  = self.angle_func(position)

        u = int(radius * cos(angle) + self.center_position.x)
        v = int(radius * sin(angle) + self.center_position.y)

        return (u, v)


class Map(object):
    def __init__(self, 
                 map_path: str,
                 icons: list) -> None:
        super().__init__()

        self.map = cv2.resize(cv2.imread(map_path), MAP_SIZE)

        cv2.circle(self.map, TREASURE_POSITION.pos, 40, (255, 255, 0), thickness=-1)
        self.icons = icons

    def render(self, position):

        map = self.map.copy()
        cv2.namedWindow("test", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("test", MAP_SIZE[0] // 4, MAP_SIZE[1] // 4)

        cv2.circle(map, position.pos, 40, (0, 255, 0), thickness=-1)

        for icon in self.icons:
            uv = icon.location(position)
            cv2.circle(map, icon.true_position.pos, 40, (0, 0, 255), thickness=-1)
            cv2.circle(map, uv, 40, (255, 0, 0), thickness=-1)
        cv2.imshow("test", map)
        cv2.waitKey(0)


if __name__ == "__main__":
    map_path = "images/dessarin_valley_dm.jpg"
    icons = [
        Icon(Position(0.5, 0.2),
             lambda pos: MAP_WIDTH * (0.1 + 0.01 * cos(pos.x / 20)),
             lambda pos: 3 * (2 * pos.x + pos.y) / MAP_WIDTH),
        Icon(Position(0.65, 0.35),
             lambda pos: MAP_WIDTH * (0.05 + 0.1 * cos(pos.x / 10)),
             lambda pos: 7 * (pos.x + 2 * pos.y) / MAP_WIDTH + 2),
        Icon(Position(0.45, 0.55),
             lambda pos: MAP_WIDTH * (0.3 + 0.15 * cos(4.5 * pos.x / 100)),
             lambda pos: 9 * (pos.x + pos.y) / MAP_WIDTH + 3.5),
        Icon(Position(0.535, 0.485),
             lambda pos: MAP_WIDTH * (0.3 + 0.15 * cos(4.5 * pos.x / 100)),
             lambda pos: 9 * (pos.x + pos.y) / MAP_WIDTH + 3.5),
        Icon(Position(0.61, 0.57),
             lambda pos: MAP_WIDTH * (0.3 + 0.15 * cos(4.5 * pos.x / 100)),
             lambda pos: 9 * (pos.x + pos.y) / MAP_WIDTH + 3.5),
        # Icon(Position(0.8, 0.6),
        #      lambda pos: MAP_WIDTH * (0.3 + 0.15 * cos(4.5 * pos.x / 100)),
        #      lambda pos: 9 * (pos.x + pos.y) / MAP_WIDTH + 3.5),
    ]

    map = Map(map_path, icons)

    for i in np.linspace(0, 1, 700):
        pos = Position(i, i)
        map.render(pos)
        if i == 350:
            cv2.waitKey(1000)

    for i in np.linspace(0, 1, 700):
        pos = Position(1-i, i)
        map.render(pos)
        if i == 350:
            cv2.waitKey(1000)