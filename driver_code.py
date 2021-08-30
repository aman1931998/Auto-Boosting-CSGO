import copy
import time, beepy
import shutil, os, pickle, cv2, psutil, sys
import pyautogui as pg, keyboard as kb
import numpy as np
import pandas as pd
import pyperclip as pc
from PIL import Image, ImageGrab#, ImageOps
from datetime import datetime, timedelta
# from positions import *
# from driver_functions import *
# from mm_batch_creator_functions import *
# from helper_functions import *
# from functions import *
# from major_functions import *
# from time import sleep

from project_path import steam_path
from loading_functions import load_account_database, load_usernames
from logging_functions import update_account_data_completed
from mm_batch_creator_functions import get_mm_batches, get_mm_batches_ranked
from helper_functions import clean_network_dns_data, new_week_check, update_new_week_triggers, check_week_trigger, update_account_stats_after_week_change
from major_functions import save_accept_args, power_connection_check
#%% MAIN SETTINGS
from config_variables import repeat_driver_code, continue_with_old
#%% Load all usernames
usernames = load_usernames()
#%% #UNRANKED ACCOUNTS
from config_variables import consider_unranked_accounts, unranked_consideration_threshold, \
    mm_batches_creation_mode, shuffle_sub_categories, consider_cooldown
#%% #RANKED ACCOUNTS
from config_variables import consider_ranked_accounts, ranked_consideration_threshold, maintain_on_unequal, target_xp
#%% Match Settings
from config_variables import after_launch_timeout, launch_timeout, untrusted, map_name, match_output, winner_score
#%% CLEANUP
from config_variables import cleanup_on_running_driver_file, clean_userdata_folder_after_running_batch, clean_network_data_after_running_batch
#%% Power supply check
from config_variables import power_supply_check


####################################
####################################
####################################
#
# in a lot of places, I have used 'batch_1' instead of in a list ||| #TODO
#
####################################
####################################
####################################

if check_week_trigger():
    update_new_week_triggers()
    update_account_stats_after_week_change()
    continue_with_old = False

#
#%% Cleanup tasks
if cleanup_on_running_driver_file:
    runfile('cleaner.py')
if clean_network_data_after_running_batch:
    clean_network_dns_data()

#%% Continue with old 
from dynamic_data_functions import save_mm_batches, load_mm_batches, save_mm_batches_index, load_mm_batches_index, save_old_account_database, load_old_account_database, save_current_mm_batch, load_current_mm_batch, save_winner_index, load_winner_index, reset_main_verification, verify_main_completion
from helper_functions import unranked_mm_batches_available, ranked_mm_batches_available, get_number_of_matches_to_play


# Verifying!
if continue_with_old: #Verifying validity of continue_with_old option
    print("Verifying Validity of old batch.")
    mm_batches = load_mm_batches()                # Loaded old mm batches
    mm_batches_index = load_mm_batches_index()    # Loaded mm batches index
    if mm_batches == False or type(mm_batches_index) == bool:
        continue_with_old = False
        mm_batches = []
    else:
        if len(mm_batches) == mm_batches_index:
            continue_with_old = False
            mm_batches = []
else:
    mm_batches = []

# Loading old database, mm_batches and mm_batches_index
if continue_with_old:
    print("Continuing with Old batch.")
    print("Loading Old Batch and databases")
    account_data = load_account_database()    # Loaded old database
    mm_batches = load_mm_batches()                # Loaded old mm batches
    mm_batches_index = load_mm_batches_index()    # Loaded mm batches index
    print("INDEX:", mm_batches_index)
    print(mm_batches[mm_batches_index])
    winner_index = load_winner_index()
    print("Winner Index:", winner_index)
else:
    print("Loading Fresh Account Data")
    account_data = load_account_database(usernames = usernames, return_type = 'dict', username_oriented = True)
    # Saving account_data for current session to be resumed later.
    save_old_account_database(account_data = account_data)
    print("Saving this database.")

    '''
# Used in creating batches of ranked accounts
import random
mm_rank_names = ['s1', 's2', 's3', 's4', 'se', 'sem', 'gn1', 'gn2', 'gn3', 'gnm', 'mg1', 'mg2', 'mge', 'dmg', 'le', 'lem', 'smfc', 'ge', 'expired', 'unranked']
for username in account_data.keys(): #username = list(account_data.keys())[0]
    for i in range(10):
        account_data[username]['Matches_History'].append(random.choice(['w', 'l']))
    account_data[username]['MM_Rank'] = random.choice(mm_rank_names[:18])
    account_data[username]['XP_Gained_For_Next_Rank'] = random.choice([0, 0, 0, 0, 0, 2000, 4000, 4000])

    '''

    #%% Getting MM batches of ranked_accounts
    # Verifying!
    if consider_ranked_accounts:
        print("Verifying Ranked Accounts with threshold: %d"%(unranked_consideration_threshold))
        if not ranked_mm_batches_available(account_data, threshold = ranked_consideration_threshold):
            consider_ranked_accounts = False
    
    if consider_ranked_accounts:
        print('Creating Ranked Batches')
        # Getting the dict of usernames with rank_defined.
        match_count_oriented_usernames_dict = get_number_of_matches_to_play(usernames = usernames, account_data = account_data, return_type = 'dict', sub_categories_mm_ranks = True, match_sequence = winner_score)


        try:
            match_count_oriented_usernames_dict[6]['ge'] = []
        except:
            pass

        mm_batches += get_mm_batches_ranked(match_count_oriented_usernames_dict = match_count_oriented_usernames_dict, 
                                            account_data = account_data, maintain_on_unequal = maintain_on_unequal, target_xp = target_xp)
        
        
        
        
        for mm_batch in mm_batches: #mm_batch = mm_batches[0]
            mm_batch['winner'] = ['batch_2', 'batch_1', 'batch_2', 'batch_1', 'batch_2', 'batch_1']
        
        
        
        mm_batches_index = 0
        print("MM_batch_index:", mm_batches_index)
        print("Current Batch:", mm_batches[mm_batches_index])
        # Saving mm_batches and it's index for the current session
        save_mm_batches(mm_batches)
        save_mm_batches_index(mm_batches_index)

    #%% Getting MM batches for Unranked accounts
    # Verifying!
    if consider_unranked_accounts:  # Should we consider unranked accounts?
        print("Verifying Unranked accounts with threshold: %d"%(unranked_consideration_threshold))
        if not unranked_mm_batches_available(account_data, threshold = unranked_consideration_threshold):
            consider_unranked_accounts = False

    if consider_unranked_accounts:
        print('Creating Unranked Batches')
        dynamic_account_data = copy.deepcopy(account_data) #dict(account_data)  #account_data.copy()
        mm_batches += get_mm_batches(account_data = dynamic_account_data, batch_creation_mode = mm_batches_creation_mode, 
                                    shuffle_sub_categories = shuffle_sub_categories, consider_cooldown = consider_cooldown)    
        mm_batches_index = 0
        # Saving mm_batches and it's index for the current session
        save_mm_batches(mm_batches)
        save_mm_batches_index(mm_batches_index)
    

    winner_index = 0
    print("Winner Index:", winner_index)
    save_winner_index(winner_index)


if power_supply_check:
    power_connection_check()

assert mm_batches_index != None
assert mm_batches != None
#%% Accounts in action
while int(mm_batches_index) < len(mm_batches):
    mm_batches_index = int(load_mm_batches_index())
    print("MM Batches_Index", mm_batches_index, "of", len(mm_batches))
    mm_batch = mm_batches[mm_batches_index]
    # Saving current_mm_batch
    save_current_mm_batch(mm_batch)
    team_1_usernames = mm_batch['batch_1']
    team_2_usernames = mm_batch['batch_2']
    team_1_steamids = [account_data[username]['SteamID'] for username in team_1_usernames]
    team_2_steamids = [account_data[username]['SteamID'] for username in team_2_usernames]
    team_1_passwords = [account_data[username]['Password'] for username in team_1_usernames]
    team_2_passwords = [account_data[username]['Password'] for username in team_2_usernames]
    winner_sequence = mm_batch['winner']
    
    print("Usernames 1: ", team_1_usernames)
    print("Usernames 2: ", team_2_usernames)
    
    new_data = []
    for i in range(5):
        l = [team_1_steamids[i], team_1_usernames[i], team_1_passwords[i]]
        new_data.append(l)
    for i in range(5):
        l = [team_2_steamids[i], team_2_usernames[i], team_2_passwords[i]]
        new_data.append(l)
    with open('active_accounts.txt', 'w') as file:
        for i in range(len(new_data)):
            for j in range(3):
                file.write(str(new_data[i][j]))
                file.write(" ")
            if i != 9:
                file.write('\n')

    clear_old_instances = 1 ## True for first index in winner_sequence, otherwise False.
    
    winner_index = 0
    print("Winner Index:", winner_index, "of %d"%(len(winner_sequence)))
    save_winner_index(winner_index)
    while int(winner_index) < len(winner_sequence):
        if new_week_check():
            runfile('driver_code.py')
            sys.exit(0)
            
    #for winner_index in range(len(winner_sequence)): #winner_index = 0
        print("Winner Index: ", winner_index)
        if clear_old_instances:
            clear_old_instances_internal = 1
            clear_old_instances = 0
        else:
            clear_old_instances_internal = 0
        print("Clearing Old instances:", clear_old_instances_internal)
        winner = 'upper' if winner_sequence[int(winner_index)] == 'batch_1' else 'lower'
        print("Winner:", winner)
        current_score = [0, 0]
        print(str(clear_old_instances_internal), \
              after_launch_timeout, \
              launch_timeout, \
              str(untrusted), \
              map_name, \
              match_output, \
              winner, \
              winner_score[0], \
              winner_score[1], \
              current_score[0], \
              current_score[1])

        accept_args = "--clear_old_instance %s --after_launch_timeout %d --launch_timeout %d --untrusted %s --map_name %s --match_output %s --winner %s --winner_score %d %d --current_score %d %d"%(str(clear_old_instances_internal), \
                        after_launch_timeout, \
                        launch_timeout, \
                        str(untrusted), \
                        map_name, \
                        match_output, \
                        winner, \
                        winner_score[0], \
                        winner_score[1], \
                        current_score[0], \
                        current_score[1])
        save_accept_args(accept_args)
        print(accept_args)
        print("Args for runfile saved")
        reset_main_verification()
        print("Main Verification Reset Done")
        runfile('main_file.py', args = accept_args)
        
        # increment winner_index
        if verify_main_completion():
            print("MATCH COMPLETED AND CONFIRMED")
            winner_index = str(int(winner_index) + 1)
            print("Incrementing Winner Index to %s"%(winner_index))
            save_winner_index(winner_index)
            print("Winner Index saved")
        else:
            break
    # increment mm_batches_index
    # assert mm_batches_index == len(mm_batches) # for new session
    
    
    
    print("Updating match Index.")
    mm_batches_index = int(mm_batches_index) + 1
    print("Saving Match Index.")
    save_mm_batches_index(mm_batches_index)
    
print("Session completed. Sleep time: 200 secs")
runfile('cleaner.py')
time.sleep(200)

if repeat_driver_code:
    print("Restarting Driver Code.")
    runfile('driver_code.py')
    import sys
    sys.exit(0)