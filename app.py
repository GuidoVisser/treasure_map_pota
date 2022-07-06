from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap, QImage, QIcon, QMouseEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget
import cv2
import numpy as np
from os import path

from constants import MAP_WIDTH, MAP_HEIGHT, MAP_PATH, OUT_DIR
from src.position import Position
from src.generate_map import Map
from src.icons import Icon, ICONS
from src.utils import generate_filename

class MainWindow(QMainWindow):
    """Main window widget. All subwidgets are declared here.
    """
    def __init__(self, treasure_map: Map, out_dir: str) -> None:
        super().__init__()
        
        # Window properties
        self.setWindowTitle("Treasure Map")
        self.setFixedSize(QSize(int(MAP_WIDTH * 1.3) + 1, int(MAP_HEIGHT * 1.1)))
        self.out_dir = out_dir
        
        # Map widget
        self.map_widget = MapWidget(treasure_map)

        # Icon button widgets
        self.icon_buttons = []
        for icon in self.map_widget.treasure_map.player_position_dependent_icons:
            button = IconButton(icon)
            button.clicked.connect(button.set_true_position_visibility)
            button.clicked.connect(self.map_widget.update_map)
            self.icon_buttons.append(button)
        
        # Export button
        export_button = ExportButton()
        export_button.clicked.connect(self.export_map)
        
        # Create button layout
        button_layout = QVBoxLayout()
        for button in self.icon_buttons:
            button_layout.addWidget(button)
        button_layout.addWidget(export_button)

        button_sidebar = QWidget()
        button_sidebar.setLayout(button_layout)

        # create main layout
        main_layout = QHBoxLayout()
        # this aligns the cursor position to the Position objects
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.addWidget(self.map_widget)
        main_layout.addWidget(button_sidebar)
        
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        
        self.setCentralWidget(main_widget)
        
    def export_map(self):
        """Export the image of the map
        """
        map_img = self.map_widget.get_map_image(show_player_icon=False)
        map_img = cv2.cvtColor(map_img, cv2.COLOR_RGB2BGR)
        
        savepath = generate_filename(self.out_dir + "out.png", 0)
        cv2.imwrite(savepath, map_img)

        
class IconButton(QPushButton):
    """Button widget that keeps track if the hidden location icon should be shown on the map
    """
    def __init__(self, icon: Icon) -> None:
        super().__init__(icon.name)

        self.setCheckable(True)
        self.setChecked(False)
        
        self.icon = icon
        
        self.setIcon(QIcon(icon.image_path))
        self.setIconSize(QSize(MAP_WIDTH // 15, MAP_WIDTH // 15))

    def set_true_position_visibility(self, checked):
        self.icon.show_true_position = checked

class ExportButton(QPushButton):
    """Button widget for exporting the treasure map
    """
    def __init__(self) -> None:
        super().__init__("Export")
        
        self.setIcon(QIcon("./images/export.png"))
        self.setIconSize(QSize(MAP_WIDTH // 40, MAP_WIDTH // 40))


class MapWidget(QLabel):
    """Widget that keeps track of the players' position, generates and shows a treasure map based on that position, and
    contains all functionality to change the players' position.
    """
    def __init__(self, treasure_map) -> None:
        super().__init__()
        
        self.player_position = Position(183, 503, mode="absolute")
        self.treasure_map = treasure_map
        
        self.update_map()
        
        self.player_icon_is_selected = False
        self.mouse_offset_from_player_position = Position(0, 0)

    def update_map(self) -> None:
        """generate a new image for the Map widget and update the widget
        """
        map_img = self.get_map_image()
        self.setPixmap(QPixmap.fromImage(QImage(map_img, 
                                                MAP_WIDTH,
                                                MAP_HEIGHT, 
                                                map_img.strides[0], 
                                                QImage.Format.Format_RGB888)))

    def get_map_image(self, show_player_icon=True) -> np.array:
        """return the image of the background map with all visible icons

        Args:
            show_player_icon (bool, optional): specifies whether the player icon should be added to the image. Defaults to True.

        Returns:
            np.array: np.array (W, H, C) with the pixelvalues of the image
        """
        return self.treasure_map.render(self.player_position, show_player_icon)

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        """Check if the player icon is selected and if so move it and update the map until it is no longer selected.

        Args:
            ev (QMouseEvent): PyQt6 mouse event
        """
        
        pos = Position.from_QPointF(ev.position())
        if self.player_icon_is_selected:
            self.player_position = pos - self.mouse_offset_from_player_position
            
            self.player_position.x = min(self.player_position.x, MAP_WIDTH)
            self.player_position.x = max(self.player_position.x, 0)
            self.player_position.y = min(self.player_position.y, MAP_HEIGHT)
            self.player_position.y = max(self.player_position.y, 0)
            
            self.update_map()
            
    def mousePressEvent(self, ev: QMouseEvent) -> None:
        """Check if the current mouse position is within the bounding box of the player icon and
        and store this as a boolean as well as the offset to the center of the icon

        Args:
            ev (QMouseEvent): PyQt6 mouse event
        """
        # get the position of the mouse
        pos = Position.from_QPointF(ev.position())
        
        # check if the mouse is on the player icon
        if pos.is_in_bbox(self.player_position.x - self.treasure_map.player_icon.size[0] // 2, 
                          self.player_position.x + self.treasure_map.player_icon.size[0] // 2,
                          self.player_position.y - self.treasure_map.player_icon.size[1] // 2, 
                          self.player_position.y + self.treasure_map.player_icon.size[1] // 2):
            
            # set selected to True and store offset to center of image to prevent the icon from snapping to the cursor
            self.player_icon_is_selected = True
            self.mouse_offset_from_player_position = pos - self.player_position

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        """Set the player_icon_is_selected to false so the icon can be dragged and dropped only when selected

        Args:
            ev (QMouseEvent): PyQt6 mouse event
        """
        self.player_icon_is_selected = False


if __name__ == "__main__":
    app = QApplication([])
    
    window = MainWindow(Map(MAP_PATH, ICONS), OUT_DIR)
    window.show()

    app.exec()
