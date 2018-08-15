import pygame
import sys
import os
import math

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()
sprite_group = pygame.sprite.OrderedUpdates()
textbox_group = pygame.sprite.OrderedUpdates()
game_clock = pygame.time.Clock()
hidden_sprites = pygame.sprite.OrderedUpdates()
screen_refresh = True
background = None
key_codes = {"space": pygame.K_SPACE, "esc": pygame.K_ESCAPE, "up": pygame.K_UP, "down": pygame.K_DOWN,
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
        if key_check == "" or keys[key_codes[key_check.lower()]]:
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


class the_background():
    def __init__(self):
        self.colour = pygame.Color("black")
        self.dimensions = 0

    def setTiles(self, tiles):
        if type(tiles) is str:
            self.tiles = [[load_image(tiles)]]
            self.dimensions = 0
        elif type(tiles[0]) is str:
            self.tiles = [[load_image(i) for i in tiles], None]
            self.dimensions = 1
        else:
            self.tiles = [[load_image(i) for i in row] for row in tiles]
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
        self.colour = parse_colour(colour)
        screen.fill(self.colour)
        pygame.display.update()
        self.surface = screen.copy()


class new_sprite(pygame.sprite.Sprite):
    def __init__(self, filename, frames=1):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        img = load_image(filename)
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
        self.images.append(load_image(filename))

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
        if screen_refresh:
            update_display()


class new_label(pygame.sprite.Sprite):
    def __init__(self, text, fontSize, font, fontColour, xpos, ypos, background):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.fontColour = parse_colour(fontColour)
        self.fontFace = pygame.font.match_font(font)
        self.fontSize = fontSize
        self.background = background
        self.font = pygame.font.Font(self.fontFace, self.fontSize)
        self.renderText()
        self.rect.topleft = [xpos, ypos]

    def update(self, newText, fontColour, background):
        self.text = newText
        if fontColour:
            self.fontColour = parse_colour(fontColour)
        if background:
            self.background = parse_colour(background)

        oldTopLeft = self.rect.topleft
        self.renderText()
        self.rect.topleft = oldTopLeft
        if screen_refresh:
            update_display()

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
            self.image.fill(parse_colour(self.background))
        linePos = 0
        for lineSurface in lineSurfaces:
            self.image.blit(lineSurface, [0, linePos])
            linePos += self.fontSize + 1
        self.rect = self.image.get_rect()


def load_image(fileName, useColorKey=False):
    if os.path.isfile(fileName):
        image = pygame.image.load(fileName)
        image = image.convert_alpha()
        return image
    else:
        raise Exception("Error loading image: " + fileName + " - Check filename and path?")


def screen_size(sizex, sizey, xpos=None, ypos=None, fullscreen=False):
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
    background = the_background()
    screen.fill(background.colour)
    pygame.display.set_caption("Graphics Window")
    background.surface = screen.copy()
    pygame.display.update()
    return screen


def move_sprite(sprite, x, y, centre=False):
    sprite.move(x, y, centre)
    if screen_refresh:
        update_display()


def add_sprite_image(sprite, image):
    sprite.addImage(image)


def change_sprite_image(sprite, index):
    sprite.changeImage(index)


def next_sprite_image(sprite):
    sprite.currentImage += 1
    if sprite.currentImage > len(sprite.images) - 1:
        sprite.currentImage = 0
    sprite.changeImage(sprite.currentImage)


def colliding(sprite1, sprite2):
    collided = pygame.sprite.collide_mask(sprite1, sprite2)
    return collided


def transform_sprite(sprite, angle, scale, hflip=False, vflip=False):
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
    if screen_refresh:
        update_display()


def set_background_colour(colour):
    background.setColour(colour)


def set_background_image(img):
    global background
    background.setTiles(img)


def hide_all():
    hidden_sprites.add(sprite_group.sprites())
    sprite_group.empty()
    if screen_refresh:
        update_display()


def show_sprite(sprite):
    sprite_group.add(sprite)
    if screen_refresh:
        update_display()


def make_sprite(filename, frames=1):
    thisSprite = new_sprite(filename, frames)
    return thisSprite


def all_colliding(spritename):
    if sprite_group.has(spritename):
        collisions = pygame.sprite.spritecollide(spritename, sprite_group, False, collided=pygame.sprite.collide_mask)
        collisions.remove(spritename)
        return collisions
    else:
        return []


def make_label(text, fontSize, xpos, ypos, fontColour='black', font='Arial', background="clear"):
    # make a text sprite
    thisText = new_label(text, fontSize, font, fontColour, xpos, ypos, background)
    return thisText


def mouse_pressed():
    pygame.event.clear()
    mouseState = pygame.mouse.get_pressed()
    if mouseState[0]:
        return True
    else:
        return False


def sprite_clicked(sprite):
    mouseState = pygame.mouse.get_pressed()
    if not mouseState[0]:
        return False  # not pressed
    pos = pygame.mouse.get_pos()
    if sprite.rect.collidepoint(pos):
        return True
    else:
        return False


def parse_colour(colour):
    if type(colour) == str:
        # check to see if valid colour
        return pygame.Color(colour)
    else:
        colourRGB = pygame.Color("white")
        colourRGB.r = colour[0]
        colourRGB.g = colour[1]
        colourRGB.b = colour[2]
        return colourRGB


def pause(milliseconds, allowEsc=True):
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()
    waittime = current_time + milliseconds
    while not (current_time > waittime or (keys[pygame.K_ESCAPE] and allowEsc)):
        pygame.event.clear()
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_ESCAPE] and allowEsc):
            pygame.quit()
            sys.exit()
        current_time = pygame.time.get_ticks()


def hide_sprite(sprite):
    hidden_sprites.add(sprite)
    sprite_group.remove(sprite)
    if screen_refresh:
        update_display()


def move_label(sprite, x, y):
    sprite.rect.topleft = [x, y]
    if screen_refresh:
        update_display()


def change_label(textObject, newText, fontColour=None, background=None):
    textObject.update(newText, fontColour, background)


def clock():
    current_time = pygame.time.get_ticks()
    return current_time


def tick(fps):
    pygame.event.clear()
    keys = pygame.key.get_pressed()
    game_clock.tick(fps)
    return game_clock.get_fps()


def show_label(labelName):
    textbox_group.add(labelName)
    if screen_refresh:
        update_display()


def hide_label(labelName):
    textbox_group.remove(labelName)
    if screen_refresh:
        update_display()


def update_display():
    global background
    spriteRects = sprite_group.draw(screen)
    textboxRects = textbox_group.draw(screen)
    pygame.display.update()
    keys = pygame.key.get_pressed()
    sprite_group.clear(screen, background.surface)
    textbox_group.clear(screen, background.surface)
