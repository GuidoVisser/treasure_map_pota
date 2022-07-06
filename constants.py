import cv2

def get_map_size(path, scale):
    h, w, _ = cv2.imread(path).shape
    
    h *= scale
    w *= scale
    
    return int(w), int(h)

MAP_PATH = "images/dessarin_valley.jpg"
OUT_DIR = "images/output/"
MAP_SCALE = 0.2
MAP_SIZE = get_map_size(MAP_PATH, MAP_SCALE)
MAP_WIDTH = MAP_SIZE[0]
MAP_HEIGHT = MAP_SIZE[1]

