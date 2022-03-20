#!/bin/env python
import os

import cv2
import numpy as np

import Localization


def processFrame(frame, display_steps=True):
    localizedFrame = Localization.screen_detection(frame, display_steps)


def processVideo(video, sample_frequency=1):
    frame_number = 0
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    frames_per_sample = fps // sample_frequency

    while video.isOpened and frame_number < frame_count:
        ret, frame = video.read()
        if frame_number % frames_per_sample == 0:
            processFrame(frame)
        frame_number += 1


def getVideo(index=0):
    path = "Input Videos/" + os.listdir("Input Videos")[index]
    return cv2.VideoCapture(path)

def main():
    video = getVideo()
    processVideo(video)


if __name__ == "__main__":
    main()
