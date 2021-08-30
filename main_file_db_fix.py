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
import argparse
import sys

from project_path import steam_path
from dynamic_data_functions import load_old_account_database, load_current_mm_batch, load_mm_batches_index, load_winner_index
from loading_functions import load_account_database
#%% Parsing arguments for running main script.
parser = argparse.ArgumentParser()
parser.add_argument("--clear_old_instance", type = str, help = "Clear old instances", default = 1)
parser.add_argument("--after_launch_timeout", type = int, help = "Time to wait after launching panel(s)", default = 100)
parser.add_argument("--launch_timeout", type = float, help = "Time to wait after launching 1 panel", default = 1)
parser.add_argument("--untrusted", type = bool, help = "Launch in untrusted mode", default = False)
parser.add_argument("--map_name", type = str, help = "Select the map name", default = "anubis")
parser.add_argument("--match_output", type = str, help = "Match outcome", default = "winlose")
parser.add_argument("--winner", type = str, help = "Winner batch", default = "upper")
parser.add_argument("--winner_score", type = str, nargs = 2, help = "Set the score for the match w.r.t. winning lobby", default = "16 3")
parser.add_argument("--current_score", type = str, nargs = 2, help = "Current Score", default = "0 0")
# parser.add_argument("--max_matches", type = int, help = "Number pf matches to play.", default = 4)
args = parser.parse_args()
print("MAINFILE!!!!")
print("args\n\n", args)

from config_variables import power_supply_check

#%% Config settings
clear_old_instance = bool(int(args.clear_old_instance))                             # Whether to clear old instances.
launch_timeout = float(args.launch_timeout)                                    # Timeout after launching a panel
after_launch_timeout = int(args.after_launch_timeout)                          # Timeout after launching all panels
untrusted = False #bool(args.untrusted)                                               # Launch in Trusted mode or not.
map_name = str(args.map_name).lower()                                          # Name of the map to play
match_output = str(args.match_output).lower()                                  # Output of the match. Eg: 16 14 or 16 0 or 15 15
winner = str(args.winner).lower()                                              # Winner lobby [upper or lower]
print(clear_old_instance, launch_timeout, after_launch_timeout, untrusted, map_name, match_output, winner)
try: winner_score = list(map(int, str(args.winner_score).split()))
except: winner_score = list(map(int, args.winner_score))
try: current_score = list(map(int, str(args.current_score).split()))
except: current_score = list(map(int, args.current_score))

if power_supply_check:
    power_connection_check()

#%% Config [Default]
# clear_old_instance = True #False in match 2
# after_launch_timeout = 100
# launch_timeout = 1
# untrusted = False
# map_name = "anubis"
# match_output = 'winlose'
# winner = 'upper' # or 'u'
# current_map = 'anubis'
# winner_score = [16, 3] #[15, 15] #or [16, 0]
# current_score = [0, 0] # or [4, 2]

#%% Paths [Default]
from project_path import friend_code_dict_path


account_data = load_account_database()
print("Loading account database for main file.")
mm_batch = load_current_mm_batch()
print("Loading current MM Batch for main file.")
winner_index = int(load_winner_index())
mm_batch['winner'] = mm_batch['winner'][winner_index]
print("Loading winner_index to get winner for this batch. : %s"%(mm_batch['winner']))

t1_initial_time = time.time()
all_panels = ['u1', 'u2', 'u3', 'u4', 'u5', 'l1', 'l2', 'l3', 'l4', 'l5']
print("Getting acccount details")                                              # Getting 10 SteamIDs, Usernames, Passwords for this batch.
USERNAME_UPPER, PASSWORD_UPPER, STEAM_ID_UPPER, USERNAME_LOWER, PASSWORD_LOWER, STEAM_ID_LOWER = get_accounts()
# print("Clearing earlier instances and panels.")


def launch_panels(PIDs, panels_to_launch, launch_timeout):
    for panel in panels_to_launch:
        panel_top_left_x, panel_top_left_y, (username, password, steamid) = get_top_left_position_from_panel_name(panel, include_account_details = True)
        PIDs = get_panel_pids(username, password, steamid, panel, PIDs, launch_timeout = launch_timeout, trusted_mode = not untrusted, map_name = map_name)
    return PIDs

def get_panels_ready(temp_panels_launched):
    panels_ready = []
    for panel in temp_panels_launched: #panel = 'l1'
        pos_x, pos_y = get_top_left_position_from_panel_name(panel, include_account_details = False)
        # index = CSGO_UPPER_POS_X.index(pos_x)
        # click_only(CSGO_TITLE_BAR_X[index] + pos_x, CSGO_TITLE_BAR_Y[index] + pos_y, 0.2, 2)
        if check_launched_panel(POS_X = pos_x, POS_Y = pos_y):
            vac_signature_error_op = ready_panel(pos_x, pos_y, untrusted_check = untrusted, untrusted_check_times = 1, panel_number = panel, do = True)
            if not vac_signature_error_op:
                panels_ready.append(panel)
    return panels_ready

if not clear_old_instance:
    print("Verifying whether old instance if available or not.")
    try:
        PIDs = load_PIDs()
        for key in PIDs.keys(): #key = list(PIDs.keys())[0]
            if type(PIDs[key]) == list:
                clear_old_instance = True
    except:
        clear_old_instance = True

if not clear_old_instance:
    print("Continuing with old batch")
    PIDs = load_PIDs()   #TODO Check if we can remove this fn to avoid r/w calls.
    print("PIDs loaded: \n")
    print(PIDs)
    for i in range(5):
        cd_ch = cd_check_wrapper(POS_X = CSGO_UPPER_POS_X[i], POS_Y = CSGO_UPPER_POS_Y[i], consider_blue = False)
        if cd_ch in ['Green', 'Yellow']: # 'Blue',
            print("CD")
            sys.exit(0)
        cd_ch = cd_check_wrapper(POS_X = CSGO_LOWER_POS_X[i], POS_Y = CSGO_LOWER_POS_Y[i], consider_blue = False)
        if cd_ch in ['Green', 'Yellow']: # 'Blue',
            print("CD")
            sys.exit(0)
    # Check what else is neeeded for continuingg.
else:
    reset_leader_index()
    print("Cleaning old batch panels")
    cleaner()
    cleaner()
    print("Running panels.")
    all_panels = ['u1', 'u2', 'u3', 'u4', 'u5', 'l1', 'l2', 'l3', 'l4', 'l5']
    PIDs = {"u1": [], "u2": [], "u3": [], "u4": [], "u5": [], "l1": [], "l2": [], "l3": [], "l4": [], "l5": [] }
    
    total_attempts = 7
    print("Total Attempts: %d"%(total_attempts))
    panels_not_launched = all_panels.copy()
    print("Panels not launched: ", *panels_not_launched)
    panels_launched = []
    print("Panels launched: ", *panels_launched)
    panels_ready = []
    print("Panels ready: ", *panels_ready)
    total_time_available = after_launch_timeout
    
    attempt = 1
    while attempt <= total_attempts:
        if power_supply_check:
            power_connection_check()
        print("Attempt #%d"%(attempt))
        if attempt != 1:
            PIDs = kill_PIDs(PIDs, panels_not_launched)
        PIDs = launch_panels(PIDs, panels_not_launched, launch_timeout)
        print(PIDs)
        save_PIDs(PIDs)
        total_time_used = 0
        while len(panels_ready) != 10:
            if power_supply_check:
                power_connection_check()
            if total_time_used >= total_time_available:
                break
            t1 = time.time()
            temp_panels_launched = set(check_launched_panel_wrapper(checker_image = None, panels_to_check = panels_not_launched))
            print("[Temp] Panels Launched: ", *temp_panels_launched)
            time.sleep(10)
            temp_panels_ready = get_panels_ready(list(temp_panels_launched))
            print("[Temp] Panels Ready: ", temp_panels_ready)
            
            panels_ready += temp_panels_ready
            print("Attempt $%d: Panels Ready: "%(attempt), *panels_ready)
            panels_not_launched = [panel for panel in list(all_panels) if panel not in panels_ready]
            print("Attempt $%d: Panels Not Launched: "%(attempt), *panels_not_launched)
            
            t2 = time.time()
            total_time_used += (t2-t1)
        attempt += 1

    # identify_and_clear_errors(all_panels = True, error_coordinates = error_coordinates, error_with_numpy_images = error_with_numpy_images, 
    #                           error_ok_button = error_ok_button)

#%%
print("Additional check for panels")
panels_not_ready_after_ready_part = set(check_launched_panel_wrapper(checker_image = None, panels_to_check = all_panels))
if len(panels_not_ready_after_ready_part) > 0:
    get_panels_ready(panels_not_ready_after_ready_part)

time.sleep(1)

from capture_functions import get_mm_rank_snippet
def get_mm_snippets2():
    if not os.path.isdir(os.path.join('mm_snippets_username_oriented')):
        os.mkdir(os.path.join('mm_snippets_username_oriented'))
    for i in range(5):
        image_upper = get_mm_rank_snippet(CSGO_UPPER_POS_X[i], CSGO_UPPER_POS_Y[i], return_numpy_object=False)
        image_lower = get_mm_rank_snippet(CSGO_LOWER_POS_X[i], CSGO_LOWER_POS_Y[i], return_numpy_object=False)
        image_upper.save(os.path.join('mm_snippets_username_oriented', USERNAME_UPPER[i] + ".png"))
        image_lower.save(os.path.join('mm_snippets_username_oriented', USERNAME_LOWER[i] + ".png"))
        print("Snippets Saved")


get_mm_snippets2()
