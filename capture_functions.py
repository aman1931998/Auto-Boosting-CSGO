import os
import cv2
from PIL import Image, ImageGrab
import numpy as np


def get_pr_rank_snippet(panel_top_left_x, panel_top_left_y, return_numpy_object = True):
    '''
    Returns the PR Rank Snippet of the panel.
    panel_top_left_x: Panel's top left coordinate X
    panel_top_left_y: Panel's top left coordinate Y
    return_numpy_object: Return in numpy or not.
    '''
    pr_rank_x_1, pr_rank_y_1 = 608, 70
    pr_rank_x_2, pr_rank_y_2 = 634, 94
    
    image = ImageGrab.grab([panel_top_left_x + pr_rank_x_1, 
                            panel_top_left_y + pr_rank_y_1, 
                            panel_top_left_x + pr_rank_x_2, 
                            panel_top_left_y + pr_rank_y_2]).convert('RGB')
    if return_numpy_object:
        return np.array(image)
    return image

def get_mm_rank_snippet(panel_top_left_x, panel_top_left_y, return_numpy_object = True):
    '''
    Returns the MM Rank Snippet of the panel.
    panel_top_left_x: Panel's top left coordinate X
    panel_top_left_y: Panel's top left coordinate Y
    return_numpy_object: Return in numpy or not.
    '''
    mm_rank_x_1, mm_rank_y_1 = 605, 102
    mm_rank_x_2, mm_rank_y_2 = 639, 114

    image = ImageGrab.grab([panel_top_left_x + mm_rank_x_1, 
                            panel_top_left_y + mm_rank_y_1, 
                            panel_top_left_x + mm_rank_x_2, 
                            panel_top_left_y + mm_rank_y_2]).convert('RGB')
    if return_numpy_object:
        return np.array(image)
    return image

