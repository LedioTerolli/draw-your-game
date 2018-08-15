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
            return 0
            break
        elif spriteClicked(levels):
            hideSprite(start)
            hideSprite(levels)
            hideSprite(exit)
            return level_menu()
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
            return start_menu()
        elif spriteClicked(exit):
            pygame.quit()
            sys.exit()
            break


def level_menu():
    start_menu_sprite = make_sprite('images/start_menu.png')
    start_menu_sprite.move(screen_size_x / 2, screen_size_y / 1.5, True)
    show_sprite(start_menu_sprite)

    levels_dir = os.listdir('images/levels')
    level_list = []

    start_point_x = (screen_size_x - (len(levels_dir) * 200 + 100)) / 2 + 100

    poss = 0
    for i in range(len(levels_dir)):
        name = 'images/thumbnail/' + levels_dir[i]
        filename = "%s" % name
        sprite_level = make_sprite(filename)
        sprite_level.move(start_point_x + poss, screen_size_y / 2, True)

        level_list.append(sprite_level)
        show_sprite(level_list[-1])
        poss += 300

    while 1:
        pause(1, False)

        for x in range(len(level_list)):
            if spriteClicked(level_list[x]):
                for i in level_list:
                    hideSprite(i)
                hideSprite(start_menu_sprite)
                return x

        if spriteClicked(start_menu_sprite):
            for i in level_list:
                hideSprite(i)
            hideSprite(start_menu_sprite)
            start_menu()
            break
