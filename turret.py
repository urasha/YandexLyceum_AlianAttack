import pygame
from technical_func import load_image
from ground import TILE_WIDTH
from pygame.math import Vector2
from character import Enemy

WIDTH = 50
HEIGHT = 60
turret_group = pygame.sprite.Group()
turret_images = {
    'rocket': load_image('rocket_turret.png'),
    'bullet': load_image('bullet_turret.png'),
    'fire': load_image('fire_turret.png')
}


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
    def __init__(self, pos_x, pos_y, turret_type):
        super().__init__(turret_group)
        self.image = turret_images[turret_type]
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.original_image = self.image
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_y, TILE_WIDTH * pos_x - 5)

    def rotate(self):
        x, y, w, h = self.rect
        direction = pygame.mouse.get_pos() - Vector2(x + w // 2, y + h // 2)
        radius, angle = direction.as_polar()
        self.image = pygame.transform.rotate(self.original_image, -angle - 90)
        self.rect = self.image.get_rect(center=self.rect.center)


class BulletTurret(Turret):
    def __init__(self, pos_x, pos_y, turret_type):
        super().__init__(pos_x, pos_y, turret_type)
        self.radius = 50
        self.price = 70
        self.speed = 500


class RocketTurret(Turret):
    def __init__(self, pos_x, pos_y, turret_type):
        super().__init__(pos_x, pos_y, turret_type)
        self.radius = 70
        self.price = 100
        self.speed = 1000


class FireTurret(Turret):
    def __init__(self, pos_x, pos_y, turret_type):
        super().__init__(pos_x, pos_y, turret_type)
        self.radius = 50
        self.price = 70
        self.speed = 200
