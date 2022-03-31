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
    feature_list = []
    cur_frame = 0
    while vid.isOpened():
        ret, frame = vid.read()
        cur_frame += 1

        if not ret:
            break
        if cur_frame + skip_frames >= frame_count:
            break
        if cur_frame % skip_frames != 0:
            continue


        print("Frame: " + str(cur_frame) + " / " + str(frame_count), end="\r")

        frame_list.append( (frame, (filename + '.' + str(cur_frame)) ))
        #frame_list.append( (cur_frame, process_func(frame)) )
        #print(frame_list)


    print("Extracting...")
    result = process_func(frame_list)
    print()
    return result

sift = cv2.SIFT_create()
def extract_sift(frame_list):

    features = {}
    
    i = 0
    total = len(frame_list)
    errors = 0
    for f in frame_list:
        im = f[0]
        name = f[1].split('/')[-1]

        print("Processing: " + str(i) + " / " + str(total), end="\r")
        i += 1

        # note!!
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        kp, desc = sift.detectAndCompute(gray, None)

        if (type(desc) is not np.ndarray):
            print("[Warning]" + name +", " + str(i) + "could not extract SIFT")
            errors += 1
            continue
        features[name] = desc

    print()
    print("Done")
    if (errors != 0):
        print("Number of failed extraction: " + str(errors))

    return features

def index_framelist(frame_list, filename):
    print("TODO: Insert into DB", filename)


video_types = ('*.mp4', '*.MP4', '*.avi') #webm?
if __name__ == "__main__":
    args = parser.parse_args()
    path = args.path.resolve()

# "Inspired" by dbt.py
    #db_name = args.prefix + base + '.db'
    db_name = "./output.db"

    #check if database already exists
    new = False
    if os.path.isfile(db_name):
        action = input('Database already exists. Do you want to (r)emove, (a)ppend or (q)uit? ')
        print('action =', action)
    else:
        action = 'c'

    if action == 'r':
        print('removing database', db_name , '...')
        os.remove(db_name)
        new = True

    elif action == 'a':
        print('appending to database ... ')

    elif action == 'c':
        print('creating database', db_name, '...')
        new = True

    else:
        print('Quit database tool')
        quit()

    # Create indexer which can create the database tables and provides an API to insert data into the tables.
    indx = db_index.Indexer(db_name)
    if new == True:
        indx.create_tables()
# End of inspiration

    video_list = []
    for t in video_types:
        regex = str(args.path) + '/' + t
        video_list.extend(glob.glob(regex))

    sift_features = {}
    for v in video_list:
        f = process_frames(v, extract_sift, 5)
        sift_features = sift_features | f
        #index_framelist(f, v)


    name_list = list(sift_features.keys())

    fname = './_sift_vocabulary.pkl'
    if os.path.isfile(fname):
        #compute = input("Found existing vocabulary: " + fname + " Do you want to recompute it? ([Y]/N): ")
        print("Found existing vocabulary: " + fname + " It will be recomputed")
        compute = 'Y'
    else:
        compute = 'Y'
    if compute == 'y':
        compute = 'Y'

    if compute == 'Y' or compute == '':
        print('Creating SIFT vocabulary ... ')
        sift_vocabulary = Vocabulary.Vocabulary(db_name)
        sift_vocabulary.train(sift_features)
        fname = './_sift_vocabulary.pkl'
        with open(fname, 'wb') as f:
            pickle.dump(sift_vocabulary, f)

    for i in name_list:
        indx.add_to_index('sift', i, sift_features[i], sift_vocabulary)

    print("Done")
