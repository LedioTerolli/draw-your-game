from process import get_data
from pygame_functions import *
import random
import sys
from win32api import GetSystemMetrics

screen = screenSize(1920, 1080, True)
screen_size_x = GetSystemMetrics(0)
screen_size_y = GetSystemMetrics(1)
edge, new_img, list_obj = get_data("images/p12.jpg")
scX = new_img.shape[0]
scY = new_img.shape[1]
mouse_pos = []
list_custom = []
aster_list = []
black_list = []

angle_obj = 0
car = makeSprite("images/tesla_small.png")
addSpriteImage(car, "images/tesla_small1.png")
addSpriteImage(car, "images/tesla_small2.png")
car.health = 3
car.xPos = 50
car.xPos = 50
car.yPos = screen_size_y / 2
car.xSpeed = 0
car.ySpeed = 0
car.angle = 0
car.thrustAmount = 0.5
moveSprite(car, 50, screen_size_y / 2, True)
showSprite(car)
life = makeLabel("Life:", 30, 10, 10, "white")
changeLabel(life, "Life: {0}".format(str(car.health)))
showLabel(life)
thrustFrame = 1
nextframe = clock()
n = 0

for i in range(len(list_obj)):
    area = list_obj[i].area
    if len(list_obj[i].coor) < 4:

        if area > 4000:
            file = "images/planet3small.png"
        elif area > 1000:
            file = "images/planet1small.png"
        else:
            file = "images/planet2small.png"

        sprite = makeSprite(file)
        sprite.move(list_obj[i].center[0], list_obj[i].center[1], True)
        sprite.x = list_obj[i].center[0]
        sprite.y = list_obj[i].center[1]
        sprite.xspeed = 0
        sprite.yspeed = (area / 300) * ((-1) ** random.randrange(0, 100))
        sprite.scale = area / (area + 1000)
        sprite.angle = 0
        sprite.rot = ((-1) ** random.randrange(0, 100))
        sprite.changeImage(0)
        aster_list.append(sprite)
        showSprite(sprite)

    else:
        sprite = makeSprite("images/blackhole.png")
        sprite.move(list_obj[i].center[0], list_obj[i].center[1], True)
        sprite.scale = area / 3000
        sprite.rot = (-1) ** random.randrange(0, 100)
        black_list.append(sprite)
        showSprite(sprite)

mars = makeSprite("images/mars_small.png")
mars.move(screen_size_x, screen_size_y / 2, True)
showSprite(mars)

calc_fuel = (len(black_list) + len(aster_list)) * 10
car.fuel = calc_fuel
fuel_dis = makeLabel("Fuel:", 30, 10, 40, "white")
changeLabel(fuel_dis, "Fuel: {0}".format(str(car.fuel)))
showLabel(fuel_dis)

while 1:

    tick(120)

    for i in aster_list:
        hide = int(i.originalWidth)

        i.x += i.xspeed
        if i.x > screen_size_x + hide:
            i.x = -hide
        elif i.x < -hide:
            i.x = screen_size_x + hide

        i.y += i.yspeed
        if i.y > screen_size_y + hide:
            i.y = -hide
        elif i.y < -hide:
            i.y = screen_size_y + hide
        moveSprite(i, i.x, i.y, True)

    if keyPressed("left"):
        car.angle = car.angle - 6
        transformSprite(car, car.angle, 1)
    elif keyPressed("right"):
        car.angle = car.angle + 6
        transformSprite(car, car.angle, 1)

    if keyPressed("up"):
        if car.fuel > 0:
            car.fuel -= 1
            changeLabel(fuel_dis, "Fuel: {0}".format(str(car.fuel)))

            if clock() > nextframe:
                nextframe = clock() + 50
                if thrustFrame == 1:
                    changeSpriteImage(car, 1)
                    thrustFrame = 2
                else:
                    changeSpriteImage(car, 2)
                    thrustFrame = 1

        if car.fuel > 0:
            car.xSpeed += math.sin(math.radians(car.angle)) * car.thrustAmount
            car.ySpeed -= math.cos(math.radians(car.angle)) * car.thrustAmount

    elif keyPressed("down"):
        changeSpriteImage(car, 0)
        if car.xSpeed > 0:
            car.xSpeed -= 0.2
        elif car.xSpeed <= 0:
            car.xSpeed += 0.2
        if car.ySpeed > 0:
            car.ySpeed -= 0.2
        elif car.ySpeed <= 0:
            car.ySpeed += 0.2
    else:
        changeSpriteImage(car, 0)
        if car.xSpeed > 0:
            car.xSpeed -= 0.01
        elif car.xSpeed <= 0:
            car.xSpeed += 0.01
        if car.ySpeed > 0:
            car.ySpeed -= 0.01
        elif car.ySpeed <= 0:
            car.ySpeed += 0.01

    hide = int(car.originalWidth)


    def restart(car):
        car.health -= 1
        changeLabel(life, "Life: {0}".format(str(car.health)))
        car.xSpeed = 0
        car.ySpeed = 0
        car.xPos = 50
        car.yPos = screen_size_y / 2
        car.fuel = calc_fuel
        changeLabel(fuel_dis, "Fuel: {0}".format(str(car.fuel)))


    def bounce_ver(car):
        car.xSpeed = (-1) * car.xSpeed


    def bounce_hor(car):
        car.ySpeed = (-1) * car.ySpeed


    car.xPos += car.xSpeed
    if car.xPos > screen_size_x + hide:
        restart(car)
    elif car.xPos < -hide:
        bounce_ver(car)
    car.yPos += car.ySpeed
    if car.yPos > screen_size_y + hide:
        bounce_hor(car)
    elif car.yPos < -hide:
        bounce_hor(car)
    moveSprite(car, car.xPos, car.yPos, True)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    hit = allTouching(car)

    if len(hit) > 0:
        if hit[-1] in black_list:
            index = black_list.index(hit[-1])
            rand = random.randrange(0, len(black_list))
            while rand == index:
                rand = random.randrange(0, len(black_list))
            car.xPos, car.yPos = black_list[rand].rect.topleft
        elif hit[-1] in aster_list:
            if car.health > 1:
                restart(car)

            else:
                for i in aster_list:
                    i.xspeed = 0
                    i.yspeed = 0
                    car.xSpeed = 0
                    car.ySpeed = 0
        else:
            for i in aster_list:
                i.xspeed = 0
                i.yspeed = 0
                car.xSpeed = 0
                car.ySpeed = 0
