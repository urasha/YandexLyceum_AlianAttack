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
        self.ORIG_HP = 28 if enemy_type == 'sprinter' else 40
        self.hp = self.ORIG_HP
        self.award = 10 if enemy_type == 'sprinter' else 6
        self.image = enemy_images[enemy_type]
        self.image = pygame.transform.scale(self.image, (TILE_WIDTH, TILE_WIDTH))
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = random.randrange(330, 355)
        self.dx = 3 if enemy_type == 'sprinter' else 2
        self.dy = 0
        self.control_positions = {
            (self.rect.x + 252, self.rect.y): (0, self.dx, -90),
            (self.rect.x + 252, self.rect.y + 66): (self.dx, 0, 0),
            (self.rect.x + 504, self.rect.y + 66): (0, self.dx, -90),
            (self.rect.x + 504, self.rect.y + 108): (self.dx, 0, 0),
            (self.rect.x + 762, self.rect.y + 108): (0, -self.dx, 90),
            (self.rect.x + 762, self.rect.y): (-self.dx, 0, 180),
            (self.rect.x + 714, self.rect.y): (0, -self.dx, 90),
            (self.rect.x + 714, self.rect.y - 66): (-self.dx, 0, 180),
            (self.rect.x + 600, self.rect.y - 66): (0, -self.dx, 90),
            (self.rect.x + 600, self.rect.y - 114): (-self.dx, 0, 180),
            (self.rect.x + 306, self.rect.y - 114): (0, -self.dx, 90),
            (self.rect.x + 306, self.rect.y - 240): (self.dx, 0, 0),
            (self.rect.x + 1001, self.rect.y - 240): (self.dx, 0, 0)
        }
        self.counter_pos = 0

    def move_enemy(self):
        """
        Сдвиг врага
        """
        self.rect.x += self.dx
        self.rect.y += self.dy

    def change_position(self):
        """
        Проверка координат врагов
        """
        key = list(self.control_positions.keys())[self.counter_pos]
        # зашёл ли за границы экрана?
        if self.rect.x >= 1000:
            enemy_group.remove(self)
            return 1
        # достиг ли поворота?
        if tuple(self.rect[0:2]) == key:
            self.dx = self.control_positions[key][0]
            self.dy = self.control_positions[key][1]
            self.image = pygame.transform.rotate(self.orig_image, self.control_positions[key][2])
            self.counter_pos += 1

        return 0

    def take_damage(self, damage):
        """Получение врагом урона"""
        self.hp -= damage

    def check_death(self):
        """Проверка на смерть (нулевое здоровье)"""
        if self.hp <= 0:
            return True

    def draw_hp_bar(self, screen):
        """Отрисовка уровня здоровья врагов"""
        x, y, w, h = self.rect
        pygame.draw.rect(screen, 'red', (x, y + 5, 100 * self.hp / self.ORIG_HP // 2, h * 0.07))

