import pygame
from pygame.locals import *
from pygame import gfxdraw
from process import get_data
import cv2

pygame.init()
edge, new_img, list_obj = get_data("p10.jpg")
scX = new_img.shape[0]
scY = new_img.shape[1]
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# screen = pygame.display.set_mode((scY, scX))
pygame.display.update()
purple = (74, 20, 140)
white = (255, 255, 255)
red = (255, 23, 68)
blue = (0, 0, 255)
clock = pygame.time.Clock()
mouse_pos = []
list_custom = []


class Poly:
    def __init__(self, tup_coor, coor, area, peri, center, color):
        self.tup_coor = tup_coor
        self.coor = coor
        self.area = area
        self.peri = peri
        self.center = center
        self.color = color
        pygame.gfxdraw.aapolygon(screen, self.tup_coor, self.color)
        pygame.gfxdraw.filled_polygon(screen, self.tup_coor, self.color)


#   3
# 1   2
#   4
def move(rank, direction, speed):
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


keydict = {"space": pygame.K_SPACE, "esc": pygame.K_ESCAPE, "up": pygame.K_UP, "down": pygame.K_DOWN,
           "left": pygame.K_LEFT, "right": pygame.K_RIGHT,
           "a": pygame.K_a,
           "b": pygame.K_b,
           "c": pygame.K_c,
           "d": pygame.K_d,
           "e": pygame.K_e,
           "f": pygame.K_f,
           "g": pygame.K_g,
           "h": pygame.K_h,
           "i": pygame.K_i,
           "j": pygame.K_j,
           "k": pygame.K_k,
           "l": pygame.K_l,
           "m": pygame.K_m,
           "n": pygame.K_n,
           "o": pygame.K_o,
           "p": pygame.K_p,
           "q": pygame.K_q,
           "r": pygame.K_r,
           "s": pygame.K_s,
           "t": pygame.K_t,
           "u": pygame.K_u,
           "v": pygame.K_v,
           "w": pygame.K_w,
           "x": pygame.K_x,
           "y": pygame.K_y,
           "z": pygame.K_z,
           "1": pygame.K_1,
           "2": pygame.K_2,
           "3": pygame.K_3,
           "4": pygame.K_4,
           "5": pygame.K_5,
           "6": pygame.K_6,
           "7": pygame.K_7,
           "8": pygame.K_8,
           "9": pygame.K_9,
           "0": pygame.K_0}


def keyPress(keyCheck=""):
    pygame.event.clear()
    keys = pygame.key.get_pressed()
    if sum(keys) > 0:
        if keyCheck == "" or keys[keydict[keyCheck.lower()]]:
            return True
    return False


def mousePress():
    pygame.event.clear()
    mouse_st = pygame.mouse.get_pressed()
    if mouse_st[0]:
        return True
    else:
        return False


while 1:

    list_poly = []
    speed = 10
    clock.tick(90)
    screen.fill(purple)

    for i in range(len(list_obj)):
        list_poly.append(
            Poly(list_obj[i].tup_coor, list_obj[i].coor, list_obj[i].area, list_obj[i].peri, list_obj[i].center, red))

    for i in mouse_pos:
        pygame.gfxdraw.aacircle(screen, i[0], i[1], 2, white)
        pygame.gfxdraw.filled_circle(screen, i[0], i[1], 2, white)

    for i in range(len(list_custom)):
        if len(list_custom[i]) == 0:
            continue
        elif len(list_custom[i]) == 1:
            pygame.gfxdraw.aacircle(screen, (list_custom[i])[0][0], (list_custom[i])[0][1], 4, white)
            pygame.gfxdraw.filled_circle(screen, (list_custom[i])[0][0], (list_custom[i])[0][1], 4, white)

        elif len(list_custom[i]) == 2:
            pygame.gfxdraw.line(screen, (list_custom[i])[0][0], (list_custom[i])[0][1], (list_custom[i])[1][0],
                                (list_custom[i])[1][1], white)

        else:
            pygame.gfxdraw.aapolygon(screen, list_custom[i], white)
            pygame.gfxdraw.filled_polygon(screen, list_custom[i], white)

    if keyPress("left"):
        move(0, 1, speed)
    elif keyPress("right"):
        move(0, 2, speed)
    elif keyPress("up"):
        move(0, 3, speed)
    elif keyPress("down"):
        move(0, 4, speed)
    elif keyPress("space"):
        list_custom.append(mouse_pos)
        mouse_pos = []
    elif keyPress("esc"):
        pygame.display.quit()
        pygame.quit()

    if mousePress():
        a = pygame.mouse.get_pos()
        if len(mouse_pos) == 0:
            mouse_pos.append(a)
        if mouse_pos[-1] != a:
            mouse_pos.append(a)

        '''             smooth controls 

        pressed_down, pressed_up, pressed_left, pressed_right = False, False, False, False

        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pressed_left = True

            if event.key == pygame.K_RIGHT:
                pressed_right = True

            if event.key == pygame.K_UP:
                pressed_up = True

            if event.key == pygame.K_DOWN:
                pressed_down = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                pressed_left = False

            if event.key == pygame.K_RIGHT:
                pressed_right = False

            if event.key == pygame.K_UP:
                pressed_up = False

            if event.key == pygame.K_DOWN:
                pressed_down = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            a = pygame.mouse.get_pos()
            print(a)

    if pressed_left:
        move(0, 4, 5)
    if pressed_right:
        move(0, 2, 5)
    if pressed_up:
        move(0, 1, 5)
    if pressed_down:
        move(0, 3, 5)
        
    '''

    pygame.display.update()
