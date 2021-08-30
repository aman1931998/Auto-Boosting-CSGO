import sys
import subprocess
import pickle
import shutil
import pyautogui as pg
import keyboard as kb
import time
import os
import psutil
import pyperclip as pc


from positions import CSGO_UPPER_POS_X, CSGO_LOWER_POS_X, CSGO_UPPER_POS_Y, CSGO_LOWER_POS_Y
def get_top_left_position_from_panel_name(panel_name = "u1"): # Get the top left coordinates of the panel using panel names
    batch = panel_name[0]
    number = int(panel_name[1]) - 1
    if batch == 'u':
        return CSGO_UPPER_POS_X[number], CSGO_UPPER_POS_Y[number]
    elif batch == 'l':
        return CSGO_LOWER_POS_X[number], CSGO_LOWER_POS_Y[number]