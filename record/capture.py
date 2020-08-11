from typing import *

from simpleuvc.camera import Camera
import numpy as np
import cv2 as cv
import uvc

from catalogue import Catalogue

def init_cameras(scene_id: int, eye_id: int, scene_exposure: int, eye_exposure: int) -> Tuple[Camera, Camera]:
    devices = uvc.device_list()

    scene_cam = Camera(devices[scene_id]['uid'], mode=(1280, 720, 60))
    eye_cam = Camera(devices[eye_id]['uid'], mode=(1280, 720, 60))

    scene_cam.controls.exposure.value = scene_exposure
    eye_cam.controls.exposure.value = eye_exposure

    # Load first frame (ensure initialised and prints info from uvc)
    scene_cam.get_frame()
    eye_cam.get_frame()

    return scene_cam, eye_cam


def run_capture(scene_cam: Camera, eye_cam: Camera, repetitions: int, rep_delay: int) -> None:
    cv.namedWindow('Capture Tester')
    point_number = 0

    folder_name = input('Folder name: ')
    cat = Catalogue(folder_name)
    cat.new_take()

    print('Ready (point 0)')
    while True:
        frame = scene_cam.get_frame()
        eyes = eye_cam.get_frame()

        eyes_display = cv.resize(eyes.bgr, (640, 360))
        frame_display = cv.resize(frame.bgr, (640, 360))

        cv.imshow('Capture Tester', np.hstack((eyes_display, frame_display)))

        key = cv.waitKey(-1) & 0xFF

        if not frame or key == ord('q'):
            break
        elif key == ord(' '):
            # Capture images
            print('Capturing...', end='')
            for i in range(repetitions):
                frame = scene_cam.get_frame()
                eyes = eye_cam.get_frame()
                
                cat.add_image_target(frame.bgr)
                cat.add_image_person(eyes.bgr)
                
                # Call save capture function
                cv.waitKey(rep_delay)

            print('Done')
        elif key == ord('n'):
            cat.new_take()
            point_number += 1
            print(f'Point no. {point_number}')



    scene_cam.close()
    eye_cam.close()
    cv.destroyAllWindows()
    cv.waitKey(1)
