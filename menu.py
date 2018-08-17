from fun import *
from win32api import GetSystemMetrics
import os, os.path

screen_size_x = GetSystemMetrics(0)
screen_size_y = GetSystemMetrics(1)
pause_click = 200


def start_menu(new_counter):
    i = new_counter

    mars_bg = make_sprite('images/mars_1000.png')
    start_sprite = make_sprite('images/start.jpg')
    levels_sprite = make_sprite('images/levels.jpg')
    exit_sprite = make_sprite('images/exit.jpg')

    mars_bg.move(screen_size_x / 2, screen_size_y / 2, True)
    start_sprite.move(screen_size_x / 2, screen_size_y / 2 - 100, True)
    levels_sprite.move(screen_size_x / 2, screen_size_y / 2, True)
    exit_sprite.move(screen_size_x / 2, screen_size_y / 2 + 100, True)

    show_sprite(mars_bg)
    show_sprite(start_sprite)
    show_sprite(levels_sprite)
    show_sprite(exit_sprite)

    while 1:
        pause(1, False)
        if sprite_clicked(start_sprite):
            hide_sprite(start_sprite)
            hide_sprite(levels_sprite)
            hide_sprite(exit_sprite)
            hide_sprite(mars_bg)
            pause(pause_click, False)
            return i
        elif sprite_clicked(levels_sprite):
            hide_sprite(start_sprite)
            hide_sprite(levels_sprite)
            hide_sprite(exit_sprite)
            hide_sprite(mars_bg)
            pause(pause_click, False)
            return level_menu(i)
        elif sprite_clicked(exit_sprite):
            pygame.quit()
            sys.exit()
            pause(pause_click, False)
            return i


def level_menu(new):
    i = new
    back_sprite = make_sprite('images/back.jpg')
    back_sprite.move(screen_size_x / 2, screen_size_y / 1.5, True)
    show_sprite(back_sprite)

    levels_dir = os.listdir('images/levels')
    level_list = []

    start_point_x = (screen_size_x - (len(levels_dir) * 200 + 100 * (len(levels_dir) - 1))) / 2 + 100

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
            if sprite_clicked(level_list[x]):
                for y in level_list:
                    hide_sprite(y)
                hide_sprite(back_sprite)
                i = x
                pause(pause_click, False)
                return start_menu(i)

            elif sprite_clicked(back_sprite):
                for z in level_list:
                    hide_sprite(z)
                hide_sprite(back_sprite)
                pause(pause_click, False)
                return start_menu(i)
