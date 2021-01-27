import pygame
from technical_func import load_image
from ground import TILE_WIDTH
from pygame.math import Vector2
from math import sqrt
from character import Enemy, enemy_group

WIDTH = 50
HEIGHT = 60
turret_group = pygame.sprite.Group()
turret_images = {
    'rocket': load_image('rocket_turret.png'),
    'bullet': load_image('bullet_turret.png'),
    'laser': load_image('laser.png')
}
shooting_events = {}


def get_cell(height, width, mouse_pos):
    """
    Определение нажатой клетки
    """
    for i in range(height):
        for j in range(width):
            x1 = TILE_WIDTH * j
            x2 = x1 + TILE_WIDTH
            y1 = TILE_WIDTH * i
            y2 = y1 + TILE_WIDTH
            if mouse_pos[0] in range(x1, x2 + 1) and mouse_pos[1] in range(y1, y2 + 1):
                return i, j


def check_shooting(t_type, screen):
    """Проверка на необзодимость выстрела"""
    for t in [i for i in turret_group if i.t_type == t_type]:
        try:
            enemy = t.check_area(screen)[2]
        except Exception:
            continue
        enemy.take_damage(t.damage)


class Turret(pygame.sprite.Sprite):
    counter = 0

    def __init__(self, pos_x, pos_y, turret_type):
        super().__init__(turret_group)
        self.t_type = turret_type
        self.image = turret_images[turret_type]
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.original_image = self.image
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_y, TILE_WIDTH * pos_x - 5)

        self.radius = None
        self.counter += 1

        shooting_events[pygame.USEREVENT + self.counter] = self.t_type

    def rotate(self, xy):
        """
        Поворот турели в сторону врага
        """
        x, y, w, h = self.rect
        try:
            direction = xy - Vector2(x + w // 2, y + h // 2)
        except Exception:
            return
        angle = direction.as_polar()[1]  # угол поворота турели
        self.image = pygame.transform.rotate(self.original_image, -angle - 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def check_area(self, screen):
        """
        Проверка на нахождение врагов в радиусе действия
        """
        x, y, w, h = self.rect
        turret_center = [x + w // 2, y + h // 2]
        sprites = enemy_group.sprites()

        pygame.draw.circle(screen, 'red', turret_center, self.radius, 2)

        for i in sprites:
            if self._distance(turret_center[0], turret_center[1], i.rect.x, i.rect.y) <= self.radius:
                return i.rect.x, i.rect.y, i

    @staticmethod
    def _distance(x1, y1, x2, y2):
        """Определение расстояния от врага до турели"""
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


class BulletTurret(Turret):
    def __init__(self, pos_x, pos_y, turret_type):
        super().__init__(pos_x, pos_y, turret_type)
        self.radius = 115
        self.price = 70
        self.damage = 2
        pygame.time.set_timer(pygame.USEREVENT + self.counter, 100)


class RocketTurret(Turret):
    def __init__(self, pos_x, pos_y, turret_type):
        super().__init__(pos_x, pos_y, turret_type)
        self.radius = 150
        self.price = 100
        self.damage = 8
        pygame.time.set_timer(pygame.USEREVENT + self.counter, 450)


class LaserTurret(Turret):
    def __init__(self, pos_x, pos_y, turret_type):
        super().__init__(pos_x, pos_y, turret_type)
        self.radius = 160
        self.price = 70
        self.damage = 1
        pygame.time.set_timer(pygame.USEREVENT + self.counter, 50)
