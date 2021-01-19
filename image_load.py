import os
import sys
from pygame import image


def load_image(name):
    fullname = os.path.join('sprites', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    img = image.load(fullname)
    return img
