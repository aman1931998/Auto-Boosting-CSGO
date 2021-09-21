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

#%% Parsing arguments for running main script.
parser = argparse.ArgumentParser()
parser.add_argument("--clear_old_instance", type = str, help = "Clear old instances", default = False)
parser.add_argument("--after_launch_timeout", type = int, help = "Time to wait after launching panel(s)", default = 180)
parser.add_argument("--untrusted", type = bool, help = "Launch in untrusted mode", default = True)
parser.add_argument("--map_name", type = str, help = "Select the map name", default = "anubis")
parser.add_argument("--match_output", type = str, help = "Match outcome", default = "tie")
parser.add_argument("--winner", type = str, help = "Winner batch", default = "upper")
parser.add_argument("--winner_score", type = str, nargs = 2, help = "Set the score for the match w.r.t. winning lobby", default = "15 15")
parser.add_argument("--current_score", type = str, nargs = 2, help = "Current Score", default = "0 0")
# parser.add_argument("--max_matches", type = int, help = "Number pf matches to play.", default = 4)
args = parser.parse_args()

#%% Config settings
clear_old_instance = bool(args.clear_old_instance)                             # Whether to clear old instances.
launch_timeout = 0.5                                                           # Timeout after launching a panel
after_launch_timeout = int(args.after_launch_timeout)                          # Timeout after launching all panels
untrusted = bool(args.untrusted)                                               # Launch in Trusted mode or not.
map_name = str(args.map_name).lower()                                          # Name of the map to play
match_output = str(args.match_output).lower()                                  # Output of the match. Eg: 16 14 or 16 0 or 15 15
winner = str(args.winner).lower()                                              # Winner lobby [upper or lower]

try: winner_score = list(map(int, str(args.winner_score).split()))
except: winner_score = list(map(int, args.winner_score))
try: current_score = list(map(int, str(args.current_score).split()))
except: current_score = list(map(int, args.current_score))
# max_matches = int(args.max_matches)                                          # Maximum number of matches to play with a batch. [Superseded by other functions. Not in use]
# number_of_matches = 1

#%% Config [Default]
# clear_old_instance = False
# after_launch_timeout = 120
# untrusted = True
# map_name = "anubis"
# match_output = "tie" #'winlose' #
# winner = 'upper' # or 'u'
# current_map = 'anubis'
# winner_score = [16, 14] #[15, 15] #or [16, 0]
# current_score = [0, 0] # or [4, 2]

#%% Paths
friend_code_dict_path = os.path.join("friend_codes.pkl")                       # Path to friend-codes file.

#%% Start
t1_initial_time = time.time()
print("Getting acccount details")                                              # Getting 10 SteamIDs, Usernames, Passwords for this batch.
USERNAME_UPPER, PASSWORD_UPPER, STEAM_ID_UPPER, USERNAME_LOWER, PASSWORD_LOWER, STEAM_ID_LOWER = get_accounts()
print("Clearing earlier instances and panels.")
cleaner()
cleaner()

#%% Clearing PID cache.
PIDs = {"u1": [], "u2": [], "u3": [], "u4": [], "u5": [], "l1": [], "l2": [], "l3": [], "l4": [], "l5": [] }

#%% Launching Upper panels.
print("Launching panels.")
for i in range(5):#i = 0
    PIDs = get_panel_pids(USERNAME_UPPER[i], PASSWORD_UPPER[i], STEAM_ID_UPPER[i], 
                          "u" + str(i+1), PIDs, launch_timeout = launch_timeout, 
                          trusted_mode = not untrusted, map_name = map_name, clear_old_instance = False)
    PIDs = get_panel_pids(USERNAME_LOWER[i], PASSWORD_LOWER[i], STEAM_ID_LOWER[i], 
                          "l" + str(i+1), PIDs, launch_timeout = launch_timeout, 
                          trusted_mode = not untrusted, map_name = map_name, clear_old_instance = False)

print("Waiting %d for panels to load."%(after_launch_timeout))
time.sleep(after_launch_timeout)

#%% #Dumping data for later movement.
#save_pickle_file(os.path.join("temp", "backup_pkl", ))
# save_PIDs(PIDs, PIDs_dict)

#%%
time.sleep(2)
panels_ready, exit_count_, max_exit_count = ['u1', 'u2', 'u3', 'u4', 'u5', 'l1', 'l2', 'l3', 'l4', 'l5'], 0, 15
while True:
    exit_count_ += 1
    panels_to_fix = check_launched_panel_wrapper(checker_image = None)
    if panels_to_fix == []: print("Panels launch successful."); break          # If all panels launched: BREAK
    print("Panels to fix: ", *panels_to_fix)
    PIDs = kill_PIDs(PIDs, panels_to_fix)
    for panel in panels_to_fix:
        panel_top_left_x, panel_top_left_y, (username, password, steamid) = get_top_left_position_from_panel_name(panel, include_account_details = True)
        PIDs = get_panel_pids(username, password, steamid, panel, PIDs, launch_timeout = launch_timeout, trusted_mode = not untrusted, map_name = map_name)

    print("Waiting for %d seconds for panels to load."%(after_launch_timeout))    
    time.sleep(after_launch_timeout)
    
    if exit_count_ == max_exit_count:
        os.system("ipconfig /release"); time.sleep(0.1); os.system("ipconfig /flushdns"); time.sleep(0.1); os.system("ipconfig /renew"); time.sleep(0.1)
        runfile('main_file.py')
        sys.exit(0)

t2_time_to_launch = time.time()
print("Time taken to launch %.2f"%(t2_time_to_launch - t1_initial_time))

restart_if_panel_not_responding()                                              # Panel Check.

#%% Getting panels ready (by the time, panels are ready and responding/running)
print("Getting panels ready.")
for i in range(5):
    if ready_panel(CSGO_UPPER_POS_X[i], CSGO_UPPER_POS_Y[i], untrusted_check = True, panel_number = 'u' + str(i+1), do = True): #VAC signature error
        PIDs = relaunch_panels_and_ready(PIDs, 'u' + str(i+1), map_name = map_name, trusted_mode = not untrusted, after_launch_timeout = after_launch_timeout)
    if ready_panel(CSGO_LOWER_POS_X[i], CSGO_LOWER_POS_Y[i], untrusted_check = True, panel_number = 'l' + str(i+1), do = True):
        PIDs = relaunch_panels_and_ready(PIDs, 'l' + str(i+1), map_name = map_name, trusted_mode = not untrusted, after_launch_timeout = after_launch_timeout)

t3_time_to_get_panels_ready = time.time()
print("Time taken to get panels_ready: %.2f"%(t3_time_to_get_panels_ready - t2_time_to_launch))

restart_if_panel_not_responding()
avast_popup(test_image = None, checker_image = avast_popup_checker_image, cancel_match_ = False)
#%% Creating lobbies
print("Getting friend codes.")
friend_code_dict = load_friend_code_dict_file(friend_code_dict_path)

upper_batch = [CSGO_UPPER_POS_X, CSGO_UPPER_POS_Y, USERNAME_UPPER]
lower_batch = [CSGO_LOWER_POS_X, CSGO_LOWER_POS_Y, USERNAME_LOWER]

# get rank snippets
right_visible_arrangement()
get_rank_snippets(all_panels = True)

#%% Cooldown check
if cd_check_wrapper(True):
    #runfile('new_driver_code.py')
    runfile('driver_code.py')
    sys.exit(0)

identify_and_clear_errors(all_panels = True, error_coordinates = error_coordinates, error_with_numpy_images = error_with_numpy_images, 
                          error_ok_button = error_ok_button)
#%%
for batch in [upper_batch, lower_batch]: #batch = upper_batch.copy()
    POS_X, POS_Y, USERNAME = batch
    create_lobby(POS_X, POS_Y, USERNAME)

identify_and_clear_errors(all_panels = True, error_coordinates = error_coordinates, error_with_numpy_images = error_with_numpy_images, 
                          error_ok_button = error_ok_button)

restart_if_panel_not_responding()
#avast_popup(test_image = None, checker_image = avast_popup_checker_image, cancel_match_ = False)
time.sleep(1)
after_lobby_blue_check_wrapper(arrangement_needed = True, checker_image = None)
    

t4_lobbies_created = time.time()
print("Lobbies created, time taken: %.2f"%(t4_lobbies_created - t3_time_to_get_panels_ready))

identify_and_clear_errors(all_panels = True, error_coordinates = error_coordinates, error_with_numpy_images = error_with_numpy_images, 
                          error_ok_button = error_ok_button)

#%% Start MM Search
time.sleep(1)
#right_visible_arrangement(include_play_button = True)
start_mm_search(arrangement_needed = True)

vac_max_count = 5
vac_count = 0
while True:
    vac_status = check_green_mm_search_wrapper()
    if vac_status:
        print("VAC STATUS: %s"%(vac_status))
        vac_count+=1
        start_mm_search(arrangement_needed = False)
    else:
        break
    if vac_count == vac_max_count:
        print("VAC Error: Relaunching panels.")
        time.sleep(2)
        accept__args = get_accept_args()
        runfile('main_file.py', accept__args)

time.sleep(5)

restart_if_panel_not_responding()
avast_popup(test_image = None, checker_image = avast_popup_checker_image, cancel_match_ = False)
#%%

 #TODO LOOP IT FAILED TO REACH CHECK
while True:
    panels_with_failed_connection = failed_to_reach_servers_check_wrapper(arrangement_needed = False, checker_image = None, checker_full_image = None)
    
    if panels_with_failed_connection == []:
        break
    else:
        accept__args = get_accept_args()
        runfile('main_file.py', accept__args)
        sys.exit(0)
        '''
        stop_mm_search(arrangement_needed = False)
        while True:
            panels_to_fix = check_launched_panel_wrapper(checker_image = None)
            panels_to_fix = []
            for panel in panels_with_failed_connection:
                x, y = get_panel_location(panel)
                if not check_launched_panel(test_image = None, checker_image = None, POS_X = x, POS_Y = y):
                    panels_to_fix.append(panel)
            if panels_to_fix == []:
                print("All Panels launched.")
                break
            print("Panels to fix: ", *panels_to_fix)
            PIDs = kill_PIDs(PIDs, panels_to_fix)
            for panel in panels_to_fix:
                panel_top_left_x, panel_top_left_y, account_details = get_top_left_position_from_panel_name(panel, include_account_details = True)
                username, password, steamid = account_details
                PIDs = get_panel_pids(username, password, steamid, panel, PIDs, launch_timeout = launch_timeout, trusted_mode = not untrusted, map_name = map_name)
            print("Waiting %d for panels to load."%(after_launch_timeout))
            time.sleep(after_launch_timeout) 

        for panel in panels_with_failed_connection:
            POS_X, POS_Y = get_top_left_position_from_panel_name(panel)
            ready_panel(POS_X, POS_Y, untrusted_check = True)

        identify_and_clear_errors(all_panels = True, error_coordinates = error_coordinates, error_with_numpy_images = error_with_numpy_images, 
                                  error_ok_button = error_ok_button)
        leave_lobby('upper')
        leave_lobby('lower')
        
        restart_if_panel_not_responding()
        avast_popup(test_image = None, checker_image = avast_popup_checker_image, cancel_match_ = False)
        
        create_lobby(CSGO_UPPER_POS_X, CSGO_UPPER_POS_Y, USERNAME_UPPER)
        create_lobby(CSGO_LOWER_POS_X, CSGO_LOWER_POS_Y, USERNAME_LOWER)

        identify_and_clear_errors(all_panels = True, error_coordinates = error_coordinates, error_with_numpy_images = error_with_numpy_images, 
                                  error_ok_button = error_ok_button)
    
        after_lobby_blue_check_wrapper(arrangement_needed = True, checker_image = None)
        
        start_mm_search(arrangement_needed = False)
        
        identify_and_clear_errors(all_panels = True, error_coordinates = error_coordinates, error_with_numpy_images = error_with_numpy_images, 
                                  error_ok_button = error_ok_button)
        time.sleep(5)

        restart_if_panel_not_responding()
        avast_popup(test_image = None, checker_image = avast_popup_checker_image, cancel_match_ = False)
        '''
#%%


#%% necessary function
def get_current_active_account_steamids():
    with open('active_accounts.txt', 'r') as file:
        data = list(map(lambda x: x.split(), file.readlines()))
    steamid = [i[0] for i in data]
    return steamid
def write_stats_for_accounts_to_file():
    steamids = get_current_active_account_steamids()
    file_name = ".".join(steamids)
    with open(os.path.join('temp', 'account_log', file_name + '.txt'), 'w') as file:
        with open('active_accounts.txt', 'r') as file2:
            data = file2.read()
        file.write(str(data))
        file.write("\n\n\n")
        with open("number_of_matches_played.txt", 'r') as file2:
            max_matches_played = str(file2.read())
        file.write(max_matches_played)

#%%
while True:
    terminate_and_matches_played = auto_accept_check()
    
    if terminate_and_matches_played is not None:
        # TODO function to add a set of 
        write_stats_for_accounts_to_file()
        break
        #sys.exit(0)
    
    time.sleep(5)
    # TODO UPDATE AND CHANGE
    print("Waiting for panels to connect to server.")
    reconnection_output = map_loading_check_wrapper(map_name = map_name, method = 'all', max_time = 30)
    
    if type(reconnection_output) != bool:
        cancel_match()
        failsafe = True
    
    print("Waiting for Warmup to end with extra 10 seconds time gap.")
    time.sleep(60 + 5 + 15 + 5 + 15)

    accept_args = "--map_name %s --match_output %s --winner %s --winner_score %d %d --current_score %d %d"%(map_name, match_output, winner, winner_score[0], winner_score[1], current_score[0], current_score[1])
    runfile('ingame_script.py', args = accept_args)

    
    time.sleep(5)
    restart_if_panel_not_responding()
    avast_popup(test_image = None, checker_image = avast_popup_checker_image, cancel_match_ = False)
    
    after_match_cleanup(5)
    
    
    # check for next match
    next_match = play_next_match()
    if next_match is False:
        right_visible_arrangement()
        get_rank_snippets(all_panels = True)
        #update_account_statistics()
        break
    winner = get_winner_lobby()
    print("Winner for next match: %s"%(winner))

    if cd_check_wrapper(True):
        #runfile('new_driver_code.py')
        runfile('driver_code.py')
        sys.exit(0)
    if cd_check_wrapper(True):
        #runfile('new_driver_code.py')
        runfile('driver_code.py')
        sys.exit(0)
    if cd_check_wrapper(True):
        #runfile('new_driver_code.py')
        runfile('driver_code.py')
        sys.exit(0)
    
    create_lobby(CSGO_UPPER_POS_X, CSGO_UPPER_POS_Y, USERNAME_UPPER)
    create_lobby(CSGO_LOWER_POS_X, CSGO_LOWER_POS_Y, USERNAME_LOWER)
    right_visible_arrangement(include_play_button = True)
    identify_and_clear_errors(all_panels = True, error_coordinates = error_coordinates, error_with_numpy_images = error_with_numpy_images, 
                          error_ok_button = error_ok_button)
    restart_if_panel_not_responding()
    after_lobby_blue_check_wrapper(arrangement_needed = True, checker_image = None)
    identify_and_clear_errors(all_panels = True, error_coordinates = error_coordinates, error_with_numpy_images = error_with_numpy_images, 
                          error_ok_button = error_ok_button)
    
    right_visible_arrangement(include_play_button = True)
    start_mm_search(arrangement_needed = False)
    identify_and_clear_errors(all_panels = True, error_coordinates = error_coordinates, error_with_numpy_images = error_with_numpy_images, 
                          error_ok_button = error_ok_button)
    time.sleep(5)
    
    # FIALED TO REACH CHECK


def update_account_statistics_final():
    data = open('active_accounts.txt', 'r').readlines()
    usernames = [i.split()[1] for i in data]
    file = open('accounts_to_boost.txt', 'a')
    for username in usernames:
        file.write(username)
        file.write("\n")
    
    
    
    


#update_account_statistics_final()
#runfile('new_driver_code.py')
runfile('driver_code.py')



















