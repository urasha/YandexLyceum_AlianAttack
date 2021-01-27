import pygame
import sys
from ground import Tile, tiles_group
from technical_func import load_image, load_level, generate_level
from menu import start_menu
from turret import turret_group, Turret, BulletTurret, LaserTurret, RocketTurret, \
    get_cell, check_shooting, shooting_events
import math
from character import enemy_group, Enemy
import numpy


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    font = pygame.font.Font(None, 75)

    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption('VLDtower')

    start_menu(screen)
    screen.fill((0, 0, 0))

    # генерация уровня
    lvl = load_level('level2.txt')
    generate_level(lvl, Tile)

    FPS = 60

    player_money = 320
    base_hp = 5

    turret_types = [LaserTurret, BulletTurret, RocketTurret]
    turret_names = ['laser', 'bullet', 'rocket']
    active_type = 1

    enemy_names = ['sprinter', 'usual']

    clock = pygame.time.Clock()
    while True:
        # отрисовка спрайтов
        tiles_group.draw(screen)
        turret_group.draw(screen)
        enemy_group.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                coord = get_cell(len(lvl), len(lvl[0]), event.pos)
                if event.button == 1:
                    # есть ли место для турели?
                    if lvl[coord[0]][coord[1]] == '@':
                        turret = turret_types[active_type](coord[0], coord[1], turret_names[active_type])
                        if player_money - turret.price >= 0:  # достаточно денег?
                            player_money -= turret.price
                            line = ' '.join(lvl[coord[0]]).split()
                            line[coord[1]] = '?'
                            lvl[coord[0]] = ''.join(line)
                        else:   
                            turret_group.remove(turret)  # нет денег - нет турели

            # смена турелей
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    active_type = 0
                elif event.key == pygame.K_2:
                    active_type = 1
                elif event.key == pygame.K_3:
                    active_type = 2
                elif event.key == pygame.K_SPACE:
                    Enemy(numpy.random.choice(enemy_names, 1, [0.3, 0.7])[0])
                elif event.key == pygame.K_ESCAPE:
                    start_menu(screen)

            # события стрельбы
            for j in shooting_events:
                if j == event.type:
                    check_shooting(shooting_events[j], screen)

        if base_hp <= 0:
            surf = pygame.Surface((1000, 600))
            surf.fill('black')
            surf.set_alpha(200)
            screen.blit(surf, (0, 0))
            screen.blit(font.render('Игра окончена', True, (150, 150, 255)), (290, 250))

        # поворот турелей к врагам
        for i in turret_group:
            try:
                x, y, enemy = i.check_area(screen)
            except Exception:
                continue
            i.rotate((x, y))

            # проверка на смерть противника
            if enemy.check_death():
                enemy_group.remove(enemy)
                player_money += enemy.award

        # движение врагов; отрисовка hp
        for i in enemy_group:
            base_hp -= i.change_position()
            i.move_enemy()
            i.draw_hp_bar(screen)

        clock.tick(FPS)
        pygame.display.flip()
