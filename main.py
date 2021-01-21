import pygame
import sys
from ground import Tile, tiles_group
from technical_func import load_image, load_level, generate_level
from menu import start_menu
from turret import turret_group, Turret, get_cell

FPS = 60
PRICE = 50

player_money = 100


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((750, 600))
    pygame.display.set_caption('Alian attack')

    start_menu(screen)
    screen.fill((0, 0, 0))

    lvl = load_level('level.txt')
    generate_level(lvl, Tile)

    tiles_group.draw(screen)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    coord = get_cell(len(lvl), len(lvl[0]), event.pos)
                    if lvl[coord[0]][coord[1]] != '?' and lvl[coord[0]][coord[1]] == '@':
                        Turret(coord[0], coord[1])
                        line = ' '.join(lvl[coord[0]]).split()
                        line[coord[1]] = '?'
                        lvl[coord[0]] = ''.join(line)

        turret_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
