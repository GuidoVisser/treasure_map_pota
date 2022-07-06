import cv2
import numpy as np
from math import sin, cos

from constants import MAP_WIDTH, MAP_HEIGHT
from .position import Position

TREASURE_POSITION = Position(0.6558, 0.5755)

class Icon(object):
     """Icon object that holds the image information of an icon that should be drawn on the map

     Args:
          name (str): name of the icon
          img_path (str): path to the image
          img_offset (Position): offset used to center the icon on a given position
          use_negative_image (bool): specifies whether to use a negative image for the icon
     """
     def __init__(self, 
                 name: str,
                 img_path: str = "images/icons/brass.png",
                 img_offset: Position = Position(-0.02, -0.02),
                 use_negative_image: bool = False) -> None:
          super().__init__()

          self.name = name
          self.image_path = img_path
          self.img_offset = img_offset

          img = cv2.resize(cv2.imread(img_path, cv2.IMREAD_UNCHANGED), (int(0.04 * MAP_HEIGHT), int(0.04 * MAP_HEIGHT)))
          self.alpha = img[:, :, 3:4] // 255
          self.image = img[:, :, 0:3]
          
          if use_negative_image:
               self.image = (255 - self.image)

          self.size = self.image.shape[0:2]      
     
     def position_on_map(self, position: Position) -> Position:
          """calculate the position of the icon on the map. An offset is applied to center the icon on the position

          Args:
              position (Position): position where Icon should be drawn

          Returns:
              Position: position of top-left corner of the icon, such that it is drawn centered on the input position
          """
          return position + self.img_offset


class PlayerPositionDependentIcon(Icon):
     """Icon object that adds functionality to the default Icon object to calculate the player dependent
     position of the icon on the map, as well as keep track of the true (hidden) position of the location.
     
     The position of the players is used to calculate a radius and angle that together specify a the position of the icon in circular coordinates along a closed path
          - In practice it's a good idea to keep the radius constant, otherwise it becomes too difficult to solve the map

     Args:
          name (str): name of the icon
          true_position (Position): the true position on the map of the hidden location
          radius_func (function: Position -> float): function that returns the radius of the displacement circle of the icon
          angle_func (function: Position -> float): function that returns the angle along the displacement circle of the icon
          img_path (str): path to the icon image
          img_offset (Position): offset used to center the icon on a given position
          show_true_position (bool): specifies whether the true position icon is drawn on the map
          
     """
     def __init__(self, 
                  name: str, 
                  true_position: Position, 
                  radius_func: object, 
                  angle_func: object, 
                  img_path: str = "images/icons/brass.png", 
                  img_offset: Position = Position(-0.02, -0.02), 
                  show_true_position: bool = False) -> None:
          
          super().__init__(name, img_path, img_offset)
          
          self.show_true_position = show_true_position
          self.true_position = true_position + img_offset
          self.true_position_icon = Icon(name + " (true position)", img_path, img_offset, use_negative_image=True)

          self.radius_func = radius_func
          self.angle_func  = angle_func
          
          center_x = true_position.x - radius_func(TREASURE_POSITION) * cos(angle_func(TREASURE_POSITION))
          center_y = true_position.y - radius_func(TREASURE_POSITION) * sin(angle_func(TREASURE_POSITION))
          self.center_position = Position(center_x, center_y, mode="absolute")
          
     def position_on_map(self, position: Position) -> Position:
          """calculate the position of the icon on the map, using the radius and angle functions and image offset

          Args:
              position (Position): position object defined on the treasure map

          Returns:
              position (Position): position on the treasure map where the icon should be drawn.
          """
          radius = self.radius_func(position)
          angle  = self.angle_func(position)

          u = int(radius * cos(angle) + self.center_position.x)
          v = int(radius * sin(angle) + self.center_position.y)

          return Position(u, v, mode="absolute") + self.img_offset

ICONS = (
     PlayerPositionDependentIcon("brass",
          Position(0.5, 0.2),
          lambda pos: MAP_WIDTH * 0.1,
          lambda pos: -3 * (pos.y) / MAP_WIDTH,
          img_path = "images/icons/brass.png"),
     PlayerPositionDependentIcon("iron",
          Position(0.65, 0.35),
          lambda pos: MAP_WIDTH * 0.05,
          lambda pos: -7 * (pos.x) / MAP_WIDTH + 2,
          img_path = "images/icons/iron.png"),
     PlayerPositionDependentIcon("gold",
          Position(0.3813, 0.5535),
          lambda pos: MAP_WIDTH * 0.08,
          lambda pos: -14 * (pos.x) / MAP_WIDTH + .5,
          img_path = "images/icons/gold.png",
          img_offset=Position(-0.02538, -0.02)),
     PlayerPositionDependentIcon("silver",
          Position(0.5555, 0.54925),
          lambda pos: MAP_WIDTH * 0.17,
          lambda pos: -5 * (pos.y) / MAP_WIDTH + 3.5,
          img_path = "images/icons/electrum.png",
          img_offset=Position(-0.02538, -0.02)),
     PlayerPositionDependentIcon("platinum",
          Position(0.622222, 0.57125),
          lambda pos: MAP_WIDTH * 0.07,
          lambda pos: -12 * (pos.x) / MAP_WIDTH + 1.5,
          img_path = "images/icons/platinum.png",
          img_offset=Position(-0.02538, -0.02)),
     PlayerPositionDependentIcon("Bridge",
          Position(0.5359, 0.48725),
          lambda pos: MAP_WIDTH * 0.15,
          lambda pos: -13 * (pos.y) / MAP_WIDTH,
          img_path = "images/icons/cadmium.png",
          img_offset=Position(-0.02538, -0.02)),
     PlayerPositionDependentIcon("Shield",
          Position(0.47777, 0.52825),
          lambda pos: MAP_WIDTH * 0.22,
          lambda pos: 6 * (pos.x) / MAP_WIDTH + 2.5,
          img_path = "images/icons/zinc.png",
          img_offset=Position(-0.03014, -0.00125)),
     PlayerPositionDependentIcon("Hammer",
          Position(0.50794, 0.58375),
          lambda pos: MAP_WIDTH * 0.22,
          lambda pos: 8 * (pos.y) / MAP_WIDTH + 2.5,
          img_path = "images/icons/allomancy_2.png",
          img_offset=Position(-0.03014, -0.00125)),
     PlayerPositionDependentIcon("door",
          Position(.49701, .64014),
          lambda pos: MAP_WIDTH * 0.13,
          lambda pos: 11 * (pos.x) / MAP_WIDTH + 3.5,
          img_path = "images/icons/tin.png",
          img_offset=Position(-.02538, -0.02625)),
     PlayerPositionDependentIcon("door",
          Position(0.37985, 0.6225),
          lambda pos: MAP_WIDTH * 0.3,
          lambda pos: 7 * (pos.y) / MAP_WIDTH + .5,
          img_path = "images/icons/tin.png",
          img_offset=Position(-0.02538, -0.02625)),
     PlayerPositionDependentIcon("door",
          Position(0.45581, 0.60595),
          lambda pos: MAP_WIDTH * 0.17,
          lambda pos: 10 * (pos.x * 4) / MAP_WIDTH + 1.5,
          img_path = "images/icons/tin.png",
          img_offset=Position(-0.02538, -0.02625)),
     PlayerPositionDependentIcon("door",
          Position(0.43366, 0.57175),
          lambda pos: MAP_WIDTH * 0.2,
          lambda pos: 5 * (pos.y) / MAP_WIDTH + 5.5,
          img_path = "images/icons/tin.png",
          img_offset=Position(-0.02538, -0.02625)),
)