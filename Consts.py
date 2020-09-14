import os

WINDOW_NAME = "AnnotationGUI"


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700
WINDOW_X = 400
WINDOW_Y = 0
WINDOW_SIZE = str(WINDOW_WIDTH) + 'x' + str(WINDOW_HEIGHT) + '+' + str(WINDOW_X) + '+' + str(WINDOW_Y)


ROW = COL = 512
BTN_REGION = {"relx": 0.75, "rely": 0.1, "relwidth": 0.2, "text": "領域拡張法"}
BTN_BRUSH = {"relx": 0.75, "rely": 0.2, "relwidth": 0.2, "text": "ブラシ"}
BTN_CLOSING = {"relx": 0.75, "rely": 0.3, "relwidth": 0.2, "text": "クロージング"}
BTN_ERASER = {"relx": 0.75, "rely": 0.4, "relwidth": 0.2, "text": "消しゴム"}
BTN_REGION_P = {"relx": 0.75, "rely": 0.5, "relwidth": 0.2, "text": "領域拡張法2"}

BTN_R = {"relx": 0.80, "rely": 0.7, "relwidth": 0.05, "text": "R"}
BTN_G = {"relx": 0.90, "rely": 0.7, "relwidth": 0.05, "text": "G"}
BTN_Y = {"relx": 0.80, "rely": 0.75, "relwidth": 0.05, "text": "Y"}
BTN_B = {"relx": 0.90, "rely": 0.75, "relwidth": 0.05, "text": "B"}
SLIDER_FOR_INDEX = {"title": "index", "min": 0, "default": 0,
                    "relx": 0.75, "rely": 0.45, "relwidth": 0.2}

SLIDER_FOR_BRUSH = {"title": "太さ", "min": 1, "max": 40, "default": 3,
                    "relx": 0.75, "rely": 0.55, "relwidth": 0.2}
SLIDER_FOR_REGION = {"title": "閾値", "min": 0, "max": 50, "default": 25,
                     "relx": 0.75, "rely": 0.55, "relwidth": 0.2}

CANVAS_FOR_IMAGE = {"relx": 0.05, "rely": 0.05}

MOUSE_MODE = {"press": 0, "drag": 1, "release":2}

FILE_TYPE = {"dicom": 0, "raw": 1}

SAVE_MESSAGE = "Save as "

RAW_FILE = [("raw file", ".raw")]

COLOR_PLATTE_FOR_RAW = {"red": (1, 1, 1), "green": (2, 2, 2), "blue": (3, 3, 3), "yellow":(4, 4, 4)}
COLOR = {"red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255),
         "yellow": (128, 128, 0), "black": (0, 0, 0)}

# DEFAULT_DIR = r"C:\Users\Ritter\Documents\eso_limphCTData2"
# パスを変更してください
DEFAULT_DIR = r"I:\Data\OPE(25ー59）"
