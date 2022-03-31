import numpy as np
import cv2

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

        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        kp, desc = sift.detectAndCompute(gray, None)

        if (type(desc) is not np.ndarray):
            print("[Warning] " + name +", " + str(i) + " could not extract SIFT")
            errors += 1
            continue

        features[name] = desc

    print()
    print("Done")
    if (errors != 0):
        print("Number of failed extraction: " + str(errors))

    return features
