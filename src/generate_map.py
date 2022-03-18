import cv2
import numpy as np

from constants import MAP_SIZE, MAP_WIDTH, MAP_HEIGHT
from .position import Position
from .icons import Icon, ICONS

class Map(object):
    def __init__(self, 
                 map_path: str,
                 icons: list) -> None:
        super().__init__()

        self.map = cv2.cvtColor(cv2.resize(cv2.imread(map_path), MAP_SIZE), cv2.COLOR_RGB2BGR)
        self.icons = icons

    def place_icon(self, bg_img: np.array, icon: Icon, position: Position) -> np.array:
        
        if icon.show_true_position:
            icon_true_x, icon_true_y = icon.true_position.pos

            bg_img[icon_true_y:icon_true_y+icon.size[0], icon_true_x:icon_true_x+icon.size[1]] = (1 - icon.alpha) * bg_img[icon_true_y:icon_true_y+icon.size[0], icon_true_x:icon_true_x+icon.size[1]] + icon.alpha * (255 - icon.image)
        
        icon_x, icon_y = icon.location(position)

        icon_left   = max(-1 * icon_x, 0)
        icon_right  = min(icon.size[1], MAP_WIDTH - icon_x)
        icon_top    = max(-1 * icon_y, 0)
        icon_bottom = min(icon.size[0], MAP_HEIGHT - icon_y)

        if icon_right < icon.size[1]:
            x=1

        if icon_x < MAP_WIDTH and icon_x >= -icon.size[1] and icon_y < MAP_HEIGHT and icon_y >= -icon.size[0]:
            left   = max(0, icon_x)
            right  = min(MAP_WIDTH, icon_x + icon.size[1])
            top    = max(0, icon_y)
            bottom = min(MAP_HEIGHT, icon_y + icon.size[0])

            alpha      = icon.alpha[icon_top:icon_bottom, icon_left:icon_right]
            foreground = icon.image[icon_top:icon_bottom, icon_left:icon_right]

            bg_img[top:bottom, left:right] = (1 - alpha) * bg_img[top:bottom, left:right] + alpha * foreground

        return bg_img


    def render(self, position):

        map = self.map.copy()
        for icon in self.icons:
            map = self.place_icon(map, icon, position)
        
        return map


if __name__ == "__main__":
    map_path = "images/dessarin_valley_dm.jpg"
    
    map = Map(map_path, ICONS)

    img = map.render(Position(0.6237, 0.64175))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imshow("test", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()