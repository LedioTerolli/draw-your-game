import pygame as py
from pygame.locals import *
from pygame import gfxdraw
from cluster import get_data
import cv2

py.init()
edge, new_img, list_obj = get_data("p9.jpg")
scX = new_img.shape[0]
scY = new_img.shape[1]

# print(scX, " ", scY)
# screen = py.display.set_mode((0, 0), py.FULLSCREEN)
screen = py.display.set_mode((scY, scX))
py.display.update()
purple = (74, 20, 140)
white = (255, 255, 255)
red = (255, 23, 68)


class Poly:
    def __init__(self, tup_coor, coor, area, peri, center, color):
        self.tup_coor = tup_coor
        self.coor = coor
        self.area = area
        self.peri = peri
        self.center = center
        self.color = color
        py.gfxdraw.aapolygon(screen, self.tup_coor, self.color)
        py.gfxdraw.filled_polygon(screen, self.tup_coor, self.color)


#   1
# 4   2
#   3
def move(rank, direction, speed):
    if direction == 1:
        list_obj[rank].coor[:, 1] -= speed
        list_obj[rank].center[1] -= speed
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
        list_obj[rank].coor[:, 1] += speed
        list_obj[rank].center[1] += speed
        xp = list_obj[rank].coor[:, 0]
        yp = list_obj[rank].coor[:, 1]
        list_obj[rank].tup_coor = list(zip(xp, yp))

    if direction == 4:
        list_obj[rank].coor[:, 0] -= speed
        list_obj[rank].center[0] -= speed
        xp = list_obj[rank].coor[:, 0]
        yp = list_obj[rank].coor[:, 1]
        list_obj[rank].tup_coor = list(zip(xp, yp))


clock = py.time.Clock()

while 1:

    list_poly = []

    clock.tick(60)
    screen.fill(purple)

    for i in range(len(list_obj)):
        list_poly.append(
            Poly(list_obj[i].tup_coor, list_obj[i].coor, list_obj[i].area, list_obj[i].peri, list_obj[i].center, red))

    # print(list_poly[0].tup_coor)

    for event in py.event.get():

        pressed_down, pressed_up, pressed_left, pressed_right = False, False, False, False

        if event.type == py.QUIT:
            py.display.quit()
            py.quit()
        elif event.type == py.KEYDOWN:
            if event.key == py.K_LEFT:
                pressed_left = True
                move(0, 4, 5)

            if event.key == py.K_RIGHT:
                pressed_right = True
                move(0, 2, 5)

            if event.key == py.K_UP:
                pressed_up = True
                move(0, 1, 5)

            if event.key == py.K_DOWN:
                pressed_down = True
                move(0, 3, 5)

        elif event.type == py.KEYUP:
            if event.key == py.K_LEFT:
                pressed_left = False

            if event.key == py.K_RIGHT:
                pressed_right = False

            if event.key == py.K_UP:
                pressed_up = False

            if event.key == py.K_DOWN:
                pressed_down = False

        elif event.type == py.MOUSEBUTTONDOWN:
            a = py.mouse.get_pos()
            print(a)

    if pressed_left:
        move(0, 4, 5)
    if pressed_right:
        move(0, 2, 5)
    if pressed_up:
        move(0, 1, 5)
    if pressed_down:
        move(0, 3, 5)

    py.display.update()
