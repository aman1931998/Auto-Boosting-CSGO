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

from dynamic_data_functions import load_old_account_database, load_current_mm_batch, load_mm_batches_index, load_winner_index
from loading_functions import load_account_database
#%% Parsing arguments for running main script.
parser = argparse.ArgumentParser()
parser.add_argument("--clear_old_instance", type = str, help = "Clear old instances", default = True)
parser.add_argument("--after_launch_timeout", type = int, help = "Time to wait after launching panel(s)", default = 150)
parser.add_argument("--launch_timeout", type = float, help = "Time to wait after launching 1 panel", default = 0.5)
parser.add_argument("--untrusted", type = bool, help = "Launch in untrusted mode", default = False)
parser.add_argument("--map_name", type = str, help = "Select the map name", default = "anubis")
parser.add_argument("--match_output", type = str, help = "Match outcome", default = "tie")
parser.add_argument("--winner", type = str, help = "Winner batch", default = "upper")
parser.add_argument("--winner_score", type = str, nargs = 2, help = "Set the score for the match w.r.t. winning lobby", default = "16 4")
parser.add_argument("--current_score", type = str, nargs = 2, help = "Current Score", default = "0 0")
# parser.add_argument("--max_matches", type = int, help = "Number pf matches to play.", default = 4)
args = parser.parse_args()
print("args", args)
#%% Config settings
clear_old_instance = bool(args.clear_old_instance)                             # Whether to clear old instances.
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

#%% Config [Default]
# clear_old_instance = True #False in match 2
# after_launch_timeout = 150
# launch_timeout = 1
# untrusted = False
# map_name = "anubis"
# match_output = 'winlose'
# winner = 'upper' # or 'u'
# current_map = 'anubis'
# winner_score = [16, 4] #[15, 15] #or [16, 0]
# current_score = [0, 0] # or [4, 2]

#%% Paths [Default]
friend_code_dict_path = os.path.join('dynamic', "friend_codes.pkl")                       # Path to friend-codes file.

from loading_functions import load_mm_rank_database, load_pr_rank_database
mm_rank_database = load_mm_rank_database()
pr_rank_database = load_pr_rank_database()


account_data = load_account_database()
mm_batch = load_current_mm_batch()
winner_index = int(load_winner_index())

mm_batch['winner'] = mm_batch['winner'][winner_index]

t1_initial_time = time.time()

print("Getting acccount details")                                              # Getting 10 SteamIDs, Usernames, Passwords for this batch.
USERNAME_UPPER, PASSWORD_UPPER, STEAM_ID_UPPER, USERNAME_LOWER, PASSWORD_LOWER, STEAM_ID_LOWER = get_accounts()
print("Clearing earlier instances and panels.")

if not clear_old_instance:
    try:
        PIDs = load_PIDs()
        for key in PIDs.keys(): #key = list(PIDs.keys())[0]
            if type(PIDs[key]) == list:
                clear_old_instance = True
    except:
        clear_old_instance = True

if not clear_old_instance:
    PIDs = load_PIDs()   #TODO Check if we can remove this fn to avoid r/w calls.
    # Check what else is neeeded for continuingg.
else:
    cleaner()
    cleaner()
    PIDs = {"u1": [], "u2": [], "u3": [], "u4": [], "u5": [], "l1": [], "l2": [], "l3": [], "l4": [], "l5": [] }
    #%% Launching panels.
    print("Launching panels.")
    for i in range(5):#i = 0
        PIDs = get_panel_pids(USERNAME_UPPER[i], PASSWORD_UPPER[i], STEAM_ID_UPPER[i], 
                              "u" + str(i+1), PIDs, launch_timeout = launch_timeout, 
                              trusted_mode = not untrusted, map_name = map_name, clear_old_instance = False)
        print(PIDs)
        PIDs = get_panel_pids(USERNAME_LOWER[i], PASSWORD_LOWER[i], STEAM_ID_LOWER[i], 
                              "l" + str(i+1), PIDs, launch_timeout = launch_timeout, 
                              trusted_mode = not untrusted, map_name = map_name, clear_old_instance = False)
        print(PIDs)
    
    print("Saving PIDs...")
    PIDs = save_PIDs(PIDs)
    
    #%% Checking and getting panels ready.
    print("Waiting for %d seconds for panels to load and start checking..."%(after_launch_timeout))
    time.sleep(after_launch_timeout)
    panels_to_fix = ['u1', 'u2', 'u3', 'u4', 'u5', 'l1', 'l2', 'l3', 'l4', 'l5']
    panels_ready, exit_count_, max_exit_count = [], 0, 6 #### Main settings ['u1', 'u2', 'u3', 'u4', 'u5', 'l1', 'l2', 'l3', 'l4', 'l5']
    panels_launch_successful = False

    while not panels_launch_successful:
        exit_count_ += 1
        if exit_count_ == max_exit_count:
            os.system("ipconfig /release"); time.sleep(0.1); os.system("ipconfig /flushdns"); time.sleep(0.1); os.system("ipconfig /renew"); time.sleep(0.1)
            accept_args = get_accept_args()
            runfile('main_file.py', accept_args)
            sys.exit(0)
        # panels_to_check = panels_to_fix
        panels_to_fix = check_launched_panel_wrapper(checker_image = None, panels_to_check = panels_to_fix)
        if panels_to_fix == []:
            print("Panels Launch Successful.")
            panels_launch_successful = True
        print("Panels to fix!!!!: ", *panels_to_fix)
        PIDs = kill_PIDs(PIDs, panels_to_fix)
        print(PIDs)

        for panel in panels_to_fix:
            panel_top_left_x, panel_top_left_y, (username, password, steamid) = get_top_left_position_from_panel_name(panel, include_account_details = True)
            PIDs = get_panel_pids(username, password, steamid, panel, PIDs, launch_timeout = launch_timeout, trusted_mode = not untrusted, map_name = map_name)
        print("Saving PIDs")
        print(PIDs)
        PIDs = save_PIDs(PIDs)
        print(PIDs)
        panels_error = []
        tt1 = time.time()
        #time.sleep(60)
        for panel in ['u1', 'u2', 'u3', 'u4', 'u5', 'l1', 'l2', 'l3', 'l4', 'l5']:
            if panel in panels_to_fix:
                continue
            if panel in panels_ready:
                continue
            pos_x, pos_y = get_top_left_position_from_panel_name(panel, include_account_details = False)
            index = CSGO_UPPER_POS_X.index(pos_x)
            click_only(CSGO_TITLE_BAR_X[index] + pos_x, CSGO_TITLE_BAR_Y[index] + pos_y, 0.2, 2)
            if check_launched_panel(POS_X = pos_x, POS_Y = pos_y):
                vac_signature_error_op = ready_panel(pos_x, pos_y, untrusted_check = untrusted, untrusted_check_times = 1, panel_number = panel, do = True)
                if not vac_signature_error_op:
                    panels_ready.append(panel)
            else:
                
                panels_error.append(panel)
        tt2 = time.time()
        if (tt2-tt1) < after_launch_timeout and panels_to_fix != []: ### added
            time.sleep(after_launch_timeout - (tt2-tt1))
        
        print("!!!!!!Panels to fix: ", *panels_error)
        PIDs = kill_PIDs(PIDs, panels_error)
        print(PIDs)
        panels_to_fix += panels_error

    t2_time_to_launch = time.time()
    print("Time taken to launch and get panels ready. %.2f"%(t2_time_to_launch - t1_initial_time))
    
    
    # identify_and_clear_errors(all_panels = True, error_coordinates = error_coordinates, error_with_numpy_images = error_with_numpy_images, 
    #                           error_ok_button = error_ok_button)


#%% Checks whether any one lobby is already created or not.
    
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

# get rank snippets
# right_visible_arrangement()
# get_rank_snippets(all_panels = True)

# #%% Cooldown check
# if cd_check_wrapper(all_panels = True):
#     #runfile('new_driver_code.py')
#     runfile('driver_code.py')
#     sys.exit(0)

# Getting panels ready
after_lobby_blue_check_wrapper(arrangement_needed = True, checker_image = None, ignore_first_attempt = True)



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

right_visible_arrangement(include_play_button = True)
start_mm_search(arrangement_needed = False)

#%%
from dynamic_data_functions import reset_match_verification, verify_match_completion, toggle_main_completion
from helper_functions import generate_unique_mismatchID, generate_unique_matchID
mm_mismatchID = generate_unique_mismatchID(include_prefix = True)
mismatch_data = {}

search_details = {"search_start_time": None, 
                  "search_error_count": 0, 
                  "search_mismatchID": None, 
                  "search_end_time": None}
search_start_time = datetime.now()
search_details['search_start_time'] = search_start_time
search_mismatchID = mm_mismatchID
search_details['search_mismatchID'] = search_mismatchID


vac_max_count = 5
vac_count = 0
while True:
    vac_status = check_green_mm_search_wrapper()
    if vac_status:
        print("VAC STATUS: %s"%(vac_status))
        vac_count+=1
        start_mm_search(arrangement_needed = False)
    else:
        print("VAC Status successful.")
        break
    if vac_count == vac_max_count:
        print("VAC Error: Relaunching panels.")
        time.sleep(2)
        accept__args = get_accept_args()
        runfile('main_file.py', accept__args)

# time.sleep(5)

restart_if_panel_not_responding()
#avast_popup(test_image = None, checker_image = avast_popup_checker_image, cancel_match_ = False)
#%%
#%%

from logging_functions import log_current_mismatch_details, log_current_match_details, update_account_data_completed

 #TODO LOOP IT FAILED TO REACH CHECK
while True:
    panels_with_failed_connection = failed_to_reach_servers_check_wrapper(arrangement_needed = False, checker_image = None, checker_full_image = None)
    
    if panels_with_failed_connection == []:
        print("No Connection Errors.")
        break
    else:
        log_current_mismatch_details(mm_mismatchID, mm_batch, mismatch_data, match_found = False, total_search_time = 0)
        accept__args = get_accept_args()
        runfile('main_file.py', accept__args)
        sys.exit(0)

#%%
#%%
while True:
    terminate_and_matches_played, mismatch_data = auto_accept_check(mismatch_data)
    search_details['search_end_time'] = datetime.now()
    # If match is not found after a given time.
    if terminate_and_matches_played == False:
        # TODO function to add a set of 
        # TODO!!!!!!!!!!!!!!!!!!!!!!!!
        #TODO add mismatch log function
        log_current_mismatch_details(mm_mismatchID, mm_batch, mismatch_data, match_found = False, total_search_time = (datetime.now() - search_start_time).seconds)
        break
        #sys.exit(0)
    search_details['search_error_count'] = len(mismatch_data.keys())
    search_end_time = search_details['search_end_time']
    match_found = True
    
    # add log mismatch fn (with match_)fpund = True
    # see whether we have to add it here or after connection check.
    
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
    match_time_details = {}
    match_time_details['match_start_time'] = datetime.now()
    print("Waiting for Warmup to end with extra 10 seconds time gap.")
    time.sleep(60 + 5 + 15 + 5)
    
    reset_match_verification()

    accept_args = "--map_name %s --match_output %s --winner %s --winner_score %d %d --current_score %d %d"%(map_name, match_output, winner, winner_score[0], winner_score[1], current_score[0], current_score[1])
    runfile('ingame_script.py', args = accept_args)
    after_match_cleanup(0)

    match_end_time = datetime.now()

    cooldown_details = {"team1": [], "team2": []}
    for i in range(4, -1, -1):
        cd_op = cd_check(CSGO_UPPER_POS_X[i], CSGO_UPPER_POS_Y[i])
        if cd_op != None:
            cd_time = match_end_time
        else:
            cd_time = None
        cd_data = {"type": cd_op, "time": match_end_time}
        cooldown_details['team1'].insert(0, cd_data)

        cd_op = cd_check(CSGO_LOWER_POS_X[i], CSGO_LOWER_POS_Y[i])
        if cd_op != None:
            cd_time = match_end_time
        else:
            cd_time = None
        cd_data = {"type": cd_op, "time": match_end_time}
        cooldown_details['team2'].insert(0, cd_data)
    
    
    # TODO
    status = verify_match_completion()
    if not status:
        log_current_mismatch_details(mm_mismatchID, mm_batch, mismatch_data, match_found = False, total_search_time = (datetime.now() - search_start_time).seconds)
        break
        
    log_current_mismatch_details(mm_mismatchID, mm_batch, mismatch_data, match_found = match_found, total_search_time = (search_end_time - search_start_time).seconds)
    match_time_details['match_end_time'] = match_end_time 

    xp_gained_details = {"team1_xp_gained": [], "team2_xp_gained": []}
    
    from loading_functions import get_xp_gained_for_next_week_of_accounts, get_match_number_of_accounts, get_week_match_count_of_accounts, get_week_number_of_accounts
    from helper_functions import calculate_xp_gained
    
    team1, team2 = get_xp_gained_for_next_week_of_accounts([USERNAME_UPPER, USERNAME_LOWER])
    team1 = [calculate_xp_gained(i, rounds_won = winner_score[0] if winner == 'upper' else winner_score[1]) for i in team1]
    team2 = [calculate_xp_gained(i, rounds_won = winner_score[0] if winner == 'lower' else winner_score[1]) for i in team2]
    xp_gained_details['team1_xp_gained'] = team1
    xp_gained_details['team2_xp_gained'] = team2
    
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
    
    for i in range(5): #i = 0
        if cooldown_details['team1'][i]['type'] is None:
            team1['mm_rank_update'].append(account_data[mm_batch['batch_1'][i]]['MM_Rank'])
        else:
            team1['mm_rank_update'].append(identify_mm_rank(rank_snippet = get_mm_rank_snippet(CSGO_UPPER_POS_X[i], CSGO_UPPER_POS_Y[i], return_numpy_object = True), mm_rank_database = mm_rank_database))
        if cooldown_details['team2'][i]['type'] is None:
            team2['mm_rank_update'].append(account_data[mm_batch['batch_2'][i]]['MM_Rank'])
        else:
            team2['mm_rank_update'].append(identify_mm_rank(rank_snippet = get_mm_rank_snippet(CSGO_LOWER_POS_X[i], CSGO_LOWER_POS_Y[i], return_numpy_object = True), mm_rank_database = mm_rank_database))
        if cooldown_details['team1'][i]['type'] is None:
            team1['pr_rank_update'].append(account_data[mm_batch['batch_1'][i]]['PR_Rank'])
        else:
            team1['pr_rank_update'].append(identify_pr_rank(rank_snippet = get_pr_rank_snippet(CSGO_UPPER_POS_X[i], CSGO_UPPER_POS_Y[i], return_numpy_object = True), mm_rank_database = mm_rank_database))
        if cooldown_details['team2'][i]['type'] is None:
            team2['pr_rank_update'].append(account_data[mm_batch['batch_2'][i]]['PR_Rank'])
        else:
            team2['pr_rank_update'].append(identify_pr_rank(rank_snippet = get_pr_rank_snippet(CSGO_LOWER_POS_X[i], CSGO_LOWER_POS_Y[i], return_numpy_object = True), mm_rank_database = mm_rank_database))
    
    from helper_functions import get_current_week_details
    log_current_match_details(match_id = match_id, 
                              team1 = team1, 
                              team2 = team2, 
                              time_stamp = match_time_details['match_start_time'], 
                              search_details = search_details, 
                              match_time_details = match_time_details, xp_gained_details = xp_gained_details)
    
    # TODO: Cooldown_details
    update_account_data_completed(mm_batch = mm_batch, 
                                  match_id = match_id, 
                                  team1 = team1, 
                                  team2 = team2, 
                                  time_stamp = match_time_details['match_start_time'], 
                                  xp_gained_details = xp_gained_details, 
                                  cooldown_details = cooldown_details, 
                                  week_index = get_current_week_details(include_datetime_obj = False))
    
    toggle_main_completion()
#%%
#%%
    
#%%
#%%
    
    
    
    
    
    
    if cd_check_wrapper(True):
        #runfile('new_driver_code.py')
        runfile('driver_code.py')
        sys.exit(0)
    
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

















