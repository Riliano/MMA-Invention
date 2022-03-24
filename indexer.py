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
        print(frame_list)

    print()
    print("Done", frame_list)
    return frame_list

#TODO

sift = cv2.SIFT_create()
def extract_sift(frame):

    # note!!
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    kp, desc = sift.detectAndCompute(gray, None)
    print(desc)
    return desc

def index_framelist(frame_list, filename):
    print("TODO: Insert into DB", filename)


video_types = ('*.mp4', '*.MP4', '*.avi') #webm?
if __name__ == "__main__":
    args = parser.parse_args()
    path = args.path.resolve()

# "Inspired" by dbt.py
#    #db_name = args.prefix + base + '.db'
#    db_name = "./output.db"
#
#    #check if database already exists
#    new = False
#    if os.path.isfile(db_name):
#        action = raw_input('Database already exists. Do you want to (r)emove, (a)ppend or (q)uit? ')
#        print('action =', action)
#    else:
#        action = 'c'
#
#    if action == 'r':
#        print('removing database', db_name , '...')
#        os.remove(db_name)
#        new = True
#
#    elif action == 'a':
#        print('appending to database ... ')
#
#    elif action == 'c':
#        print('creating database', db_name, '...')
#        new = True
#
#    else:
#        print('Quit database tool')
#        sys.exit(0)
#
#    # Create indexer which can create the database tables and provides an API to insert data into the tables.
#    indx = db_index.Indexer(db_name)
#    if new == True:
#        indx.create_tables()
# End of inspiration

    video_list = []
    for t in video_types:
        regex = str(args.path) + '/' + t
        video_list.extend(glob.glob(regex))

    for v in video_list:
        f = process_frames(v, extract_sift)
        index_framelist(f, v)
