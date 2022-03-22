import math
import random
from collections import namedtuple
import cv2
import numpy as np

Box = namedtuple('Box', ["minX", "maxX", "minY", "maxY"])

#Seems unused probably should delete
#def rotate_image(image, angle):
#    image_center = tuple(np.array(image.shape[1::-1]) / 2)
#    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
#    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
#    return result

#Seems unused probably should delete
#def getCropBox(image):
#    w = image.shape[0]
#    h = image.shape[1]
#    minX = w
#    maxX = 0
#    minY = h
#    maxY = 0
#    for x in range(0, w):
#        for y in range(0, h):
#            if image[x, y] > 0:
#                minX = min(minX, x)
#                maxX = max(maxX, x)
#                minY = min(minY, y)
#                maxY = max(maxY, y)
#    maxX += 1
#    maxY += 1
#    return Box(minX, maxX, minY, maxY)

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
    return Box(minX-inflate, maxX+inflate, minY-inflate, maxY+inflate)

def isInvalidImage(image):
    if image is None or image.shape[0] < 10 or image.shape[1] < 30:
        return True
    return False

def binarize(screen):
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    screen = cv2.adaptiveThreshold(screen, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 8)
    screen = cv2.morphologyEx(screen, cv2.MORPH_RECT, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)))

    return screen

# we might wanna include the brightness of the screen
def localize(screen, display_steps=False):
    mask = cv2.bitwise_not(binarize(screen))
    contours, h = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cs = []
    for c in contours:
        b = contourToBox(c, 0)
        widthRatio = (b[3] - b[2] + 1) / (b[1] - b[0] + 1)

        if (b[3] - b[2]) * (b[1] - b[0]) < (screen.shape[0] * screen.shape[1]) / 8 or not (1.4 < widthRatio < 1.8 or 1.4 < 1 / widthRatio < 1.8):
            continue
        cs.append(c)
        s = screen[b.minX:b.maxX, b.minY:b.maxY]
        return s

    return None


#Seems unused probably should delete
# # get rotation angle from a cropped plate so it would be axis aligned.
# def rotateScreen(screen):
#     if isInvalidImage(screen):
#         return None
#     edges = cv2.Canny(screen, 50, 200, None, 3)
#     lines = cv2.HoughLines(edges, 1, np.pi / 180, 20, None, 0, 0)
#
#     # get first line
#     if lines is None:
#         return screen
#
#     rho = lines[0][0][0]
#     theta = lines[0][0][1]
#     a = math.cos(theta)
#     b = math.sin(theta)
#     x0 = a * rho
#     y0 = b * rho
#     pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * a))
#     pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * a))
#     slope = (pt2[1] - pt1[1]) / max((pt2[0] - pt1[0]), 1)
#
#     angle = np.rad2deg(np.arctan(slope))
#     r_screen = rotate_image(screen, angle)
#
#     return localize(r_screen)

def screen_detection(image, display_steps=False):
    screen = localize(image, display_steps)

    if display_steps and screen is not None:
        cv2.imshow("localized screen", screen)
        cv2.waitKey(0)

    return screen
