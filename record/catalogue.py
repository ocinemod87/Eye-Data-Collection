import os
import numpy as np
from PIL import Image
import cv2 as cv

class Catalogue:

    def __init__(self, folder_name):
        self.folder_name = folder_name
        self.create_person_folder
        self.create_person_shootings_folder
        self.create_person_targets_folder
        self.person_images_counter = 0
        self.take = 0
        self.shot = 0
        self.target = 0

    @property
    def create_person_folder(self):
        self.person_path = os.getcwd()+'/Data/'+self.folder_name
        print(self.person_path)

        try:
            os.mkdir(self.person_path)
        except OSError:
            print ("Creation of the directory %s failed" % self.person_path)
        else:
            print ("Successfully created the directory %s " % self.person_path)

    @property
    def create_person_shootings_folder(self):
        print('here')
        self.person_shootings_path = self.person_path+'/shooting'

        try:
            os.mkdir(self.person_shootings_path)
        except OSError:
            print ("Creation of the directory %s failed" % self.person_shootings_path)
        else:
            print ("Successfully created the directory %s " % self.person_shootings_path)

    @property
    def create_person_targets_folder(self):
        self.person_targets_path = self.person_path+'/targets'

        try:
            os.mkdir(self.person_targets_path)
        except OSError:
            print ("Creation of the directory %s failed" % self.person_targets_path)
        else:
            print ("Successfully created the directory %s " % self.person_targets_path)

    @property
    def create_shooting_take_folder(self):
        self.shooting_take_path = self.person_shootings_path+'/take'+str(self.take)

        try:
            os.mkdir(self.shooting_take_path)
        except OSError:
            print ("Creation of the directory %s failed" % self.shooting_take_path)
        else:
            print ("Successfully created the directory %s " % self.shooting_take_path)

    @property
    def create_target_take_folder(self):
        self.target_take_path = self.person_targets_path+'/take'+str(self.take)

        try:
            os.mkdir(self.target_take_path)
        except OSError:
            print ("Creation of the directory %s failed" % self.target_take_path)
        else:
            print ("Successfully created the directory %s " % self.target_take_path)

    def new_take(self):
        self.create_shooting_take_folder
        self.create_target_take_folder
        self.take +=1
        self.shot = 0

    def add_image_person(self, image_person):
        cv.imwrite(self.shooting_take_path+"/person"+str(self.shot)+".png", image_person)
        #self.image_person = Image.fromarray(image_person)
        #self.image_person.save(self.shooting_take_path+"/person"+str(self.shot)+".png")
        self.shot += 1


    def add_image_target(self, image_target):
        cv.imwrite(self.target_take_path+"/person"+str(self.shot)+".png", image_target)
        #self.image_target = Image.fromarray(image_target)
        #self.image_target.save(self.target_take_path+"/person"+str(self.shot)+".png")

if __name__ == '__main__':
    cat = Catalogue("dom")
    cat.new_take()
    cat.new_take()
