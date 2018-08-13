import pygame
import sys
import os
import math

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()
spriteGroup = pygame.sprite.OrderedUpdates()
textboxGroup = pygame.sprite.OrderedUpdates()
gameClock = pygame.time.Clock()
musicPaused = False
hiddenSprites = pygame.sprite.OrderedUpdates()
screenRefresh = True
background = None
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
screen = ""


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


class Background():
    def __init__(self):
        self.colour = pygame.Color("black")
        self.dimensions = 0

    def setTiles(self, tiles):
        if type(tiles) is str:
            self.tiles = [[loadImage(tiles)]]
            self.dimensions = 0
        elif type(tiles[0]) is str:
            self.tiles = [[loadImage(i) for i in tiles], None]
            self.dimensions = 1
        else:
            self.tiles = [[loadImage(i) for i in row] for row in tiles]
            self.dimensions = 2
        self.stagePosX = 0
        self.stagePosY = 0
        self.tileWidth = self.tiles[0][0].get_width()
        self.tileHeight = self.tiles[0][0].get_height()
        screen.blit(self.tiles[0][0], [0, 0])
        self.surface = screen.copy()

    def scroll(self, x, y):
        self.stagePosX -= x
        self.stagePosY -= y
        col = (self.stagePosX % (self.tileWidth * len(self.tiles[0]))) // self.tileWidth
        xOff = (0 - self.stagePosX % self.tileWidth)
        row = (self.stagePosY % (self.tileHeight * len(self.tiles))) // self.tileHeight
        yOff = (0 - self.stagePosY % self.tileHeight)

        col2 = ((self.stagePosX + self.tileWidth) % (self.tileWidth * len(self.tiles[0]))) // self.tileWidth
        row2 = ((self.stagePosY + self.tileHeight) % (self.tileHeight * len(self.tiles))) // self.tileHeight
        screen.blit(self.tiles[row][col], [xOff, yOff])
        screen.blit(self.tiles[row][col2], [xOff + self.tileWidth, yOff])
        screen.blit(self.tiles[row2][col], [xOff, yOff + self.tileHeight])
        screen.blit(self.tiles[row2][col2], [xOff + self.tileWidth, yOff + self.tileHeight])

        self.surface = screen.copy()

    def setColour(self, colour):
        self.colour = parseColour(colour)
        screen.fill(self.colour)
        pygame.display.update()
        self.surface = screen.copy()


class newSprite(pygame.sprite.Sprite):
    def __init__(self, filename, frames=1):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        img = loadImage(filename)
        self.originalWidth = img.get_width() // frames
        self.originalHeight = img.get_height()
        frameSurf = pygame.Surface((self.originalWidth, self.originalHeight), pygame.SRCALPHA, 32)
        x = 0
        for frameNo in range(frames):
            frameSurf = pygame.Surface((self.originalWidth, self.originalHeight), pygame.SRCALPHA, 32)
            frameSurf.blit(img, (x, 0))
            self.images.append(frameSurf.copy())
            x -= self.originalWidth
        self.image = pygame.Surface.copy(self.images[0])

        self.currentImage = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = 0
        self.scale = 1

    def addImage(self, filename):
        self.images.append(loadImage(filename))

    def move(self, xpos, ypos, centre=False):
        if centre:
            self.rect.center = [xpos, ypos]
        else:
            self.rect.topleft = [xpos, ypos]

    def changeImage(self, index):
        self.currentImage = index
        if self.angle == 0 and self.scale == 1:
            self.image = self.images[index]
        else:
            self.image = pygame.transform.rotozoom(self.images[self.currentImage], -self.angle, self.scale)
        oldcenter = self.rect.center
        self.rect = self.image.get_rect()
        originalRect = self.images[self.currentImage].get_rect()
        self.originalWidth = originalRect.width
        self.originalHeight = originalRect.height
        self.rect.center = oldcenter
        self.mask = pygame.mask.from_surface(self.image)
        if screenRefresh:
            updateDisplay()


class newLabel(pygame.sprite.Sprite):
    def __init__(self, text, fontSize, font, fontColour, xpos, ypos, background):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.fontColour = parseColour(fontColour)
        self.fontFace = pygame.font.match_font(font)
        self.fontSize = fontSize
        self.background = background
        self.font = pygame.font.Font(self.fontFace, self.fontSize)
        self.renderText()
        self.rect.topleft = [xpos, ypos]

    def update(self, newText, fontColour, background):
        self.text = newText
        if fontColour:
            self.fontColour = parseColour(fontColour)
        if background:
            self.background = parseColour(background)

        oldTopLeft = self.rect.topleft
        self.renderText()
        self.rect.topleft = oldTopLeft
        if screenRefresh:
            updateDisplay()

    def renderText(self):
        lineSurfaces = []
        textLines = self.text.split("<br>")
        maxWidth = 0
        maxHeight = 0
        for line in textLines:
            lineSurfaces.append(self.font.render(line, True, self.fontColour))
            thisRect = lineSurfaces[-1].get_rect()
            if thisRect.width > maxWidth:
                maxWidth = thisRect.width
            if thisRect.height > maxHeight:
                maxHeight = thisRect.height
        self.image = pygame.Surface((maxWidth, (self.fontSize + 1) * len(textLines) + 5), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        if self.background != "clear":
            self.image.fill(parseColour(self.background))
        linePos = 0
        for lineSurface in lineSurfaces:
            self.image.blit(lineSurface, [0, linePos])
            linePos += self.fontSize + 1
        self.rect = self.image.get_rect()


def loadImage(fileName, useColorKey=False):
    if os.path.isfile(fileName):
        image = pygame.image.load(fileName)
        image = image.convert_alpha()
        # Return the image
        return image
    else:
        raise Exception("Error loading image: " + fileName + " - Check filename and path?")


def screenSize(sizex, sizey, xpos=None, ypos=None, fullscreen=False):
    global screen
    global background
    if xpos != None and ypos != None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (xpos, ypos + 50)
    else:
        windowInfo = pygame.display.Info()
        monitorWidth = windowInfo.current_w
        monitorHeight = windowInfo.current_h
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % ((monitorWidth - sizex) / 2, (monitorHeight - sizey) / 2)
    if fullscreen:
        screen = pygame.display.set_mode([sizex, sizey], pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode([sizex, sizey])
    background = Background()
    screen.fill(background.colour)
    pygame.display.set_caption("Graphics Window")
    background.surface = screen.copy()
    pygame.display.update()
    return screen


def moveSprite(sprite, x, y, centre=False):
    sprite.move(x, y, centre)
    if screenRefresh:
        updateDisplay()


def transformSprite(sprite, angle, scale, hflip=False, vflip=False):
    oldmiddle = sprite.rect.center
    if hflip or vflip:
        tempImage = pygame.transform.flip(sprite.images[sprite.currentImage], hflip, vflip)
    else:
        tempImage = sprite.images[sprite.currentImage]
    if angle != 0 or scale != 1:
        sprite.angle = angle
        sprite.scale = scale
        tempImage = pygame.transform.rotozoom(tempImage, -angle, scale)
    sprite.image = tempImage
    sprite.rect = sprite.image.get_rect()
    sprite.rect.center = oldmiddle
    sprite.mask = pygame.mask.from_surface(sprite.image)
    if screenRefresh:
        updateDisplay()


def setBackgroundColour(colour):
    background.setColour(colour)


def setBackgroundImage(img):
    global background
    background.setTiles(img)


def hideAll():
    hiddenSprites.add(spriteGroup.sprites())
    spriteGroup.empty()
    if screenRefresh:
        updateDisplay()


def showSprite(sprite):
    spriteGroup.add(sprite)
    if screenRefresh:
        updateDisplay()


def makeSprite(filename, frames=1):
    thisSprite = newSprite(filename, frames)
    return thisSprite


def addSpriteImage(sprite, image):
    sprite.addImage(image)


def changeSpriteImage(sprite, index):
    sprite.changeImage(index)


def nextSpriteImage(sprite):
    sprite.currentImage += 1
    if sprite.currentImage > len(sprite.images) - 1:
        sprite.currentImage = 0
    sprite.changeImage(sprite.currentImage)


def touching(sprite1, sprite2):
    collided = pygame.sprite.collide_mask(sprite1, sprite2)
    return collided


def allTouching(spritename):
    if spriteGroup.has(spritename):
        collisions = pygame.sprite.spritecollide(spritename, spriteGroup, False, collided=pygame.sprite.collide_mask)
        collisions.remove(spritename)
        return collisions
    else:
        return []


def makeLabel(text, fontSize, xpos, ypos, fontColour='black', font='Arial', background="clear"):
    # make a text sprite
    thisText = newLabel(text, fontSize, font, fontColour, xpos, ypos, background)
    return thisText


def moveLabel(sprite, x, y):
    sprite.rect.topleft = [x, y]
    if screenRefresh:
        updateDisplay()


def changeLabel(textObject, newText, fontColour=None, background=None):
    textObject.update(newText, fontColour, background)


def clock():
    current_time = pygame.time.get_ticks()
    return current_time


def tick(fps):
    pygame.event.clear()
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_ESCAPE]):
        pygame.quit()
        sys.exit()
    gameClock.tick(fps)
    return gameClock.get_fps()


def showLabel(labelName):
    textboxGroup.add(labelName)
    if screenRefresh:
        updateDisplay()


def hideLabel(labelName):
    textboxGroup.remove(labelName)
    if screenRefresh:
        updateDisplay()


def updateDisplay():
    global background
    spriteRects = spriteGroup.draw(screen)
    textboxRects = textboxGroup.draw(screen)
    pygame.display.update()
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_ESCAPE]):
        pygame.quit()
        sys.exit()
    spriteGroup.clear(screen, background.surface)
    textboxGroup.clear(screen, background.surface)


def mousePressed():
    pygame.event.clear()
    mouseState = pygame.mouse.get_pressed()
    if mouseState[0]:
        return True
    else:
        return False


def spriteClicked(sprite):
    mouseState = pygame.mouse.get_pressed()
    if not mouseState[0]:
        return False  # not pressed
    pos = pygame.mouse.get_pos()
    if sprite.rect.collidepoint(pos):
        return True
    else:
        return False


def parseColour(colour):
    if type(colour) == str:
        # check to see if valid colour
        return pygame.Color(colour)
    else:
        colourRGB = pygame.Color("white")
        colourRGB.r = colour[0]
        colourRGB.g = colour[1]
        colourRGB.b = colour[2]
        return colourRGB


def mouseX():
    x = pygame.mouse.get_pos()
    return x[0]


def mouseY():
    y = pygame.mouse.get_pos()
    return y[1]


def scrollBackground(x, y):
    global background
    background.scroll(x, y)


def set_auto_update(val):
    global screenRefresh
    screenRefresh = val
