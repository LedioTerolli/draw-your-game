from win32api import GetSystemMetrics
from pygame_functions import *
from process import get_data
import random
import sys

screen = screenSize(1920, 1080, True)
screen_size_x = GetSystemMetrics(0)
screen_size_y = GetSystemMetrics(1)
edge, new_img, list_obj = get_data("images/p12.jpg")
scX = new_img.shape[0]
scY = new_img.shape[1]
aster_list = []
black_list = []

for i in range(len(list_obj)):
    area = list_obj[i].area
    if len(list_obj[i].coor) < 4:

        if area > 4000:
            file = "images/planet3_100_5.png"
        elif area > 1000:
            file = "images/planet1_75_7.png"
        else:
            file = "images/planet2_50_5.png"

        stripe = makeSprite("images/stripe_1080_1_dashed.png")
        stripe.move(list_obj[i].center[0], screen_size_y/2, True)
        # stripe.move(list_obj[i].center[0], list_obj[i].center[1], True)
        showSprite(stripe)

        sprite = makeSprite(file)
        sprite.move(list_obj[i].center[0], list_obj[i].center[1], True)
        sprite.x = list_obj[i].center[0]
        sprite.y = list_obj[i].center[1]
        sprite.xspeed = 0
        sprite.yspeed = (area / 250) * ((-1) ** random.randrange(0, 100))
        sprite.changeImage(0)
        aster_list.append(sprite)
        showSprite(sprite)

    else:
        sprite = makeSprite("images/blackhole_50_10.png")
        sprite.move(list_obj[i].center[0], list_obj[i].center[1], True)
        sprite.changeImage(0)
        black_list.append(sprite)
        showSprite(sprite)


mars = makeSprite("images/mars_100_5.png")
mars.move(screen_size_x, screen_size_y / 2, True)
showSprite(mars)

car = makeSprite("images/tesla_base.png")
addSpriteImage(car, "images/tesla_small1.png")
addSpriteImage(car, "images/tesla_small2.png")
car.health = 3
car.xPos = 50
car.xPos = 50
car.yPos = screen_size_y / 2
car.xSpeed = 0
car.ySpeed = 0
car.angle = 0
car.thrustAmount = 0.7
moveSprite(car, 50, screen_size_y / 2, True)
showSprite(car)

life = makeLabel("Life:", 30, 10, 10, "white")
changeLabel(life, "Life: {0}".format(str(car.health)))
showLabel(life)
thrustFrame = 1
nextframe = clock()

calc_fuel = (len(black_list) + len(aster_list)) * 3
car.fuel = calc_fuel
fuel_dis = makeLabel("Fuel:", 30, 10, 40, "white")
changeLabel(fuel_dis, "Fuel: {0}".format(str(car.fuel)))
showLabel(fuel_dis)

fpsDisplay = makeLabel("FPS:", 30, 10, 70, "white")
showLabel(fpsDisplay)

time_pass = clock()
slow_down_rate = 0.1
first_time = 0
first_time_bh = 0

while 1:

    if car.fuel <= 0:
        if first_time == 0:
            time_pass = clock() + 6000
            first_time += 1
        else:
            if time_pass < clock():
                restart(car)
                first_time = 0

    if key_press("r"):
        car.xSpeed = 0
        car.ySpeed = 0
        car.xPos = 50
        car.yPos = screen_size_y / 2


    if key_press("left"):
        car.angle = car.angle - 6
        transformSprite(car, car.angle, 1)
    elif key_press("right"):
        car.angle = car.angle + 6
        transformSprite(car, car.angle, 1)

    if key_press("up"):
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

    elif key_press("down"):
        # slow down
        changeSpriteImage(car, 0)
        if car.xSpeed > 0:
            car.xSpeed -= slow_down_rate
        elif car.xSpeed <= 0:
            car.xSpeed += slow_down_rate
        if car.ySpeed > 0:
            car.ySpeed -= slow_down_rate
        elif car.ySpeed <= 0:
            car.ySpeed += slow_down_rate
    else:
        # auto slow down
        changeSpriteImage(car, 0)
        if car.xSpeed > 0:
            car.xSpeed -= 0.001
        elif car.xSpeed <= 0:
            car.xSpeed += 0.001
        if car.ySpeed > 0:
            car.ySpeed -= 0.001
        elif car.ySpeed <= 0:
            car.ySpeed += 0.001

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


    def restart(car):
        car.health -= 1
        changeLabel(life, "Life: {0}".format(str(car.health)))
        car.xSpeed = 0
        car.ySpeed = 0
        car.xPos = 50
        car.yPos = screen_size_y / 2
        car.fuel = calc_fuel
        changeLabel(fuel_dis, "Fuel: {0}".format(str(car.fuel)))


    def end(car):
        for i in aster_list:
            i.xspeed = 0
            i.yspeed = 0
            car.xSpeed = 0
            car.ySpeed = 0


    def bounce_ver(car):
        car.xSpeed = (-1) * car.xSpeed


    def bounce_hor(car):
        car.ySpeed = (-1) * car.ySpeed

    # hide = int(car.originalWidth)
    hide = 20

    car.xPos += car.xSpeed
    if car.xPos > screen_size_x + hide:
        if car.health > 1:
            restart(car)
        else:
            hideAll()
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
            if first_time_bh == 0:
                rand = len(black_list) - 1
            if hit[-1] != black_list[rand]:
                index = black_list.index(hit[-1])
                rand = random.randrange(0, len(black_list))
                while rand == index:
                    rand = random.randrange(0, len(black_list))
                car.xPos, car.yPos = black_list[rand].rect.center
                first_time_bh += 1
        elif hit[-1] in aster_list:
            if car.health > 1:
                restart(car)
            else:
                hideAll()
        else:
            hideAll()

    fps = tick(60)
    changeLabel(fpsDisplay, "FPS: {0}".format(str(round(fps, 2))))
