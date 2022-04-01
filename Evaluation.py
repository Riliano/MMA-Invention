#!/bin/env python
import os
import argparse
import pathlib

import cv2
import numpy as np

import Localization
import query

parser = argparse.ArgumentParser(description='Evaluates the query tool.')

parser.add_argument('query', type=pathlib.Path, help='The path to the test folder.')


def getFiles(path):
    files = os.listdir(path)
    files.sort()
    print("File list: " + str(files))
    groundTruth = None
    testVideos = []
    for f in files:
        if f.endswith(".txt"):
            if groundTruth is None:
                groundTruth = f
            else:
                raise ValueError("You have more than one txt files in the test folder")
        else:
            testVideos.append(f)

    with open(str(path) + "/" + groundTruth, 'r') as f:
        truth = [line.strip('\n') for line in f]

    if len(truth) != len(testVideos):
        raise ValueError("You dont have the correct number of truth values (" + str(len(truth)) + ") for the amount of videos (" + str(len(testVideos)) + ")")

    return testVideos, truth


def evaluate(path):
    videos, truth = getFiles(path)
    score = 0
    for i in range(len(videos)):
        v = cv2.VideoCapture(str(path) + "/" + videos[i])
        t = truth[i]

        result = query.processVideo(v, 0.15)
        print("Result is: " + result + " ground truth: " + t)
        if result == t:
            score += 1

    score /= len(videos)

    print("The system got a score of: " + str(score))


if __name__ == "__main__":
    args = parser.parse_args()
    evaluate(args.query.resolve().resolve())
