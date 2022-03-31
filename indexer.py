#!/bin/env python
import os
import argparse
import pathlib
import glob

import cv2
import numpy as np

import sqlite3 as sqlite
import pickle
import db_index

import Vocabulary
import ExtractorSIFT

parser = argparse.ArgumentParser(description='Creates the database for the videos. Outputs to files \'output.db\' and \'_sift_vocabulary.pkl\'.')
parser.add_argument('path', type=pathlib.Path, help='The path to video library.')

def process_frames(filename, process_func, skip_frames = 1):
    print("Processing: " + filename)
    vid = cv2.VideoCapture(filename)
    if not vid.isOpened():
        print("Error opening video: " + filename)

    frame_count = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(vid.get(cv2.CAP_PROP_FPS))

    frame_list = []
    feature_list = []
    cur_frame = 0
    while vid.isOpened():
        ret, frame = vid.read()
        cur_frame += 1

        if (not ret) or (cur_frame + skip_frames >= frame_count):
            break
        if cur_frame % skip_frames != 0:
            continue

        print("Frame: " + str(cur_frame) + " / " + str(frame_count), end="\r")

        frame_list.append( (frame, (filename + '.' + str(cur_frame)) ))
    print()

    print("Extracting...")
    result = process_func(frame_list)
    return result

def check_if_should_create_db(db_name):
    if os.path.isfile(db_name):
        action = input('Database already exists. Do you want to (r)emove, (a)ppend or (q)uit? ')
        print('action =', action)
    else:
        action = 'c'

    if action == 'r':
        print('removing database', db_name , '...')
        os.remove(db_name)
        return True

    elif action == 'a':
        print('appending to database ... ')
        return False

    elif action == 'c':
        print('creating database', db_name, '...')
        return True

    else:
        print('Quit database tool')
        quit()

    return False

video_types = ('*.mp4', '*.MP4', '*.avi')
if __name__ == "__main__":
    args = parser.parse_args()
    path = args.path.resolve()

# "Inspired" by dbt.py
    #db_name = args.prefix + base + '.db'
    db_name = "./output.db"

    # Create indexer which can create the database tables and provides an API to insert data into the tables.
    create_db = check_if_should_create_db(db_name)
    indx = db_index.Indexer(db_name)
    if create_db:
        indx.create_tables()
# End of inspiration

    video_list = []
    for t in video_types:
        regex = str(args.path) + '/' + t
        video_list.extend(glob.glob(regex))

    frame_skip = 15
    sift_features = {}
    i = 0
    t = len(video_list)
    for v in video_list:
        print("Working " + str(i) + "/" + str(t))
        i += 1
        f = process_frames(v, ExtractorSIFT.extract_sift, frame_skip)
        sift_features = sift_features | f

    name_list = list(sift_features.keys())

    fname = './_sift_vocabulary.pkl'
    if os.path.isfile(fname):
        print("Found existing vocabulary: " + fname + " It will be recomputed!")

    print('Creating SIFT vocabulary ... ')
    sift_vocabulary = Vocabulary.Vocabulary(db_name)
    sift_vocabulary.train(sift_features)
    fname = './_sift_vocabulary.pkl'
    with open(fname, 'wb') as f:
        pickle.dump(sift_vocabulary, f)

    for i in name_list:
        indx.add_to_index('sift', i, sift_features[i], sift_vocabulary)

    print("Done")
