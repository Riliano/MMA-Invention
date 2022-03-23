#!/bin/env python
import os
import argparse
import pathlib
import glob

import cv2
import numpy as np

import sqlite3 as sqlite

parser = argparse.ArgumentParser(description='Cretes the database for the videos.')

parser.add_argument('path', type=pathlib.Path, help='The path to videos.')
parser.add_argument('--output', type=pathlib.Path, help='Specify the output file for the database.')

def process_frames(filename, process_func, skip_frames = 1):
    print("Processing: " + filename)
    vid = cv2.VideoCapture(filename)
    if not vid.isOpened():
        print("Error opening video: " + filename)

    frame_count = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(vid.get(cv2.CAP_PROP_FPS))

    frame_list = []
    cur_frame = 0
    while vid.isOpened():
        ret, frame = vid.read()
        cur_frame += 1

        if not ret:
            break
        if cur_frame % skip_frames != 0:
            continue

        print("Frame: " + str(cur_frame) + " / " + str(frame_count), end="\r")

        frame_list.append( (cur_frame, process_func(frame)) )

    print()
    return frame_list

#TODO
def extract_sift(frame):
    return []

def index_framelist(frame_list, filename):
    print("TODO: Insert into DB", filename)


video_types = ('*.mp4', '*.MP4', '*.avi') #webm?
if __name__ == "__main__":
    args = parser.parse_args()
    path = args.path.resolve()

    video_list = []
    for t in video_types:
        regex = str(args.path) + '/' + t
        video_list.extend(glob.glob(regex))

    for v in video_list:
        f = process_frames(v, extract_sift)
        index_framelist(f, v)
