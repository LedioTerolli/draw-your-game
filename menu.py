from pygame_functions import *
from win32api import GetSystemMetrics

screen_size_x = GetSystemMetrics(0)
screen_size_y = GetSystemMetrics(1)


def start_menu():
    start = make_sprite('images/start.png')
    start.move(screen_size_x / 2, screen_size_y / 2, True)
    exit = make_sprite('images/exit.png')
    exit.move(screen_size_x / 2, screen_size_y / 2 + 100, True)
    show_sprite(start)
    show_sprite(exit)
    while 1:
        pause(1, False)
        if spriteClicked(start):
            hideAll()
            break
        elif spriteClicked(exit):
            pygame.quit()
            sys.exit()


def pause_menu():
    resume = make_sprite('images/resume.png')
    resume.move(screen_size_x / 2, screen_size_y / 2, True)
    exit = make_sprite('images/exit.png')
    exit.move(screen_size_x / 2, screen_size_y / 2 + 100, True)
    show_sprite(resume)
    show_sprite(exit)
    while 1:
        pause(1, False)
        if spriteClicked(resume):
            hideSprite(resume)
            hideSprite(exit)
            break
        elif spriteClicked(exit):
            pygame.quit()
            sys.exit()

def level_menu():
    

