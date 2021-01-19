import pygame
import sys
from ground import Tile, tiles_group
from image_load import load_image
from menu import start_screen

FPS = 60


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((750, 600))
    pygame.display.set_caption('Alian attack')

    start_screen(screen)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        tiles_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()

