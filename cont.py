import numpygame as np
import matplotlib.pygameplot as plt
import cv2
import time
import random

# contour.pygame
# print('Enter file...')
# filename = input()
# filename = "%s" % filename


im = cv2.imread('sq3.png')
# imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

blurred_frame = cv2.GaussianBlur(im, (5, 5), 0)

hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

lower_blue = np.array([170, 50, 50])
upper_blue = np.array([180, 255, 255])
mask = cv2.inRange(hsv, lower_blue, upper_blue)

ret, thresh = cv2.threshold(blurred_frame, 127, 255, cv2.THRESH_TOZERO)

im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

for contour in contours:
    area = cv2.contourArea(contour)

    if area > 10000:
        cv2.drawContours(im, contour, -1, (0, 255, 0), 3)

cv2.imshow('thresh', thresh)
cv2.imshow('image', im)
cv2.waitKey(0)


# epsilon = 0.1 * cv2.arcLength(cnt, True)
# approx = cv2.approxPolyDP(cnt, epsilon, True)
# edge = cv2.Canny(img, 100, 200)
# M = cv2.moments(cnt)

def print_img(matr):
    hor_size = matr.shape[1]
    hh = 300

    if hor_size > hh:
        shrink = hh / hor_size
        matr = cv2.resize(matr, (0, 0), fx=shrink, fy=shrink)

    rows = matr.shape[0]
    cols = matr.shape[1]

    new_val = [0, 35, 60, 90, 125, 160, 185, 210, 235]
    char = [' ', '.', ',', ':', '!', '?', '$', '@', '0']
    # char = list(reversed(char))

    for x in range(0, rows):
        for y in range(0, cols):
            for i in reversed(range(len(char))):
                if matr[x, y].astype(int) >= new_val[i]:
                    print('{:<2}'.format(char[i]), end="")
                    break

        time.sleep(random.randint(0, 50) * random.randint(0, 50) * 0.00001)
        print()

# print_img(matr)
