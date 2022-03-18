#!/bin/env python

import cv2
import numpy as np

noise = np.random.rand(600, 300) * 255

cv2.imshow("Noise", noise)
cv2.waitKey()


