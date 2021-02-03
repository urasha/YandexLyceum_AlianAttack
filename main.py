import pygame
import sys
from ground import Tile, tiles_group
from technical_func import load_image, load_level, generate_level
from menu import start_menu
from turret import turret_group, Turret, BulletTurret, LaserTurret, RocketTurret, \
    get_cell, check_shooting, shooting_events, turret_images
import math
from character import enemy_group, Enemy
import random
import secrets


def terminate():
    pygame.quit()
    sys.exit()


def check_game_state(param, text):
    if param <= 0:
        pygame.mixer.music.fadeout(500)
        surf = pygame.Surface((1000, 700))
        surf.fill('black')
        surf.set_alpha(200)
        screen.blit(surf, (0, 0))
        screen.blit(font_1.render(text, True, (150, 150, 255)), (290, 250))
        pygame.display.flip()
        pygame.time.wait(2000)
        terminate()


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    font_1 = pygame.font.Font(None, 75)
    font_2 = pygame.font.Font(None, 40)
    font_3 = pygame.font.Font(None, 35)

    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption('VLDTower')

    pygame.mixer.music.load('sounds/music.mp3')
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)

    start_menu(screen)
    screen.fill((0, 0, 0))

    # генерация уровня
    lvl = load_level('level2.txt')
    generate_level(lvl, Tile)

    FPS = 60
    SPAWN_GROUP = pygame.USEREVENT + 1
    COUNT_TIME = pygame.USEREVENT + 2
    SPAWN_ENEMY = pygame.USEREVENT + 3

    player_money = 170
    money_image = load_image('money.jpg')
    money_image.set_colorkey((255, 255, 255))
    money_image = pygame.transform.scale(money_image, (100, 100))

    base_hp = 5
    base_image = load_image('heart.png')
    base_image = pygame.transform.scale(base_image, (80, 60))

    light = load_image('light.png')
    light = pygame.transform.scale(light, (160, 150))
    light.set_alpha(200)
    is_fade_out = True

    bullet_turret = pygame.transform.scale(turret_images['bullet'], (60, 75))
    laser_turret = pygame.transform.scale(turret_images['laser'], (60, 75))
    rocket_turret = pygame.transform.scale(turret_images['rocket'], (60, 75))

    turret_types = [LaserTurret, BulletTurret, RocketTurret]
    turret_names = ['laser', 'bullet', 'rocket']
    active_type = 1

    silver_bullet = load_image('silver_bullet.png')

    time_before_start = 20
    time_after_start = 145
    pygame.time.set_timer(COUNT_TIME, 1000)

    is_spawn = False
    is_see_radius = False
    counter_spawn = 0
    clock = pygame.time.Clock()
    while True:
        # отрисовка спрайтов
        tiles_group.draw(screen)
        enemy_group.draw(screen)

        if time_before_start > 0:
            screen.blit(font_2.render(f'До начала: {time_before_start} сек', True, 'black'), (20, 20))
        elif time_before_start == 0:
            pygame.time.set_timer(SPAWN_GROUP, 6500)

        elif 145 >= time_after_start > -1:
            screen.blit(font_2.render(f'Осталось: {time_after_start} сек', True, 'black'), (20, 20))

        # здоровье базы
        screen.blit(base_image, (60, 600))
        screen.blit(font_1.render(str(base_hp), True,  (30, 30, 30)), (135, 610))

        # кол-во денег
        screen.blit(money_image, (760, 580))
        screen.blit(font_1.render(str(player_money), True, (30, 30, 30)), (855, 610))

        # цены турелей
        screen.blit(font_3.render('$120', True, 'black'), (315, 630))
        screen.blit(font_3.render('$70', True, 'black'), (490, 630))
        screen.blit(font_3.render('$120', True, 'black'), (655, 630))

        screen.blit(laser_turret, (250, 600))
        screen.blit(bullet_turret, (420, 600))
        screen.blit(rocket_turret, (590, 600))
        pygame.draw.rect(screen, 'black', (225, 595, 510, 85), 2)
        pygame.draw.rect(screen, 'red', (225 + 170 * active_type, 595, 171, 85), 4)
        pygame.draw.line(screen, 'black', (395, 595), (395, 680), 2)
        pygame.draw.line(screen, 'black', (565, 595), (565, 680), 2)

        # красный свет
        if time_before_start > 0:
            if is_fade_out:
                light.set_alpha(light.get_alpha() - 2)
            else:
                light.set_alpha(light.get_alpha() + 2)
            if light.get_alpha() < 100:
                is_fade_out = False
            elif light.get_alpha() > 200:
                is_fade_out = True

            screen.blit(light, (-80, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                coord = get_cell(len(lvl), len(lvl[0]), event.pos)
                # устновка турели
                if event.button == 1:
                    # есть ли место для турели?
                    if lvl[coord[0]][coord[1]] == '@':
                        turret = turret_types[active_type](coord[0], coord[1], turret_names[active_type])
                        if player_money - turret.price >= 0:  # достаточно денег?
                            player_money -= turret.price
                            line = ' '.join(lvl[coord[0]]).split()
                            line[coord[1]] = '?'
                            lvl[coord[0]] = ''.join(line)
                            turret.play_base_sound()
                        else:
                            turret_group.remove(turret)  # нет денег - нет турели
                # удаление турели
                if event.button == 3:
                    if lvl[coord[0]][coord[1]] == '?':
                        player_money += 40
                        line = ' '.join(lvl[coord[0]]).split()
                        line[coord[1]] = '@'
                        lvl[coord[0]] = ''.join(line)
                        for i in turret_group:
                            if i.lvl_coord == (coord[0], coord[1]):
                                turret_group.remove(i)

            # смена турелей
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    active_type = 0
                elif event.key == pygame.K_2:
                    active_type = 1
                elif event.key == pygame.K_3:
                    active_type = 2
                elif event.key == pygame.K_ESCAPE:
                    start_menu(screen)
                elif event.key == pygame.K_SPACE:
                    is_see_radius = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    is_see_radius = False

            if event.type == COUNT_TIME:
                time_before_start -= 1
                time_after_start -= 1

            if event.type == SPAWN_GROUP:
                num = 4
                if time_after_start < 80:
                    num = 6
                elif time_after_start < 50:
                    num = 8
                elif time_after_start < 20:
                    num = 10
                counter_spawn = random.randint(3, num)
                pygame.time.set_timer(SPAWN_ENEMY, 2500 // counter_spawn)

            if event.type == SPAWN_ENEMY:
                if counter_spawn > 0:
                    Enemy('sprinter' if secrets.randbelow(100) < 25 else 'usual')
                    counter_spawn -= 1

            # события стрельбы
            for j in shooting_events:
                if j == event.type:
                    check_shooting(shooting_events[j], screen)

        # проверка на проигрыш
        check_game_state(base_hp, 'Поражение')

        # проверка на победу
        check_game_state(time_after_start, 'Вы победили!')

        # отрисовка радиусов
        if is_see_radius:
            for i in turret_group:
                pygame.draw.circle(screen, 'red', (i.rect.x + i.rect.width // 2,
                                                   i.rect.y + i.rect.height // 2), i.radius, width=2)

        # поворот турелей к врагам
        for i in turret_group:
            try:
                x, y, enemy = i.check_area()
            except Exception:
                continue
            i.rotate((x, y))

            # проверка на смерть противника
            if enemy.check_death():
                enemy_group.remove(enemy)
                player_money += enemy.award

        # движение врагов
        for i in enemy_group:
            base_hp -= i.change_position()
            i.move_enemy()
            i.draw_hp_bar(screen)

        # отрисовка турели
        turret_group.draw(screen)

        clock.tick(FPS)
        pygame.display.flip()
