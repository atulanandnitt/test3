# import numpy as np
# import face_recognition
# from flask import Flask, jsonify, request, redirect
# import PIL.Image

import os

dirpath = os.getcwd()
print("current directory is : " + dirpath)
foldername = os.path.basename(dirpath)
training_folder = dirpath + "/pictures"
for item1,item2,item3 in os.walk(training_folder):
    print("item1",item1)
    print("item 2:",item2)
    print("item3", item3)
print("Directory name is : " + foldername)

#
# def load_image_file(file, mode='RGB'):
#     """
#     Loads an image file (.jpg, .png, etc) into a numpy array
#
#     :param file: image file name or file object to load
#     :param mode: format to convert the image to. Only 'RGB' (8-bit RGB, 3 channels) and 'L' (black and white) are supported.
#     :return: image contents as numpy array
#     """
#     im = PIL.Image.open(file)
#     if mode:
#         im = im.convert(mode)
#     return np.array(im)
#
#
# print(load_image_file("pictures/atul.JPG"))
