from operator import pos
from typing import Tuple
import cv2
import numpy as np

from constants import MAP_SIZE, MAP_WIDTH, MAP_HEIGHT
from .position import Position
from .icons import PlayerPositionDependentIcon, Icon

class Map(object):
    """Map object with all functionality to render a treasure map based on the state of the GUI
    
    Args:
        map_path (str): path to the default treasure map image
        player_position_dependent_icons (Tuple[PlayerPositionDependentIcon]): tuple of Icon objects that belong to hidden locations
    """
    def __init__(self, 
                 map_path: str,
                 player_position_dependent_icons: Tuple[PlayerPositionDependentIcon]) -> None:
        super().__init__()

        self.background = cv2.cvtColor(cv2.resize(cv2.imread(map_path), MAP_SIZE), cv2.COLOR_RGB2BGR)
        self.player_position_dependent_icons = player_position_dependent_icons
        self.player_icon = Icon("player", img_path="images/icons/aluminium.png")

    def draw_icon_on_map(self, treasure_map: np.array, icon: Icon, position: Position):
        """Draw an icon on the treasure map using a back-to-front compositing technique

        Args:
            treasure_map (np.array): current image of the treasure map
            icon (Icon): Icon object that holds the icon image.
            position (Position): position on the treasure map of the icon
        """

        icon_left   = max(-1 * position.x, 0)
        icon_right  = min(icon.size[1], MAP_WIDTH - position.x)
        icon_top    = max(-1 * position.y, 0)
        icon_bottom = min(icon.size[0], MAP_HEIGHT - position.y)

        if position.is_in_bbox(-icon.size[1], MAP_WIDTH, -icon.size[0], MAP_HEIGHT):
            left   = max(0, position.x)
            right  = min(MAP_WIDTH, position.x + icon.size[1])
            top    = max(0, position.y)
            bottom = min(MAP_HEIGHT, position.y + icon.size[0])

            alpha      = icon.alpha[icon_top:icon_bottom, icon_left:icon_right]
            foreground = icon.image[icon_top:icon_bottom, icon_left:icon_right]

            treasure_map[top:bottom, left:right] = (1 - alpha) * treasure_map[top:bottom, left:right] + alpha * foreground

    def render(self, player_position: Position, show_player_icon: bool) -> np.array:
        """Generate an image of the treasure map based on the current position of the players.
        The order specifies which icons are drawn on top of others.

        Args:
            player_position (Position): current position of the players
            show_player_icon (bool): specifies whether to show the player icon

        Returns:
            np.array: image of the treasure map
        """

        # create a new image with only the background and add the necessary icons
        treasure_map = self.background.copy()
        
        # draw true position icons of hidden locations
        for icon in self.player_position_dependent_icons:
            if icon.show_true_position:
                self.draw_icon_on_map(treasure_map, icon.true_position_icon, icon.true_position)   
        
        # draw position dependent icons
        for icon in self.player_position_dependent_icons:
            icon_position = icon.position_on_map(player_position)
            self.draw_icon_on_map(treasure_map, icon, icon_position)
            
        # draw player icon
        if show_player_icon:
            icon_position = self.player_icon.position_on_map(player_position)
            self.draw_icon_on_map(treasure_map, self.player_icon, icon_position)

        return treasure_map
