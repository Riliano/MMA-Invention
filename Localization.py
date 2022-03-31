import math
import random
from collections import namedtuple
import cv2
import numpy as np

Box = namedtuple('Box', ["minX", "maxX", "minY", "maxY"])


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


def contourToBox(contour, inflate=0):
    minX = float('inf')
    maxX = 0
    minY = float('inf')
    maxY = 0
    for C in contour:
        c = C[0]
        x = c[1]
        y = c[0]
        minX = min(minX, x)
        maxX = max(maxX, x)
        minY = min(minY, y)
        maxY = max(maxY, y)
    return Box(minX - inflate, maxX + inflate, minY - inflate, maxY + inflate)


def isInvalidImage(image):
    if image is None or image.shape[0] < 10 or image.shape[1] < 30:
        return True
    return False


def binarize(screen):
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    screen = cv2.Canny(screen, 50, 100, 1)
    screen = cv2.morphologyEx(screen, cv2.MORPH_DILATE, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
    screen = cv2.bitwise_not(screen)

    return screen


# we might wanna include the brightness of the screen
def localize(screen, display_steps=False, takeExternal=True):
    mask = binarize(screen)
    mask = mask if takeExternal else cv2.bitwise_not(mask)
    contours, h = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if display_steps:
        screenCopy = mask.copy()
        screenCopy = cv2.cvtColor(screenCopy, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(image=screenCopy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
        cv2.imshow("contours screen", screenCopy)

    cs = []
    for c in contours:
        b = contourToBox(c, 0)
        widthRatio = (b[3] - b[2] + 1) / (b[1] - b[0] + 1)
        surface = (b[3] - b[2]) * (b[1] - b[0])
        if surface < (screen.shape[0] * screen.shape[1]) / 8 or surface > (screen.shape[0] * screen.shape[1]) / 1.2 or not 1.4 < widthRatio < 1.9: #or 1.4 < 1 / widthRatio < 1.8):
            continue
        cs.append(c)
        s = screen[b.minX:b.maxX, b.minY:b.maxY]
        return s

    if takeExternal:
        return localize(screen, display_steps, False)
    return screen


def screen_detection(image, display_steps=False):
    screen = localize(image, display_steps)

    if display_steps and screen is not None:
        cv2.imshow("localized screen", screen)
        cv2.waitKey(0)

    return screen
