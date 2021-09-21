import time
import beepy 
import shutil, os
import pyautogui as pg
import keyboard as kb
from time import sleep
import numpy as np
from PIL import Image, ImageGrab, ImageOps
import pickle, cv2
import psutil
import pyperclip as pc
from positions import *
from functions import *
from major_functions import *
from driver_file_functions import *
import pandas as pd

#%%
update_accounts = True







while True:
#%% match repetition
    if update_accounts:
        os.system("ipconfig /release"); time.sleep(0.3)
        os.system("ipconfig /flushdns"); time.sleep(0.3)
        os.system("ipconfig /renew"); time.sleep(0.3)
        #TODO
        update_active_accounts()
        # Do full workup














    #%% Config
    clear_old_instance = False
    launch_timeout = 35
    after_launch_timeout = 180
    untrusted = True
    
    map_name = "anubis"
    match_output = 'winlose'   #"winlose" #"tie"
    winner = get_winner_lobby()#"upper"
    #print("Winner for next match: %s"%(winner))
    
    winner_score = [16, 0] #[15, 15] #[15, 15]  #[16, 14] #
    current_score = [0, 0]
    
    mode = 'play'
    
    
    if mode == 'play':
        accept_args = "--clear_old_instance %s --after_launch_timeout %d --untrusted %s --map_name %s --match_output %s --winner %s --winner_score %d %d --current_score %d %d"%(str(clear_old_instance), \
                        after_launch_timeout, \
                        str(untrusted), \
                        map_name, \
                        match_output, \
                        winner, \
                        winner_score[0], \
                        winner_score[1], \
                        current_score[0], \
                        current_score[1])
            
        save_accept_args(accept_args)
        
        
        runfile('main_file.py', accept_args)
    elif mode == 'vac_check':
        accept_args = "--clear_old_instance %s --after_launch_timeout %d --untrusted %s --map_name %s --match_output %s --winner %s --winner_score %d %d --current_score %d %d"%(str(clear_old_instance), \
                        after_launch_timeout, \
                        str(untrusted), \
                        map_name, \
                        match_output, \
                        winner, \
                        winner_score[0], \
                        winner_score[1], \
                        current_score[0], \
                        current_score[1])
        
        runfile('vac_error_checker.py', accept_args)


