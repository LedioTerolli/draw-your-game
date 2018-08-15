from pygame_functions import *
from win32api import GetSystemMetrics
import os, os.path

screen_size_x = GetSystemMetrics(0)
screen_size_y = GetSystemMetrics(1)




def start_menu():
    start = make_sprite('images/start.png')
    levels = make_sprite('images/levels.png')
    exit = make_sprite('images/exit.png')

    start.move(screen_size_x / 2 - 500, screen_size_y / 2, True)
    levels.move(screen_size_x / 2 - 500, screen_size_y / 2 + 100, True)
    exit.move(screen_size_x / 2 - 500, screen_size_y / 2 + 200, True)

    show_sprite(start)
    show_sprite(levels)
    show_sprite(exit)

    while 1:
        pause(1, False)
        if spriteClicked(start):
            hideSprite(start)
            hideSprite(levels)
            hideSprite(exit)
            break
        elif spriteClicked(levels):
            hideSprite(start)
            hideSprite(levels)
            hideSprite(exit)
            level_menu()
            break
        elif spriteClicked(exit):
            pygame.quit()
            sys.exit()
            break


def pause_menu():
    start_menu_sprite = make_sprite('images/start_menu.png')
    resume = make_sprite('images/resume.png')
    exit = make_sprite('images/exit.png')

    resume.move(screen_size_x / 2, screen_size_y / 2, True)
    start_menu_sprite.move(screen_size_x / 2, screen_size_y / 2 + 100, True)
    exit.move(screen_size_x / 2, screen_size_y / 2 + 200, True)

    show_sprite(resume)
    show_sprite(start_menu_sprite)
    show_sprite(exit)

    while 1:
        pause(1, False)
        if spriteClicked(resume):
            hideSprite(resume)
            hideSprite(start_menu_sprite)
            hideSprite(exit)
            break
        elif spriteClicked(start_menu_sprite):
            hideSprite(resume)
            hideSprite(start_menu_sprite)
            hideSprite(exit)
            start_menu()
            break
        elif spriteClicked(exit):
            pygame.quit()
            sys.exit()
            break


def level_menu():
    start_menu_sprite = make_sprite('images/start_menu.png')
    show_sprite(start_menu_sprite)

    levels_dir = os.listdir('images/levels')
    level_list = []

    for i in range(len(levels_dir)):
        name = 'images/levels/' + levels_dir[i]
        filename = "%s" % name
        sprite_level = make_sprite(filename)

        if sprite_level.originalWidth > 100:
            scale = 100 / sprite_level.originalWidth
            sprite_level.scale = scale
            print(scale)

        sprite_level.changeImage(0)
        level_list.append(sprite_level)
        show_sprite(level_list[-1])



    while 1:
        pause(1, False)
        if spriteClicked(start_menu_sprite):
            hideSprite(start_menu_sprite)
            start_menu()
            break
