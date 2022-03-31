#!/bin/env python
import os
import argparse
import pathlib

import cv2
import numpy as np

import Localization

parser = argparse.ArgumentParser(description='Query tool for the video database created by <TODO>. Returns a filename for the best match.')

parser.add_argument('query', type=pathlib.Path, help='The path to the query video.')

def processVideo(video, sample_frequency=1):
    frame_number = 0
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    frames_per_sample = fps // sample_frequency

    while video.isOpened() and frame_number < frame_count:
        ret, frame = video.read()
        if frame_number % frames_per_sample == 0:
            localizedFrame = Localization.screen_detection(frame, display_steps=True)
        frame_number += 1

    return "return video name here"

if __name__ == "__main__":
    args = parser.parse_args()
    path = args.query.resolve()

    video = cv2.VideoCapture(str(path.resolve()))

    if (video.isOpened()== False):
        print("Error opening video stream or file. Does the path exist?")

    print('Results for: ' + path.name)
    processVideo(video)
