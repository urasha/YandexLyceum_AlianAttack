import pygame

enemy_group = pygame.sprite.Group()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(enemy_group)
