from technical_func import load_image
import pygame

tile_images = {
    'grass': load_image('towerDefense_tile024.png'),
    'trail': load_image('towerDefense_tile158.png'),
    'base': load_image('towerDefense_tile044.png'),
}
TILE_WIDTH = TILE_HEIGHT = 50
tiles_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.image = pygame.transform.scale(self.image, (TILE_WIDTH, TILE_HEIGHT))
        self.tile_type = tile_type
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)
