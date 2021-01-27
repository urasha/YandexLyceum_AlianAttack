from technical_func import load_image
import pygame

tile_images = {
    'grass': load_image('grass.png'),
    'trail': load_image('trail.png'),
    'base': load_image('turret_base.png'),
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
