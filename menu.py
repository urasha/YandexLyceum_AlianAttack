import pygame
from image_load import load_image


def start_screen(surface):
    TEXT_SPACING = 20
    RIGHT_INDENT = 235

    intro_text = ["Начать",
                  "Правила игры",
                  "Выйти"]

    font_text = pygame.font.Font(None, 75)
    font_name = pygame.font.Font(None, 45)

    bg = pygame.transform.scale(load_image('bg.jpg'), (750, 600))

    name = font_text.render("Alian attack", True, (200, 50, 0))

    arrow = load_image('arrow.png')
    arrow = pygame.transform.scale(arrow, (70, 35))
    y_arr = 205
    counter_arr = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if counter_arr != 2:
                        counter_arr += 1
                if event.key == pygame.K_UP:
                    if counter_arr != 0:
                        counter_arr -= 1

        surface.blit(bg, (0, 0))
        text_coord = 190
        for line in intro_text:
            string_rendered = font_name.render(line, True, (200, 200, 200))
            intro_rect = string_rendered.get_rect()
            text_coord += TEXT_SPACING
            intro_rect.top = text_coord
            intro_rect.x = RIGHT_INDENT
            text_coord += intro_rect.height
            surface.blit(string_rendered, intro_rect)
        surface.blit(name, (RIGHT_INDENT, 120))
        surface.blit(arrow, (RIGHT_INDENT - 75, y_arr + 50 * counter_arr))

        pygame.display.flip()
