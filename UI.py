import pygame
from pygame import gfxdraw
from process import get_data
from pygame_functions import *
import sys

pygame.init()
edge, new_img, list_obj = get_data("p12.jpg")
scX = new_img.shape[0]
scY = new_img.shape[1]
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.update()
purple = (74, 20, 140)
white = (255, 255, 255)
red = (255, 23, 68)
blue = (0, 0, 255)
clock = pygame.time.Clock()
mouse_pos = []
list_custom = []
list_black = []
list_other = []


'''
for i in range(len(list_obj)):
    if len(list_obj[i].coor) == 3:
        list_black.append(makeSprite("blackhole.png"))
        moveSprite(list_black[-1], list_obj[i].center[0], list_obj[i].center[1])
        showSprite(list_black[-1])

    else:
        list_other.append(makeSprite("blackhole.png"))
        moveSprite(list_other[-1], list_obj[i].center[0], list_obj[i].center[1])
        showSprite(list_other[-1])
'''


while 1:
    speed = 10
    list_poly = []
    clock.tick(120)
    screen.fill(purple)

    # draw photo polygons
    for i in range(len(list_obj)):
        list_poly.append(
            Poly(screen, list_obj[i].tup_coor, list_obj[i].coor, list_obj[i].area, list_obj[i].peri, list_obj[i].center,
                 red))

    # draw mouse points
    for i in mouse_pos:
        pygame.gfxdraw.aacircle(screen, i[0], i[1], 2, white)
        pygame.gfxdraw.filled_circle(screen, i[0], i[1], 2, white)

    # draw mouse polygons
    for i in range(len(list_custom)):
        if len(list_custom[i]) == 0:
            continue
        elif len(list_custom[i]) == 1:
            pygame.gfxdraw.aacircle(screen, (list_custom[i])[0][0], (list_custom[i])[0][1], 10, red)
            pygame.gfxdraw.filled_circle(screen, (list_custom[i])[0][0], (list_custom[i])[0][1], 10, red)
        elif len(list_custom[i]) == 2:
            pygame.gfxdraw.line(screen, (list_custom[i])[0][0], (list_custom[i])[0][1], (list_custom[i])[1][0],
                                (list_custom[i])[1][1], red)
        else:
            pygame.gfxdraw.aapolygon(screen, list_custom[i], red)
            pygame.gfxdraw.filled_polygon(screen, list_custom[i], red)

    # controls
    if key_press("left"):
        move(list_obj, 0, 1, speed)
    elif key_press("right"):
        move(list_obj, 0, 2, speed)
    elif key_press("up"):
        move(list_obj, 0, 3, speed)
    elif key_press("down"):
        move(list_obj, 0, 4, speed)
    elif key_press("space"):
        list_custom.append(mouse_pos)
        mouse_pos = []
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
    if mouse_press():
        a = pygame.mouse.get_pos()
        if len(mouse_pos) == 0:
            mouse_pos.append(a)
        if mouse_pos[-1] != a:
            mouse_pos.append(a)

    pygame.display.update()
