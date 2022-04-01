#!/bin/env python
import os
import argparse
import pathlib
import pickle

import cv2
import numpy as np

import Localization
import image_search
import ExtractorSIFT

parser = argparse.ArgumentParser(description='Query tool for the video database created by <TODO>. Returns a filename for the best match.')

parser.add_argument('query', type=pathlib.Path, help='The path to the query video.')
db_name = "output.db"

search = image_search.Searcher(db_name)
with open("_sift_vocabulary.pkl", 'rb') as f:
    sift_vocabulary = pickle.load(f)

def processVideo(video, sample_frequency=1):
    frame_number = 0
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    frames_per_sample = fps // sample_frequency

    query_frames = []
    while video.isOpened() and frame_number < frame_count:
        ret, frame = video.read()
        if frame_number % frames_per_sample == 0:
            localized_frame = Localization.screen_detection(frame, display_steps=False)
            query_frames.append( (localized_frame, "query" + str(frame_number)) )

        frame_number += 1

    sift_features = ExtractorSIFT.extract_sift(query_frames)
    for f in sift_features:
        sift_query = sift_features[f]
        image_words = sift_vocabulary.project(sift_query)
        sift_candidates = search.query_iw('sift', image_words)
        print("RESULTS: ", len(sift_candidates))

        N = 10
        sift_winners = [search.get_filename(cand[1]) for cand in sift_candidates][0:N]
        sift_distances = [cand[0] for cand in sift_candidates][0:N]
        for i in range(N):
            print(sift_winners[i], sift_distances[i])
        #plot_results(sift_winners, 'SIFT Results', sift_distances)
    result = "TODO"#majority_voting(sift_winners), 
    return result

if __name__ == "__main__":
    args = parser.parse_args()
    path = args.query.resolve()

    video = cv2.VideoCapture(str(path.resolve()))

    if (video.isOpened()== False):
        print("Error opening video stream or file. Does the path exist?")

    print('Results for: ' + path.name)
    processVideo(video)
