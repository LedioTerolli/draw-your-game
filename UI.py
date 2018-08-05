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


def key_press(key_check=""):
    pygame.event.clear()
    keys = pygame.key.get_pressed()
    if sum(keys) > 0:
        if key_check == "" or keys[keydict[key_check.lower()]]:
            return True
    return False


def mouse_press():
    pygame.event.clear()
    mouse_st = pygame.mouse.get_pressed()
    if mouse_st[0]:
        return True
    else:
        return False


class Poly:
    def __init__(self, screen, tup_coor, coor, area, peri, center, color):
        self.screen = screen
        self.tup_coor = tup_coor
        self.coor = coor
        self.area = area
        self.peri = peri
        self.center = center
        self.color = color
        pygame.gfxdraw.aapolygon(screen, self.tup_coor, self.color)
        pygame.gfxdraw.filled_polygon(screen, self.tup_coor, self.color)


def move(list_obj, rank, direction, speed):
    if direction == 1:
        list_obj[rank].coor[:, 0] -= speed
        list_obj[rank].center[0] -= speed
        xp = list_obj[rank].coor[:, 0]
        yp = list_obj[rank].coor[:, 1]
        list_obj[rank].tup_coor = list(zip(xp, yp))

    if direction == 2:
        list_obj[rank].coor[:, 0] += speed
        list_obj[rank].center[0] += speed
        xp = list_obj[rank].coor[:, 0]
        yp = list_obj[rank].coor[:, 1]
        list_obj[rank].tup_coor = list(zip(xp, yp))

    if direction == 3:
        list_obj[rank].coor[:, 1] -= speed
        list_obj[rank].center[1] -= speed
        xp = list_obj[rank].coor[:, 0]
        yp = list_obj[rank].coor[:, 1]
        list_obj[rank].tup_coor = list(zip(xp, yp))

    if direction == 4:
        list_obj[rank].coor[:, 1] += speed
        list_obj[rank].center[1] += speed
        xp = list_obj[rank].coor[:, 0]
        yp = list_obj[rank].coor[:, 1]
        list_obj[rank].tup_coor = list(zip(xp, yp))


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
