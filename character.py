import pygame
from technical_func import load_image
from ground import TILE_WIDTH
import random

pygame.init()

enemy_group = pygame.sprite.Group()
enemy_images = {
    'usual': load_image('usual_enemy.png'),
    'sprinter': load_image('sprinter_enemy.png')
}


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type):
        super().__init__(enemy_group)
        self.image = enemy_images[enemy_type]
        self.image = pygame.transform.scale(self.image, (TILE_WIDTH, TILE_WIDTH))
        self.orig_image = self.image
        self.dx = 2 if enemy_type == 'usual' else 3
        self.dy = 0
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = random.randrange(330, 348)

        self.control_positions = {
            (252, self.rect.y): (0, self.dx, -90),
            (252, self.rect.y + 66): (self.dx, 0, 0),
            (504, self.rect.y + 66): (0, self.dx, -90),
            (504, self.rect.y + 108): (self.dx, 0, 0),
            (762, self.rect.y + 108): (0, -self.dx, 90),
            (762, self.rect.y): (-self.dx, 0, 180),
            (714, self.rect.y): (0, -self.dx, 90),
            (714, self.rect.y - 66): (-self.dx, 0, 180),
            (600, self.rect.y - 66): (0, -self.dx, 90),
            (600, self.rect.y - 114): (-self.dx, 0, 180),
            (306, self.rect.y - 114): (0, -self.dx, 90),
            (306, self.rect.y - 240): (self.dx, 0, 0),
            (1001, self.rect.y - 240): (self.dx, 0, 0)
        }  # костыль - ПОТОМ МБ ИСПРАВИТЬ
        self.counter_pos = 0

    def move_enemy(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def check_position(self):
        key = list(self.control_positions.keys())[self.counter_pos]
        # зашёл ли за границы экрана?
        if self.rect.x >= 1000:
            enemy_group.remove(self)
        # достиг ли поворота?
        if tuple(self.rect[0:2]) == key:
            self.dx = self.control_positions[key][0]
            self.dy = self.control_positions[key][1]
            self.image = pygame.transform.rotate(self.orig_image, self.control_positions[key][2])
            self.counter_pos += 1
