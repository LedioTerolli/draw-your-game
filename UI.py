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

xPos = 50
yPos = screen_size_y / 2
xSpeed = 0
ySpeed = 0
angle = 0
angle_obj = 0
thrustAmount = 0.5
car = makeSprite("images/tesla_small.png")
addSpriteImage(car, "images/tesla_small1.png")
addSpriteImage(car, "images/tesla_small2.png")
moveSprite(car, 50, screen_size_y / 2, True)
showSprite(car)
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
        sprite.yspeed = (area/300) * ((-1) ** random.randrange(0, 100))
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
        sprite.changeImage(0)
        sprite.rot = (-1) ** random.randrange(0, 100)
        black_list.append(sprite)
        showSprite(sprite)

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

    '''for i in black_list:
        angle_obj = angle_obj - i.rot
        scale = i.scale
        transformSprite(i, angle_obj, scale)'''

    if keyPressed("left"):
        angle = angle - 6
        transformSprite(car, angle, 1)
    elif keyPressed("right"):
        angle = angle + 6
        transformSprite(car, angle, 1)

    if keyPressed("up"):
        if clock() > nextframe:
            nextframe = clock() + 50
            if thrustFrame == 1:
                changeSpriteImage(car, 1)
                thrustFrame = 2
            else:
                changeSpriteImage(car, 2)
                thrustFrame = 1
        xSpeed += math.sin(math.radians(angle)) * thrustAmount
        ySpeed -= math.cos(math.radians(angle)) * thrustAmount
    elif keyPressed("down"):
        changeSpriteImage(car, 0)
        if xSpeed > 0:
            xSpeed -= 0.2
        elif xSpeed <= 0:
            xSpeed += 0.2
        if ySpeed > 0:
            ySpeed -= 0.2
        elif ySpeed <= 0:
            ySpeed += 0.2
    else:
        changeSpriteImage(car, 0)

    hide = int(car.originalWidth)

    xPos += xSpeed
    if xPos > screen_size_x + hide:
        xPos = -hide
    elif xPos < -hide:
        xPos = screen_size_x
    yPos += ySpeed
    if yPos > screen_size_y:
        yPos = -hide
    elif yPos < -hide:
        yPos = screen_size_y
    moveSprite(car, xPos, yPos, True)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
