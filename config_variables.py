import os
import numpy as np
import pickle
import cv2
from PIL import Image, ImageGrab


#%% MAIN SETTINGS
repeat_driver_code = True #True
continue_with_old = True # True

#%% #UNRANKED ACCOUNTS
consider_unranked_accounts = True
unranked_consideration_threshold = 10

# MM Batch Creation Mode "no_rank_greedy" #or "greedy" or "hierarchical"
mm_batches_creation_mode = "no_rank_greedy"
shuffle_sub_categories = True
consider_cooldown = True

#%% #RANKED ACCOUNTS
consider_ranked_accounts = True
ranked_consideration_threshold = 10
# What to priortize while creating batches on unequal accounts: 'match_count' or 'mm_rank'
maintain_on_unequal = 'match_count'
# Amount of XP to gain: default: 5000
target_xp = 5000

#%% Match Settings
after_launch_timeout = 110 ##Manage!
launch_timeout = 1
untrusted = False
map_name = 'agency'
match_output = 'winlose'
winner_score = [16, 3]

#%% CLEANUP
cleanup_on_running_driver_file = True

# Cleaning userdata folder inside steam/userdata/<steamid>/...
clean_userdata_folder_after_running_batch = True
clean_network_data_after_running_batch = False

#%% Power connection check needed
power_supply_check = False

#%% ingame args
technical_timeout_single_handle = False

#%% MAP TIME SETTINGS
if map_name == 'anubis':
    after_dc_wait_time = 15+7 + (-12)
    after_rc_wait_time = 7+15 # +21?
    max_time_for_loading = 25
if map_name == 'ancient':
    after_dc_wait_time = 15+7 + (-9)
    after_rc_wait_time = 7+15 # +21?
    max_time_for_loading = 25
if map_name == 'agency':
    after_dc_wait_time = 15+7+5 - 10    #15+7 + (-12)
    after_rc_wait_time = 7+15 # +21?
    max_time_for_loading = 25    
if map_name == 'vertigo':
    after_dc_wait_time = 15+7+5 - 11    #15+7 + (-12)
    after_rc_wait_time = 7+15 # +21?
    max_time_for_loading = 25    
if map_name == 'office':
    after_dc_wait_time = 15+7+5 - 10    #15+7 + (-12)
    after_rc_wait_time = 7+15 # +21?
    max_time_for_loading = 25    
if map_name == 'overpass':
    after_dc_wait_time = 15+7+5 - 10    #15+7 + (-12)
    after_rc_wait_time = 7+15 # +21?
    max_time_for_loading = 25    

#%%
safe_pixel_x, safe_pixel_y = 1920, 1080