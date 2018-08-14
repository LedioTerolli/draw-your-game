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
    cv2.imwrite("images/detection_output.jpg", new_img)
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

            stripe = make_sprite("images/stripe_1080_1_dashed.png")
            stripe.move(list_obj[i].center[0], screen_size_y / 2, True)
            # stripe.move(list_obj[i].center[0], list_obj[i].center[1], True)
            # show_sprite(stripe)

            sprite = make_sprite(file)
            sprite.move(list_obj[i].center[0], list_obj[i].center[1], True)
            sprite.x = list_obj[i].center[0]
            sprite.y = list_obj[i].center[1]
            sprite.xspeed = 0
            sprite.yspeed = (area / 200) * ((-1) ** random.randrange(0, 100))
            sprite.changeImage(0)
            aster_list.append(sprite)
            show_sprite(sprite)

        else:
            sprite = make_sprite("images/wormhole_50_1.png")
            sprite.move(list_obj[i].center[0], list_obj[i].center[1], True)
            sprite.changeImage(0)
            black_list.append(sprite)
            show_sprite(sprite)

    mars = make_sprite("images/mars_100_1.png")
    mars.move(screen_size_x, screen_size_y / 2, True)
    show_sprite(mars)

    # CAR parameters
    car = make_sprite("images/tesla_small0_1.png")
    addSpriteImage(car, "images/tesla_small1_1.png")
    addSpriteImage(car, "images/tesla_small2_1.png")

    car.health = 3
    car.thrustAmount = 0.7

    car.xPos = 20
    car.yPos = screen_size_y / 2
    car.xSpeed = 0
    car.ySpeed = 0
    car.slow_down = 0.05
    car.slow_down_auto = 0.001
    car.speed_lim = 40

    car.angle = 0
    car.angle_speed = 0
    car.angle_change = 0.5
    car.angle_speed_slow_down = 0.05
    car.angle_speed_slow_down_auto = 0.05
    car.angle_speed_lim = 20

    move_sprite(car, car.xPos, car.yPos, True)
    show_sprite(car)

    # labels
    life = make_label("Life:", 30, 10, 10, "white")
    change_label(life, "Life: {0}".format(str(car.health)))
    show_label(life)
    thrust_frame = 1
    nextframe = clock()

    calc_fuel = (len(black_list) + len(aster_list)) * 5
    car.fuel = calc_fuel
    fuel_dis = make_label("Fuel:", 30, 10, 40, "white")
    change_label(fuel_dis, "Fuel: {0}".format(str(car.fuel)))
    show_label(fuel_dis)

    fps_display = make_label("FPS:", 30, 10, 70, "white")
    show_label(fps_display)

    time_pass = clock()

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
            car.angle_speed -= car.angle_change
        elif key_press("right"):
            car.angle_speed += car.angle_change

        elif key_press("up"):
            if car.fuel > 0:
                car.fuel -= 1
                change_label(fuel_dis, "Fuel: {0}".format(str(car.fuel)))
                if clock() > nextframe:
                    nextframe = clock() + 50
                    if thrust_frame == 1:
                        changeSpriteImage(car, 1)
                        thrust_frame = 2
                    else:
                        changeSpriteImage(car, 2)
                        thrust_frame = 1
            else:
                changeSpriteImage(car, 0)

            if car.fuel > 0:
                car.xSpeed += math.sin(math.radians(car.angle)) * car.thrustAmount
                car.ySpeed -= math.cos(math.radians(car.angle)) * car.thrustAmount

            if car.angle_speed != 0:
                if car.angle_speed >= 0:
                    car.angle_speed -= car.angle_speed_slow_down
                else:
                    car.angle_speed += car.angle_speed_slow_down
        elif key_press("down"):
            # slow down
            changeSpriteImage(car, 0)
            if car.xSpeed > 0:
                car.xSpeed -= car.slow_down * abs(car.xSpeed)
            elif car.xSpeed <= 0:
                car.xSpeed += car.slow_down * abs(car.xSpeed)
            if car.ySpeed > 0:
                car.ySpeed -= car.slow_down * abs(car.ySpeed)
            elif car.ySpeed <= 0:
                car.ySpeed += car.slow_down * abs(car.ySpeed)

            # angle speed slow down
            if car.angle_speed != 0:
                if car.angle_speed >= 0:
                    car.angle_speed -= car.angle_speed_slow_down * abs(car.angle_speed)
                else:
                    car.angle_speed += car.angle_speed_slow_down * abs(car.angle_speed)
        else:
            # auto slow down
            changeSpriteImage(car, 0)
            if car.xSpeed > 0:
                car.xSpeed -= car.slow_down_auto * abs(car.xSpeed)
            elif car.xSpeed <= 0:
                car.xSpeed += car.slow_down_auto * abs(car.xSpeed)
            if car.ySpeed > 0:
                car.ySpeed -= car.slow_down_auto * abs(car.ySpeed)
            elif car.ySpeed <= 0:
                car.ySpeed += car.slow_down_auto * abs(car.ySpeed)

            # auto angle slow down
            if car.angle_speed > 0:
                car.angle_speed -= car.angle_speed_slow_down_auto * abs(car.angle_speed)
            else:
                car.angle_speed += car.angle_speed_slow_down_auto * abs(car.angle_speed)

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
            else:
                bounce_ver(car)
        elif car.xPos < -hide:
            bounce_ver(car)
        car.yPos += car.ySpeed
        if car.yPos > screen_size_y + hide:
            bounce_hor(car)
        elif car.yPos < -hide:
            bounce_hor(car)
        move_sprite(car, car.xPos, car.yPos, True)

        # angle speed limit and update angle
        if car.angle_speed > car.angle_speed_lim:
            car.angle_speed = car.angle_speed_lim
        elif car.angle_speed < -car.angle_speed_lim:
            car.angle_speed = -car.angle_speed_lim
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
            move_sprite(i, i.x, i.y, True)

        def restart_game():
            hideAll()
            hideLabel(fps_display)
            hideLabel(fuel_dis)
            hideLabel(life)
            main()

        def restart(car):
            car.health -= 1
            change_label(life, "Life: {0}".format(str(car.health)))
            car.xSpeed = 0
            car.ySpeed = 0
            car.xPos = 50
            car.yPos = screen_size_y / 2
            car.angle_speed = 0
            car.fuel = calc_fuel
            change_label(fuel_dis, "Fuel: {0}".format(str(car.fuel)))
            transformSprite(car, car.angle, 1)

        def bounce_ver(car):
            car.xSpeed = (-1) * car.xSpeed

        def bounce_hor(car):
            car.ySpeed = (-1) * car.ySpeed

        hit = allTouching(car)
        # wormhole algorithm
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
        change_label(fps_display, "FPS: {0}".format(str(round(fps))))
        # change_label(fps_display, "FPS: {0}".format(str(round(fps, 2))))


main()
