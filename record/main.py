import uvc
import cv2 as cv
from simpleuvc.camera import Camera
import glob
import numpy as np
import os
from capture import run_capture, init_cameras

import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('config', help='Path to config file')
args = parser.parse_args()

with open(args.config) as file:
    data = json.load(file)

    scene_cam, eye_cam = init_cameras(0, 1, data['exposure']['scene'], data['exposure']['eye'])

    run_capture(scene_cam, eye_cam, data['repetitions'], data['rep_delay'])
