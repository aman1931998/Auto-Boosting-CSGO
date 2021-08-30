import copy
import time, beepy
import shutil, os, pickle, cv2, psutil, sys
import pyautogui as pg, keyboard as kb
import numpy as np
import pandas as pd
import pyperclip as pc
from PIL import Image, ImageGrab#, ImageOps
from datetime import datetime, timedelta

from project_path import steam_path
from loading_functions import load_account_database, load_usernames
from logging_functions import update_account_data_completed
from mm_batch_creator_functions import get_mm_batches, get_mm_batches_ranked
from helper_functions import clean_network_dns_data, new_week_check, update_new_week_triggers, check_week_trigger, update_account_stats_after_week_change
from major_functions import save_accept_args, power_connection_check
#%% MAIN SETTINGS
from config_variables import repeat_driver_code, continue_with_old
#%% #UNRANKED ACCOUNTS
from config_variables import consider_unranked_accounts, unranked_consideration_threshold, \
    mm_batches_creation_mode, shuffle_sub_categories, consider_cooldown
#%% #RANKED ACCOUNTS
from config_variables import consider_ranked_accounts, ranked_consideration_threshold, maintain_on_unequal, target_xp
#%% Match Settings
from config_variables import after_launch_timeout, launch_timeout, untrusted, map_name, match_output, winner_score
#%% CLEANUP
from config_variables import cleanup_on_running_driver_file, clean_userdata_folder_after_running_batch, clean_network_data_after_running_batch

#%% Load all usernames
usernames = load_usernames()
l = [i.split(".")[0] for i in os.listdir('mm_snippets_username_oriented')]
for i in l:
    usernames.remove(i)

import random
random.shuffle(usernames)

print("Loading Fresh Account Data")
account_data = load_account_database(usernames = usernames, return_type = 'dict', username_oriented = True)

for i in range(len(usernames)//10):
    index_1 = i * 10
    index_2 = (i * 10) + 5
    index_3 = (i * 10) + 10
    print(index_1, index_2, index_3)
    team_1_usernames = usernames[index_1:index_2]
    team_1_steamids = [account_data[username]['SteamID'] for username in team_1_usernames]
    team_1_passwords = [account_data[username]['Password'] for username in team_1_usernames]

    team_2_usernames = usernames[index_2:index_3]
    team_2_steamids = [account_data[username]['SteamID'] for username in team_2_usernames]
    team_2_passwords = [account_data[username]['Password'] for username in team_2_usernames]
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
    
    runfile("main_file_db_fix.py", args = "--clear_old_instance 1 --after_launch_timeout 120 --launch_timeout 1 --untrusted False --map_name nuke --match_output winlose --winner upper --winner_score 16 3 --current_score 0 0")
