import cv2
import numpy as np
from math import sin, cos

from constants import MAP_WIDTH, MAP_HEIGHT
from .position import Position

TREASURE_POSITION = Position(0.6558, 0.5755)

class Icon(object):
    def __init__(self, 
                 name,
                 true_position: Position, 
                 radius_func: object, 
                 angle_func: object,
                 img_path: str = "images/icons/brass.png",
                 img_offset: Position = Position(-0.02, -0.02),
                 show_true_position: bool = False) -> None:
     super().__init__()

     self.name = name
     self.true_position = true_position + img_offset
     self.show_true_position = show_true_position
     self.radius_func = radius_func
     self.angle_func = angle_func

     self.image = cv2.resize(cv2.imread(img_path, cv2.IMREAD_UNCHANGED), (int(0.04 * MAP_HEIGHT), int(0.04 * MAP_HEIGHT)))
     self.alpha = np.stack([(cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY) <= 128).astype(np.uint8)]*3, axis=2)

     self.alpha = cv2.dilate(self.alpha, kernel=np.ones((3,3), dtype=np.uint8), iterations=2)

     self.size = self.image.shape[0:2]
     
     center_x = true_position.x - radius_func(TREASURE_POSITION) * cos(angle_func(TREASURE_POSITION))
     center_y = true_position.y - radius_func(TREASURE_POSITION) * sin(angle_func(TREASURE_POSITION))
     self.center_position = Position(center_x, center_y, mode="absolute") + img_offset

    def location(self, position: Position):
        
          radius = self.radius_func(position)
          angle  = self.angle_func(position)

          u = int(radius * cos(angle) + self.center_position.x)
          v = int(radius * sin(angle) + self.center_position.y)

          return (u, v)

ICONS = [
     Icon("brass",
          Position(0.5, 0.2),
          lambda pos: MAP_WIDTH * 0.1,# (0.1 + 0.1 * cos(6 * (2 * pos.x + pos.y) / MAP_WIDTH)),
          lambda pos: -3 * (pos.y) / MAP_WIDTH,
          img_path = "images/icons/brass.png"),
     Icon("iron",
          Position(0.65, 0.35),
          lambda pos: MAP_WIDTH * 0.05,# * (0.05 + 0.1 * cos(pos.x / 10)),
          lambda pos: -7 * (pos.x) / MAP_WIDTH + 2,
          img_path = "images/icons/iron.png"),
     Icon("gold",
          Position(0.3813, 0.5535),
          lambda pos: MAP_WIDTH * 0.08,# * (0.3 + 0.15 * cos(4.5 * pos.x / 100)),
          lambda pos: -14 * (pos.x) / MAP_WIDTH + .5,
          img_path = "images/icons/gold.png",
          img_offset=Position(-0.02538, -0.02)),
     Icon("silver",
          Position(0.5555, 0.54925),
          lambda pos: MAP_WIDTH * 0.17,# * (0.3 + 0.15 * cos(4.5 * pos.x / 100)),
          lambda pos: -5 * (pos.y) / MAP_WIDTH + 3.5,
          img_path = "images/icons/electrum.png",
          img_offset=Position(-0.02538, -0.02)),
     Icon("platinum",
          Position(0.622222, 0.57125),
          lambda pos: MAP_WIDTH * 0.07,# * (0.3 + 0.15 * cos(4.5 * pos.x / 100)),
          lambda pos: -12 * (pos.x) / MAP_WIDTH + 1.5,
          img_path = "images/icons/platinum.png",
          img_offset=Position(-0.02538, -0.02)),
     Icon("Bridge",
          Position(0.5359, 0.48725),
          lambda pos: MAP_WIDTH * 0.15,# * (0.3 + 0.15 * cos(4.5 * pos.x / 100)),
          lambda pos: -13 * (pos.y) / MAP_WIDTH,
          img_path = "images/icons/cadmium.png",
          img_offset=Position(-0.02538, -0.02)),
     Icon("Shield",
          Position(0.47777, 0.52825),
          lambda pos: MAP_WIDTH * 0.22,# * (0.3 + 0.15 * cos(4.5 * pos.x / 100)),
          lambda pos: 6 * (pos.x) / MAP_WIDTH + 2.5,
          img_path = "images/icons/zinc.png",
          img_offset=Position(-0.03014, -0.00125)),
     Icon("Hammer",
          Position(0.50794, 0.58375),
          lambda pos: MAP_WIDTH * 0.22,# * (0.3 + 0.15 * cos(4.5 * pos.x / 100)),
          lambda pos: 8 * (pos.y) / MAP_WIDTH + 2.5,
          img_path = "images/icons/allomancy_2.png",
          img_offset=Position(-0.03014, -0.00125)),
     Icon("door",
          Position(.49701, .64014),
          lambda pos: MAP_WIDTH * 0.13,# * (0.3 + 0.15 * cos(4.5 * pos.x / 100)),
          lambda pos: 11 * (pos.x) / MAP_WIDTH + 3.5,
          img_path = "images/icons/tin.png",
          img_offset=Position(-.02538, -0.02625)),
     Icon("door",
          Position(0.37985, 0.6225),
          lambda pos: MAP_WIDTH * 0.3,# * (0.3 + 0.15 * cos(4.5 * pos.x / 100)),
          lambda pos: 7 * (pos.y) / MAP_WIDTH + .5,
          img_path = "images/icons/tin.png",
          img_offset=Position(-0.02538, -0.02625)),
     Icon("door",
          Position(0.45581, 0.60595),
          lambda pos: MAP_WIDTH * 0.17,# * (0.3 + 0.15 * cos(4.5 * pos.x / 100)),
          lambda pos: 10 * (pos.x * 4) / MAP_WIDTH + 1.5,
          img_path = "images/icons/tin.png",
          img_offset=Position(-0.02538, -0.02625)),
     Icon("door",
          Position(0.43366, 0.57175),
          lambda pos: MAP_WIDTH * 0.2,# * (0.3 + 0.15 * cos(4.5 * pos.x / 100)),
          lambda pos: 5 * (pos.y) / MAP_WIDTH + 5.5,
          img_path = "images/icons/tin.png",
          img_offset=Position(-0.02538, -0.02625)),
]