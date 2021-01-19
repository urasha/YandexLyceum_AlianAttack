from image_load import load_image
import pygame

tile_images = {
    'bg': load_image('towerDefense_tile024.png'),
    'trail': load_image('towerDefense_tile050.png')
}
tile_width = tile_height = 50
tiles_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.tile_type = tile_type
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
