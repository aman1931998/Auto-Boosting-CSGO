# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 21:46:25 2021

@author: aman1
"""
import sys, pickle
import shutil
import os
import cv2
from PIL import Image, ImageGrab
import numpy as np
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
# def backup_rank_database(base_path):
#     backup_path = os.path.join('images', 'backup_folder')
#     try:
#         assert len(os.listdir(backup_path)) == 0
#     except:
#         backup_path_override_input = input("Backup folder is not empty. Overwrite?: ")
#         if backup_path_override_input.lower() in ['yes', '1']:
#             shutil.rmtree(backup_path)
#         else:
#             sys.exit(0)
#     try:
#         if not os.path.isdir(backup_path):
#             os.mkdir(backup_path)
#         shutil.copytree(base_path, backup_path)
#         return True
#     except:
#         return False

def backup_rank_database(base_path):
    backup_path = os.path.join('images', 'backup_folder')
    if os.path.isdir(backup_path):
        backup_path_override_input = input("Backup folder is not empty. Overwrite?: ")
        if backup_path_override_input.lower() in ['yes', '1']:
            shutil.rmtree(backup_path)
        else:
            sys.exit(0)
    try:
        shutil.copytree(base_path, backup_path)
        return True
    except:
        return False



def get_rank_count(base_path, new_rank):
    l = os.listdir(base_path)
    try: l.remove('numpy_objects')
    except: pass
    l = [i.split(".")[0].split("_")[0] for i in l]
    return l.count(new_rank)



def prettify(elem):
    """
    Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def load_conversion_tables(rank_replace_path = os.path.join('images', 'replace_dict'), order = ['mm', 'pr']):
    assert set(['mm', 'pr']) == set(order)
    mm_conversion_table_path = os.path.join(rank_replace_path, 'mm_conversion_table.pkl')
    pr_conversion_table_path = os.path.join(rank_replace_path, 'pr_conversion_table.pkl')
    with open(mm_conversion_table_path, 'rb') as file:
        mm_conversion_table = pickle.load(file)
    with open(pr_conversion_table_path, 'rb') as file:
        pr_conversion_table = pickle.load(file)
    if order == ['mm', 'pr']:
        return mm_conversion_table, pr_conversion_table
    elif order == ['pr', 'mm']:
        return pr_conversion_table, mm_conversion_table

def load_to_ignore_lists(rank_replace_path = os.path.join('images', 'replace_dict'), order = ['mm', 'pr']):
    assert set(['mm', 'pr']) == set(order)
    mm_to_ignore_path = os.path.join(rank_replace_path, 'mm_to_ignore.pkl')
    pr_to_ignore_path = os.path.join(rank_replace_path, 'pr_to_ignore.pkl')
    with open(mm_to_ignore_path, 'rb') as file:
        mm_to_ignore = pickle.load(file)
    with open(pr_to_ignore_path, 'rb') as file:
        pr_to_ignore = pickle.load(file)
    if order == ['mm', 'pr']:
        return mm_to_ignore, pr_to_ignore
    elif order == ['pr', 'mm']:
        return pr_to_ignore, mm_to_ignore



















