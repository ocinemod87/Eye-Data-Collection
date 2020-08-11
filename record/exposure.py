import uvc
import cv2 as cv
import numpy as np
from simpleuvc.camera import *
import serial
import json
import glob

devices = uvc.device_list()
print(devices)

#rduino = serial.Serial('/dev/cu.usbmodem1A1221', 115200)

scene_cam = Camera(devices[0]['uid'], mode=(1280, 720, 60))
scene_cam.controls.auto_exposure_mode.value = AUTO_EXPOSURE_MODE_MANUAL
scene_cam.list_available_modes()

eye_cam = Camera(devices[1]['uid'], mode=(1280, 720, 60))
eye_cam.controls.auto_exposure_mode.value = AUTO_EXPOSURE_MODE_MANUAL
eye_cam.list_available_modes()


def update_exposure(camera, value):
    camera.controls.exposure.value = value


cv.namedWindow('Capture Tester')
cv.createTrackbar('Scene', 'Capture Tester', 100, 500, lambda val: update_exposure(scene_cam, val))
cv.createTrackbar('Eyes', 'Capture Tester', 100, 500, lambda val: update_exposure(eye_cam, val))

data_list = []
last_light = 0

while True:
    frame_scene = scene_cam.get_frame()
    frame_eyes = eye_cam.get_frame()
    #data = arduino.readline()
    #if data:
    #    last_light = int(data.decode('utf-8'))
    #    #print(data.decode('utf-8'))


    key = cv.waitKey(1) & 0xFF

    if not frame_scene or not frame_eyes or key == ord('q'):
        break
    elif key == ord('a'):
        print('saved')
        entry = {
            'scene': scene_cam.controls.exposure.value,
            'eyes': eye_cam.controls.exposure.value,
            'light_reading': last_light
        }
        data_list.append(entry)

    frame_scene = cv.resize(frame_scene.bgr, (640, 360))
    frame_eyes = cv.resize(frame_eyes.bgr, (640, 360))

    cv.imshow('Capture Tester', np.hstack((frame_scene, frame_eyes)))

num = len(glob.glob('data/' + '[0-9]'*3 + '.json'))
f = open('data/{:03d}.json'.format(num), "w")
f.write(json.dumps(data_list))
f.close()

scene_cam.close()
cv.destroyAllWindows()
cv.waitKey(1)
