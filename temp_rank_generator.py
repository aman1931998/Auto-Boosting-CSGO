# -*- coding: utf-8 -*-
"""
@author: aman1

Script to identify unique PR and MM ranks.

"""

import os
import cv2
from PIL import Image, ImageGrab
import numpy as np
import shutil
from tqdm import tqdm
from project_path import steam_path

#rank_type = 'mm'
rank_type = 'pr'

base_path = os.path.join(rank_type + '_snippets')
full_image_files = os.listdir(base_path)
try: full_image_files.remove('Thumbs.db')
except: pass

accepted_list = {}

for file_name in tqdm(full_image_files): #file_name = full_image_files[1]
    image = Image.open(os.path.join(base_path, file_name))
    if accepted_list == {}:
        accepted_list[file_name] = 1
        continue
    to_append = True

    for crosscheck_image in accepted_list.keys(): #crosscheck_image = accepted_list[0]
        if np.all(np.array(Image.open(os.path.join(base_path, crosscheck_image))) == np.array(image)):
            accepted_list[crosscheck_image] += 1
            to_append = False
    if to_append:
        accepted_list[file_name] = 1

#%%

rank_list = []
target_path = os.path.join('images', rank_type + '_ranks')

for image in sorted(accepted_list, reverse = True, key = lambda x:accepted_list[x]): #image = accepted_list[0]
    print(accepted_list[image])
    print(*sorted(rank_list))
    image = Image.open(os.path.join(base_path, image)).convert('RGB')
    display(image)
    rank_name = input("Enter the rank name: ")
    if rank_name == "": continue
    rank_list.append(rank_name)
    if rank_name in rank_list:
        get_count = rank_list.count(rank_name)
        rank_name = rank_name + "_" + str(get_count)
    # else:
    #     rank_name = rank_name + "_" + "1"
    image.save(os.path.join(target_path, rank_name + '.png'))
    np.save(os.path.join(target_path, 'numpy_objects', rank_name + '.npy'), np.array(image))

