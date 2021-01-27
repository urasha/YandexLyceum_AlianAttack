import os
import sys
from pygame import image, transform


def load_image(name):
    """
    Загрузка изображений
    """
    fullname = os.path.join('sprites', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    img = image.load(fullname)
    return img


def load_level(filename):
    """
    Загрузка уровня
    """
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


def generate_level(level, cls):
    """
    Создание уровня из файла
    """
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                cls('grass', x, y)
            elif level[y][x] == '#':
                cls('trail', x, y)
            elif level[y][x] == '@':
                cls('base', x, y)
