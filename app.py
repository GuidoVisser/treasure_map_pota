from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import cv2

from constants import MAP_WIDTH, MAP_HEIGHT
from src.position import Position
from src.generate_map import Map
from src.icons import Icon, ICONS

LAST_POSITION = Position(0,0)
PLAYER_ICON = Icon("player", Position(0, 0), lambda x: 0, lambda x: 0, img_path="images/icons/aluminium.png")

def move(event):
    global bg_img # because tkinter
    cv2_img = map.render(Position(event.x, event.y, mode="absolute"))
    pil_img = Image.fromarray(cv2_img)
    bg_img = ImageTk.PhotoImage(image=pil_img)
    canvas.create_image(0, 0, image=bg_img, anchor=NW)

    global mouse_icon # because tkinter
    cv2_icon = np.concatenate((PLAYER_ICON.image, PLAYER_ICON.alpha[..., 0:1] * 255), axis=2)
    pil_icon = Image.fromarray(cv2_icon)
    mouse_icon = ImageTk.PhotoImage(image=pil_icon)
    canvas.create_image(event.x, event.y, image=mouse_icon)

    global LAST_POSITION
    LAST_POSITION = Position(event.x, event.y, mode="absolute")

class IconButton(object):
    def __init__(self, button_bar, icon, index) -> None:
        super().__init__()

        self.button_bar = button_bar
        self.icon = icon
        self.index = index
        self.active = False
        self.render_button()

    def render_button(self):
        global icon_image_list
        if self.active:
            img = Image.fromarray(self.icon.image)
        else:
            img = Image.fromarray(self.icon.image // 2)

        icon_image_list[self.index] = ImageTk.PhotoImage(img)
        self.button = Button(self.button_bar, image=icon_image_list[self.index], command=self.button_press)
        self.button.grid(row=self.index, column=0)
    
        self.text = Text(self.button_bar, height=2, width=8)
        self.text.insert(INSERT, self.icon.name)
        self.text.grid(row=self.index, column=1)

    def button_press(self):
        self.icon.show_true_position = not self.icon.show_true_position
        self.active = not self.active
        self.render_button()
        move(LAST_POSITION)


class ExportButton(object):
    def __init__(self, button_bar) -> None:
        super().__init__()

        self.button_bar = button_bar
        self.render_button()
        
    def render_button(self):
        global export_img
        img = Image.open("images/export.png")
        img = img.resize((40, 40))
        export_img = ImageTk.PhotoImage(img)
        self.button = Button(self.button_bar, image=export_img, command=self.export)
        self.button.grid(row=len(ICONS) + 1, column=0)

        self.text = Text(self.button_bar, height=2, width=8)
        self.text.insert(INSERT, "Export")
        self.text.grid(row=len(ICONS) + 1, column=1)

    def export(self):
        out_img = map.render(LAST_POSITION)
        out_img = cv2.cvtColor(out_img, cv2.COLOR_RGB2BGR)
        cv2.imwrite("images/out.png", out_img)

root = Tk()
root.title("Treasure Map")

canvas = Canvas(root, width=MAP_WIDTH, height=MAP_HEIGHT, bg="white")
icon_bar = Frame(root, borderwidth=2, relief="raised")

canvas.pack(side=LEFT, fill='both', expand=True)
icon_bar.pack(side=RIGHT, fill='both', expand=True)

icon_image_list = list(np.arange(len(ICONS)))
icons_buttons = [IconButton(icon_bar, icon, index=i) for i, icon in enumerate(ICONS)]

export_button = ExportButton(icon_bar)

icon_bar.grid_rowconfigure(100, weight=1)
icon_bar.grid_columnconfigure(2, weight=1)

map_path = "images/dessarin_valley.jpg"

map = Map(map_path, ICONS)

move(Position(0.5, 0.5))
canvas.bind("<B1-Motion>", move)
root.mainloop()