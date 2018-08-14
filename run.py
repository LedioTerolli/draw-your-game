from win32api import GetSystemMetrics
from pygame_functions import *
from image_process import get_data
import random
import sys
import cv2


def main():
    screen = screenSize(1920, 1080, True)
    setBackgroundImage("images/bg_max.jpg")
    screen_size_x = GetSystemMetrics(0)
    screen_size_y = GetSystemMetrics(1)
    edge, new_img, list_obj = get_data("images/p16.jpg")
    cv2.imwrite("detection_output.jpg", new_img)
    aster_list = []
    black_list = []

    for i in range(len(list_obj)):
        area = list_obj[i].area
        if len(list_obj[i].coor) < 4:

            if area > 2000:
                file = "images/planet3_100_1.png"
            elif area > 1000:
                file = "images/planet1_75_1.png"
            else:
                file = "images/planet2_50_1.png"

            stripe = makeSprite("images/stripe_1080_1_dashed.png")
            stripe.move(list_obj[i].center[0], screen_size_y / 2, True)
            # stripe.move(list_obj[i].center[0], list_obj[i].center[1], True)
            # showSprite(stripe)

            sprite = makeSprite(file)
            sprite.move(list_obj[i].center[0], list_obj[i].center[1], True)
            sprite.x = list_obj[i].center[0]
            sprite.y = list_obj[i].center[1]
            sprite.xspeed = 0
            sprite.yspeed = (area / 200) * ((-1) ** random.randrange(0, 100))
            sprite.changeImage(0)
            aster_list.append(sprite)
            showSprite(sprite)

        else:
            sprite = makeSprite("images/wormhole_50_1.png")
            sprite.move(list_obj[i].center[0], list_obj[i].center[1], True)
            sprite.changeImage(0)
            black_list.append(sprite)
            showSprite(sprite)

    mars = makeSprite("images/mars_100_1.png")
    mars.move(screen_size_x, screen_size_y / 2, True)
    showSprite(mars)

    car = makeSprite("images/tesla_small0_1.png")
    addSpriteImage(car, "images/tesla_small1_1.png")
    addSpriteImage(car, "images/tesla_small2_1.png")
    car.health = 3
    car.xPos = 20
    car.yPos = screen_size_y / 2
    car.xSpeed = 0
    car.ySpeed = 0
    car.angle = 0
    car.angle_speed = 0
    car.angle_sp_lim = 20
    car.speed_lim = 30
    car.thrustAmount = 0.8
    moveSprite(car, car.xPos, car.yPos, True)
    showSprite(car)

    life = makeLabel("Life:", 30, 10, 10, "white")
    changeLabel(life, "Life: {0}".format(str(car.health)))
    showLabel(life)
    thrustFrame = 1
    nextframe = clock()

    calc_fuel = (len(black_list) + len(aster_list)) * 5
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
                if car.health > 1:
                    if time_pass < clock():
                        restart(car)
                        first_time = 0
                        first_time_bh = 0
                else:
                    if time_pass < clock():
                        first_time = 0
                        restart_game()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        if key_press("r"):
            car.xSpeed = 0
            car.ySpeed = 0
            car.xPos = 50
            car.yPos = screen_size_y / 2
            car.angle_speed = 0
            car.angle = 0
            transformSprite(car, car.angle, 1)

        if key_press("left"):
            car.angle_speed -= 0.5
        elif key_press("right"):
            car.angle_speed += 0.5

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

            else:
                changeSpriteImage(car, 0)

            if car.fuel > 0:
                car.xSpeed += math.sin(math.radians(car.angle)) * car.thrustAmount
                car.ySpeed -= math.cos(math.radians(car.angle)) * car.thrustAmount

            if car.angle_speed != 0:
                if car.angle_speed >= 0:
                    car.angle_speed -= 0.1
                else:
                    car.angle_speed += 0.1

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

            if car.angle_speed != 0:
                if car.angle_speed >= 0:
                    car.angle_speed -= 0.1
                else:
                    car.angle_speed += 0.1
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

        # auto angle slow down
        if car.angle_speed > 0:
            car.angle_speed -= 0.1
        else:
            car.angle_speed += 0.1

        hide = 20

        # car speed limit
        if car.xSpeed > car.speed_lim:
            car.xSpeed = car.speed_lim
        elif car.xSpeed < -car.speed_lim:
            car.xSpeed = -car.speed_lim
        if car.ySpeed > car.speed_lim:
            car.ySpeed = car.speed_lim
        elif car.ySpeed < -car.speed_lim:
            car.ySpeed = -car.speed_lim

        # update position and bounce
        car.xPos += car.xSpeed
        if car.xPos > screen_size_x + hide:
            if car.health > 1:
                bounce_ver(car)
                # restart(car)
            else:
                bounce_ver(car)
                # restart_game()
        elif car.xPos < -hide:
            bounce_ver(car)
        car.yPos += car.ySpeed
        if car.yPos > screen_size_y + hide:
            bounce_hor(car)
        elif car.yPos < -hide:
            bounce_hor(car)
        moveSprite(car, car.xPos, car.yPos, True)

        # angle speed limit and update angle
        if car.angle_speed > car.angle_sp_lim:
            car.angle_speed = car.angle_sp_lim
        elif car.angle_speed < -car.angle_sp_lim:
            car.angle_speed = -car.angle_sp_lim
        car.angle += car.angle_speed
        transformSprite(car, car.angle, 1)

        # update asteroid position
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

        def restart_game():
            hideAll()
            hideLabel(fpsDisplay)
            hideLabel(fuel_dis)
            hideLabel(life)
            main()

        def restart(car):
            car.health -= 1
            changeLabel(life, "Life: {0}".format(str(car.health)))
            car.xSpeed = 0
            car.ySpeed = 0
            car.xPos = 50
            car.yPos = screen_size_y / 2
            car.angle_speed = 0
            car.fuel = calc_fuel
            changeLabel(fuel_dis, "Fuel: {0}".format(str(car.fuel)))
            transformSprite(car, car.angle, 1)

        def bounce_ver(car):
            car.xSpeed = (-1) * car.xSpeed

        def bounce_hor(car):
            car.ySpeed = (-1) * car.ySpeed

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
                    first_time_bh = 0
                else:
                    restart_game()
            else:
                restart_game()

        fps = tick(60)
        changeLabel(fpsDisplay, "FPS: {0}".format(str(round(fps, 2))))


main()
