from tkinter import *
from PIL import Image, ImageTk
import numpy as np

from constants import MAP_WIDTH, MAP_HEIGHT
from src.position import Position
from src.generate_map import Map
from src.icons import Icon, ICONS

PLAYER_ICON = Icon(Position(0, 0), lambda x: 0, lambda x: 0, img_path="images/icons/aluminium.png")

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

root = Tk()
root.title("Treasure Map")
root.geometry("788x1000")

canvas = Canvas(root, width=MAP_WIDTH, height=MAP_HEIGHT, bg="white")
canvas.pack(pady=20)

map_path = "images/dessarin_valley.jpg"

map = Map(map_path, ICONS)

move(Position(0.5, 0.5))
canvas.bind("<B1-Motion>", move)
root.mainloop()