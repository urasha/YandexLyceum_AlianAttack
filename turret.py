import pygame
from technical_func import load_image
from ground import TILE_WIDTH

WIDTH = 50
HEIGHT = 50
turret_group = pygame.sprite.Group()


def get_cell(height, width, mouse_pos):
    for i in range(height):
        for j in range(width):
            x1 = TILE_WIDTH * j
            x2 = x1 + TILE_WIDTH
            y1 = TILE_WIDTH * i
            y2 = y1 + TILE_WIDTH
            if mouse_pos[0] in range(x1, x2 + 1) and mouse_pos[1] in range(y1, y2 + 1):
                return i, j


class Turret(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(turret_group)
        self.image = load_image('turret.png')
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.rect = self.image.get_rect().move(WIDTH * pos_y, HEIGHT * pos_x - 15)
