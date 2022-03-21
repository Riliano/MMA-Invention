#!/bin/env python
import os
import argparse
import pathlib

import cv2
import numpy as np

import Localization

parser = argparse.ArgumentParser(description='Cretes the database for the videos.')

parser.add_argument('path', type=pathlib.Path, help='The path to videos.')
parser.add_argument('--output', type=pathlib.Path, help='Specify the output file for the database.')

def main():
    args = parser.parse_args()
    path = args.path.resolve()

    print("Path to videos: " + path.name)
    print("TODO")


if __name__ == "__main__":
    main()
