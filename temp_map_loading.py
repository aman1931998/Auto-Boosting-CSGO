# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 14:02:49 2021

@author: Aman Agarwal
"""


import os
import numpy as np
import cv2
from PIL import Image, ImageGrab
from project_path import steam_path
map_name = 'nuke'

pos_x, pos_y = 0, 54
map_loading_check_x_1, map_loading_check_y_1 = 84, 93
map_loading_check_x_2, map_loading_check_y_2 = 120, 127

path = os.path.join('validation_data', 'map_loading', map_name + "_map_loading.npy")

image = ImageGrab.grab().convert('RGB')


op_img = image.crop([pos_x + map_loading_check_x_1, 
                     pos_y + map_loading_check_y_1, 
                     pos_x + map_loading_check_x_2, 
                     pos_y + map_loading_check_y_2])
op_img.save(os.path.join('validation_data', 'map_loading', map_name + "_map_loading.png"))
np.save(path, np.array(op_img))


assert np.all(np.array(op_img) == np.array(ImageGrab.grab().crop([pos_x + map_loading_check_x_1, pos_y + map_loading_check_y_1,  pos_x + map_loading_check_x_2,  pos_y + map_loading_check_y_2]).convert('RGB')))

