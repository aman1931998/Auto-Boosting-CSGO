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

#%% Loading functions
from loading_functions import load_mm_rank_database, load_pr_rank_database
mm_rank_database = load_mm_rank_database()
pr_rank_database = load_pr_rank_database()
print("PR and MM Rank database loaded.")

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
        print("dsfdf%d"%(attempt))
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
    
#     if attempt > total_attempts:
#         print("CLEAARNING")
#         sys.exit(0)

#     # identify_and_clear_errors(all_panels = True, error_coordinates = error_coordinates, error_with_numpy_images = error_with_numpy_images, 
#     #                           error_ok_button = error_ok_button)
# print("CHEECKECHECKEC ")
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

#%% Checks whether any one lobby is already created or not.
t2_time_to_launch = time.time()
if power_supply_check:
    power_connection_check()
print("Time taken to launch panels.", t2_time_to_launch - t1_initial_time)
# Case 1: Fresh panels are loaded: both lobbies need to be created
# Case 2: Panels already loaded and last match was 16:0, then 1 lobby is already ready we need second only.
# Case 3: Panels are ready but last match resulted in both lobby disconnects.
# Case N: Try to do this: 
            # When match is over
            # Wait for some time [Formality wait]
            # Disconnect the loosing team immediately and start making new lobby
            # By this time, another lobby should be ready already.

friend_code_dict = load_friend_code_dict_file(friend_code_dict_path)

upper_batch = [CSGO_UPPER_POS_X, CSGO_UPPER_POS_Y, USERNAME_UPPER]
lower_batch = [CSGO_LOWER_POS_X, CSGO_LOWER_POS_Y, USERNAME_LOWER]
print("Upper", upper_batch)
print("Lower", lower_batch)
# get rank snippets
# right_visible_arrangement()
# get_rank_snippets(all_panels = True)

# #%% Cooldown check
# if cd_check_wrapper(all_panels = True):
#     #runfile('new_driver_code.py')
#     runfile('driver_code.py')
#     sys.exit(0)

# Getting panels ready
restart_if_panel_not_responding()
after_lobby_blue_check_wrapper(arrangement_needed = True, checker_image = None, ignore_first_attempt = True)
if power_supply_check:
    power_connection_check()

print("LOBBY CREATED AND AFTER LOBBY CHECK DONE.")

# for batch in [upper_batch, lower_batch]: #batch = upper_batch.copy()
#     POS_X, POS_Y, USERNAME = batch
#     create_lobby(POS_X, POS_Y, USERNAME)

# identify_and_clear_errors(all_panels = True, error_coordinates = error_coordinates, error_with_numpy_images = error_with_numpy_images, 
#                           error_ok_button = error_ok_button)

restart_if_panel_not_responding()
    
t4_lobbies_created = time.time()
print("Lobbies created, time taken: %.2f"%(t4_lobbies_created - t2_time_to_launch))

# identify_and_clear_errors(all_panels = True, error_coordinates = error_coordinates, error_with_numpy_images = error_with_numpy_images, 
#                           error_ok_button = error_ok_button)

time.sleep(1)
restart_if_panel_not_responding()
if power_supply_check:
    power_connection_check()
# right_visible_arrangement(include_play_button = True)
# print("Right Arrangement Done")
start_mm_search(arrangement_needed = False)
print("Starting MM Search")
search_start_time = datetime.now()
print("Search Start Time: ", search_start_time)
#%%
from dynamic_data_functions import reset_match_verification, verify_match_completion, toggle_main_completion
from helper_functions import generate_unique_mismatchID, generate_unique_matchID
mm_mismatchID = generate_unique_mismatchID(include_prefix = True)
print("MismatchID: ", mm_mismatchID)
mismatch_data = {}

search_details = {"search_start_time": None, 
                  "search_error_count": 0, 
                  "search_mismatchID": None, 
                  "search_end_time": None}
search_details['search_start_time'] = search_start_time
search_mismatchID = mm_mismatchID
search_details['search_mismatchID'] = search_mismatchID

if power_supply_check:
    power_connection_check()

# vac_max_count = 5
# vac_count = 0
# print("VAC test count: %d"%(vac_count))
# while True:
#     vac_status = check_green_mm_search_wrapper(arrangement_needed = False, checker_image = None, to_fix = False)
#     if vac_status:
#         if power_supply_check:
#             power_connection_check()
#         print("VAC STATUS: %s"%(vac_status))
#         vac_count+=1
#         stop_mm_search(arrangement_needed = True)
#         click_only(CSGO_UPPER_POS_X[0] + CSGO_PLAY_BUTTON_X, CSGO_UPPER_POS_Y[0] + CSGO_PLAY_BUTTON_Y, 0.2, 4)
#         click_only(CSGO_LOWER_POS_X[0] + CSGO_PLAY_BUTTON_X, CSGO_LOWER_POS_Y[0] + CSGO_PLAY_BUTTON_Y, 0.2, 4)
#         click_only(CSGO_UPPER_POS_X[0] + CSGO_PLAY_BUTTON_X, CSGO_UPPER_POS_Y[0] + CSGO_PLAY_BUTTON_Y, 0.2, 4)
#         click_only(CSGO_LOWER_POS_X[0] + CSGO_PLAY_BUTTON_X, CSGO_LOWER_POS_Y[0] + CSGO_PLAY_BUTTON_Y, 0.2, 4)
#         start_mm_search(arrangement_needed = False)
#         print("Starting MM Search Again after VAC status True trigger.")
#     else:
#         print("VAC Status successful.")
#         break
#     if vac_count == vac_max_count:
#         print("VAC Error: Relaunching panels.")
#         time.sleep(2)
#         # accept__args = get_accept_args()
#         # runfile('main_file.py', accept__args)

# time.sleep(5)

restart_if_panel_not_responding()
#avast_popup(test_image = None, checker_image = avast_popup_checker_image, cancel_match_ = False)
#%%
#%%

from logging_functions import log_current_mismatch_details, log_current_match_details, update_account_data_completed

 #TODO LOOP IT FAILED TO REACH CHECK
while True:
    if power_supply_check:
        power_connection_check()
    panels_with_failed_connection = failed_to_reach_servers_check_wrapper(arrangement_needed = False, checker_image = None, checker_full_image = None)
    
    if panels_with_failed_connection == []:
        print("No Connection Errors.")
        break
    else:
        print("There is a panel with error: 'Failed to reach MM Servers'")
        print("Logging mismatch details with match_found = False")
        log_current_mismatch_details(mm_mismatchID, mm_batch, mismatch_data, match_found = False, total_search_time = 0)
        # print("loading Args for mainfile.")
        # accept__args = get_accept_args()
        # print("Running MAIN again because of Failed conn error.")
        # runfile('main_file.py', accept__args)
        sys.exit(0)

#%%
#%%
if power_supply_check:
    power_connection_check()
terminate_and_matches_played, mismatch_data = auto_accept_check(mismatch_data)

search_details['search_end_time'] = datetime.now()
print("Search End Time.", search_details['search_end_time'])
# If match is not found after a given time.
if terminate_and_matches_played == False:
    print("Match NOT FOUND :(")
    # TODO function to add a set of 
    # TODO!!!!!!!!!!!!!!!!!!!!!!!!
    #TODO add mismatch log function
    print("Logging mismatch details with match_Found = False")
    log_current_mismatch_details(mm_mismatchID, mm_batch, mismatch_data, match_found = False, total_search_time = (datetime.now() - search_start_time).seconds)
    sys.exit(0)
search_details['search_error_count'] = len(mismatch_data.keys())
search_end_time = search_details['search_end_time']
match_found = True

# add log mismatch fn (with match_)fpund = True
# see whether we have to add it here or after connection check.
if power_supply_check:
    power_connection_check()
time.sleep(5)
# TODO UPDATE AND CHANGE
print("Waiting for panels to connect to server.")
reconnection_output = map_loading_check_wrapper(map_name = map_name, method = 'all', max_time = 30)

if type(reconnection_output) != bool:
    log_current_mismatch_details(mm_mismatchID, mm_batch, mismatch_data, match_found = False, total_search_time = (datetime.now() - search_start_time).seconds)
    cancel_match()
    failsafe = True
#log_current_mismatch_details(mm_mismatchID, mm_batch, mismatch_data, match_found = match_found, total_search_time = (search_end_time - search_start_time).seconds)
match_id = generate_unique_matchID(include_prefix = True)
print("MATCH ID: ", match_id)
match_time_details = {}
match_time_details['match_start_time'] = datetime.now()
print("Match Start time.")
print("Waiting for Warmup to end with extra 10 seconds time gap.")
time.sleep(60 + 5 + 15 + 5)
if power_supply_check:
    power_connection_check()
reset_match_verification()
print("Resetting Main File verification toggle.")

accept_args = "--map_name %s --match_output %s --winner %s --winner_score %d %d --current_score %d %d"%(map_name, match_output, winner, winner_score[0], winner_score[1], current_score[0], current_score[1])
print("Running Ingame script.")
runfile('ingame_script.py', args = accept_args)
after_match_cleanup(0)

match_end_time = datetime.now()
print("Match End Time:", match_end_time)

cooldown_details = {"team1": [], "team2": []}
for i in range(4, -1, -1):
    cd_op = cd_check_wrapper(POS_X = CSGO_UPPER_POS_X[i], POS_Y = CSGO_UPPER_POS_Y[i], consider_blue = True)
    print("u" + str(i+1), cd_op)
    if cd_op != None:
        cd_time = match_end_time
    else:
        cd_time = None
    cd_data = {"type": cd_op, "time": match_end_time}
    cooldown_details['team1'].insert(0, cd_data)

    cd_op = cd_check_wrapper(POS_X = CSGO_LOWER_POS_X[i], POS_Y = CSGO_LOWER_POS_Y[i], consider_blue = True)
    print("l" + str(i+1), cd_op)
    if cd_op != None:
        cd_time = match_end_time
    else:
        cd_time = None
    cd_data = {"type": cd_op, "time": match_end_time}
    cooldown_details['team2'].insert(0, cd_data)


# TODO
print("Verifying INGAME COMPLETION")
status = verify_match_completion()
if not status:
    print("Logging Mismatch details due to some ingame script error. [False].")
    log_current_mismatch_details(mm_mismatchID, mm_batch, mismatch_data, match_found = False, total_search_time = (datetime.now() - search_start_time).seconds)
    sys.exit(0)
print("[True] Logging Mismatch details")
log_current_mismatch_details(mm_mismatchID, mm_batch, mismatch_data, match_found = match_found, total_search_time = (search_end_time - search_start_time).seconds)
match_time_details['match_end_time'] = match_end_time 

xp_gained_details = {"team1_xp_gained": [], "team2_xp_gained": []}

from loading_functions import get_xp_gained_for_next_week_of_accounts, get_match_number_of_accounts, get_week_match_count_of_accounts, get_week_number_of_accounts
from helper_functions import calculate_xp_gained

team1, team2 = get_xp_gained_for_next_week_of_accounts([USERNAME_UPPER, USERNAME_LOWER])
team1 = [calculate_xp_gained(i, rounds_won = winner_score[0] if winner == 'upper' else winner_score[1]) for i in team1]
team2 = [calculate_xp_gained(i, rounds_won = winner_score[0] if winner == 'lower' else winner_score[1]) for i in team2]
xp_gained_details['team1_xp_gained'] = team1
print("Upper Batch XP Gained", xp_gained_details['team1_xp_gained'])
xp_gained_details['team2_xp_gained'] = team2
print("Lower Batch XP Gained", xp_gained_details['team2_xp_gained'])

team1 = {"username": mm_batch['batch_1'], 
         "mm_rank_update": [], 
         "pr_rank_update": [], 
         "match_number": [], 
         "week_number": [], 
         "week_match_count": []}

team2 = {"username": mm_batch['batch_2'], 
         "mm_rank_update": [], 
         "pr_rank_update": [], 
         "match_number": [], 
         "week_number": [], 
         "week_match_count": []}

team1['match_number'], team2['match_number'] = get_match_number_of_accounts([USERNAME_UPPER, USERNAME_LOWER])
team1['match_number'] = [str(int(i) + 1) for i in team1['match_number']]
team2['match_number'] = [str(int(i) + 1) for i in team2['match_number']]

team1['week_number'], team2['week_number'] = get_week_number_of_accounts([USERNAME_UPPER, USERNAME_LOWER])

team1['week_match_count'], team2['week_match_count'] = get_week_match_count_of_accounts([USERNAME_UPPER, USERNAME_LOWER])
team1['week_match_count'] = [str(int(i) + 1) for i in team1['week_match_count']]
team2['week_match_count'] = [str(int(i) + 1) for i in team2['week_match_count']]

from capture_functions import get_mm_rank_snippet, get_pr_rank_snippet
from image_functions import identify_mm_rank, identify_pr_rank

for i in range(5):
    click_only(CSGO_UPPER_POS_X[i] + CSGO_PLAY_BUTTON_X, CSGO_UPPER_POS_Y[i] + CSGO_PLAY_BUTTON_Y, 0.02, 2)
    click_only(CSGO_LOWER_POS_X[i] + CSGO_PLAY_BUTTON_X, CSGO_LOWER_POS_Y[i] + CSGO_PLAY_BUTTON_Y, 0.02, 2)
    click_only(CSGO_UPPER_POS_X[i] + CSGO_PLAY_BUTTON_X, CSGO_UPPER_POS_Y[i] + CSGO_PLAY_BUTTON_Y, 0.02, 2)
    click_only(CSGO_LOWER_POS_X[i] + CSGO_PLAY_BUTTON_X, CSGO_LOWER_POS_Y[i] + CSGO_PLAY_BUTTON_Y, 0.02, 2)
time.sleep(1)

# for i in range(5): #i = 0
#     if cooldown_details['team1'][i]['type'] is None:
#         # click_only(CSGO_UPPER_POS_X[i] + CSGO_PLAY_BUTTON_X, CSGO_UPPER_POS_Y[i] + CSGO_PLAY_BUTTON_Y, 0.1, 1)
#         team1['mm_rank_update'].append(identify_mm_rank(rank_snippet = get_mm_rank_snippet(CSGO_UPPER_POS_X[i], CSGO_UPPER_POS_Y[i], return_numpy_object = True), mm_rank_database = mm_rank_database))
#     else:
#         team1['mm_rank_update'].append(account_data[mm_batch['batch_1'][i]]['MM_Rank'])
#     if cooldown_details['team2'][i]['type'] is None:
#         # click_only(CSGO_LOWER_POS_X[i] + CSGO_PLAY_BUTTON_X, CSGO_LOWER_POS_Y[i] + CSGO_PLAY_BUTTON_Y, 0.1, 1)
#         team2['mm_rank_update'].append(identify_mm_rank(rank_snippet = get_mm_rank_snippet(CSGO_LOWER_POS_X[i], CSGO_LOWER_POS_Y[i], return_numpy_object = True), mm_rank_database = mm_rank_database))
#     else:
#         team2['mm_rank_update'].append(account_data[mm_batch['batch_2'][i]]['MM_Rank'])
#     if cooldown_details['team1'][i]['type'] is None:
#         # click_only(CSGO_UPPER_POS_X[i] + CSGO_PLAY_BUTTON_X, CSGO_UPPER_POS_Y[i] + CSGO_PLAY_BUTTON_Y, 0.1, 1)
#         team1['pr_rank_update'].append(identify_pr_rank(rank_snippet = get_pr_rank_snippet(CSGO_UPPER_POS_X[i], CSGO_UPPER_POS_Y[i], return_numpy_object = True), pr_rank_database = pr_rank_database))
#     else:
#         team1['pr_rank_update'].append(account_data[mm_batch['batch_1'][i]]['PR_Rank'])
#     if cooldown_details['team2'][i]['type'] is None:
#         # click_only(CSGO_LOWER_POS_X[i] + CSGO_PLAY_BUTTON_X, CSGO_LOWER_POS_Y[i] + CSGO_PLAY_BUTTON_Y, 0.1, 1)
#         team2['pr_rank_update'].append(identify_pr_rank(rank_snippet = get_pr_rank_snippet(CSGO_LOWER_POS_X[i], CSGO_LOWER_POS_Y[i], return_numpy_object = True), pr_rank_database = pr_rank_database))
#     else:
#         team2['pr_rank_update'].append(account_data[mm_batch['batch_2'][i]]['PR_Rank'])
for i in range(5): #i = 0
    team1['mm_rank_update'].append(identify_mm_rank(rank_snippet = get_mm_rank_snippet(CSGO_UPPER_POS_X[i], CSGO_UPPER_POS_Y[i], return_numpy_object = True), mm_rank_database = mm_rank_database))
    team2['mm_rank_update'].append(identify_mm_rank(rank_snippet = get_mm_rank_snippet(CSGO_LOWER_POS_X[i], CSGO_LOWER_POS_Y[i], return_numpy_object = True), mm_rank_database = mm_rank_database))
    team1['pr_rank_update'].append(identify_pr_rank(rank_snippet = get_pr_rank_snippet(CSGO_UPPER_POS_X[i], CSGO_UPPER_POS_Y[i], return_numpy_object = True), pr_rank_database = pr_rank_database))
    team2['pr_rank_update'].append(identify_pr_rank(rank_snippet = get_pr_rank_snippet(CSGO_LOWER_POS_X[i], CSGO_LOWER_POS_Y[i], return_numpy_object = True), pr_rank_database = pr_rank_database))

print(team1)
print("\n\n\n")
print(team2)
print("\n\n\n")

from helper_functions import get_current_week_details
log_current_match_details(match_id = match_id, 
                          team1 = team1, 
                          team2 = team2, 
                          time_stamp = match_time_details['match_start_time'], 
                          search_details = search_details, 
                          match_time_details = match_time_details, xp_gained_details = xp_gained_details)
print("Match details Updated")
# TODO: Cooldown_details
update_account_data_completed(mm_batch = mm_batch, 
                              match_id = match_id, 
                              team1 = team1, 
                              team2 = team2, 
                              time_stamp = match_time_details['match_start_time'], 
                              xp_gained_details = xp_gained_details, 
                              cooldown_details = cooldown_details, 
                              week_index = get_current_week_details(include_datetime_obj = False))
print("Account details Updated")

toggle_main_completion()
print("Toggling Main Completion.")
#%%
#%%
    
#%%
#%%
    
    

    
    # create_lobby(CSGO_UPPER_POS_X, CSGO_UPPER_POS_Y, USERNAME_UPPER)
    # create_lobby(CSGO_LOWER_POS_X, CSGO_LOWER_POS_Y, USERNAME_LOWER)
    # right_visible_arrangement(include_play_button = True)
    # identify_and_clear_errors(all_panels = True, error_coordinates = error_coordinates, error_with_numpy_images = error_with_numpy_images, 
    #                       error_ok_button = error_ok_button)
    # restart_if_panel_not_responding()
    # after_lobby_blue_check_wrapper(arrangement_needed = True, checker_image = None)
    # identify_and_clear_errors(all_panels = True, error_coordinates = error_coordinates, error_with_numpy_images = error_with_numpy_images, 
    #                       error_ok_button = error_ok_button)
    
    # right_visible_arrangement(include_play_button = True)
    # start_mm_search(arrangement_needed = False)
    # identify_and_clear_errors(all_panels = True, error_coordinates = error_coordinates, error_with_numpy_images = error_with_numpy_images, 
    #                       error_ok_button = error_ok_button)
    # time.sleep(5)
    
    # FIALED TO REACH CHECK


# runfile('driver_code.py')















