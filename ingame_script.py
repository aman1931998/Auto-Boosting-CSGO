import sys
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
import argparse

from positions import *
from functions import *
from major_functions import *
from project_path import steam_path

#%% additional args
from config_variables import technical_timeout_single_handle, power_supply_check

#%%
parser = argparse.ArgumentParser()
parser.add_argument("--map_name", type = str, help = "Select the map name", default = "anubis")
parser.add_argument("--match_output", type = str, help = "Match outcome", default = "winlose")
parser.add_argument("--winner", type = str, help = "Winner batch", default = "lower")
parser.add_argument("--winner_score", type = str, nargs = 2, help = "Set the score for the match w.r.t. winning lobby", default = "16 3")
parser.add_argument("--current_score", type = str, nargs = 2, help = "Current Score", default = "0 0")

args = parser.parse_args()

print(args)
#%% Config
map_name = str(args.map_name).lower()
match_output = str(args.match_output).lower()
winner = str(args.winner).lower()

try:
    winner_score = list(map(int, str(args.winner_score).split()))
except:
    winner_score = list(map(int, args.winner_score))
try:
    current_score = list(map(int, str(args.current_score).split()))
except:
    current_score = list(map(int, args.current_score))


#%%
ingame_win_checker_file = [np.load(os.path.join('warning_snippets', 'ingame_ct_win_icon_right.npy')), 
                           np.load(os.path.join('warning_snippets', 'ingame_t_win_icon_right.npy'))]


score = [winner_score[0] - current_score[0], winner_score[1] - current_score[1]]
failsafe = False
#%% MAP settings
from config_variables import after_dc_wait_time, after_rc_wait_time, max_time_for_loading
#%%
upper_icon, lower_icon = None, None

if winner == "upper":
    upper_count, lower_count = current_score[0], current_score[1]
    upper_max_count, lower_max_count = winner_score[0], winner_score[1]
elif winner == "lower":
    lower_count, upper_count = current_score[0], current_score[1]
    lower_max_count, upper_max_count = winner_score[0], winner_score[1]

total_rounds = sum(winner_score)
current_round = sum(current_score) + 1

upper_batch = [CSGO_UPPER_POS_X, CSGO_UPPER_POS_Y, 'upper', lower_icon, lower_count, lower_max_count] 
lower_batch = [CSGO_LOWER_POS_X, CSGO_LOWER_POS_Y, 'lower', upper_icon, upper_count, upper_max_count]

#%%
restart_if_panel_not_responding()
# avast_popup_output = avast_popup(test_image = None, checker_image = avast_popup_checker_image, cancel_match_ = True)
# if avast_popup_output:
#     failsafe = True
'''
### add a way to not complete at 16 early.
'''
print("Match Output: %d-%d"%(upper_max_count, lower_max_count))
print("Current Score: %d-%d"%(upper_count, lower_count))



for batch in [upper_batch, lower_batch]: #batch = upper_batch.copy()
    if failsafe:
        break
    
    POS_X, POS_Y = batch[:2]
    
    # if batch[4] in [14, 15]:
    #     continue
    
    if batch[5] == batch[4]:
        continue
    # if (batch[5] - batch[4])%2 == 1:
    #     #print("Disconnect and reconnect %s batch."%(batch[2]))
    after_dc_wait = 0

    print("Score: %d-%d"%(lower_batch[4], upper_batch[4]))
    print("\nCurrent Round: %d"%(current_round))

    if power_supply_check:
        power_connection_check()
    restart_if_panel_not_responding()
    
    print("Disconnecting %s batch."%(batch[2]))
    error_outputs = disconnect_batch(batch = batch[2], disconnect_last_panel_only = technical_timeout_single_handle)
    if error_outputs != []:
        if len(error_outputs) == 5:
            cancel_match()
            failsafe = True
        else:
            reconnect_error_panels(batch = batch[2], panels = error_outputs)
    
    print("Score: %d-%d"%(lower_batch[4], upper_batch[4]))
    print("\nCurrent Round: %d"%(current_round))
    if power_supply_check:
        power_connection_check()

    restart_if_panel_not_responding()

    print("Reconnecting %s batch"%(batch[2]))
    # TODO add function to check for error snippets.
    error_outputs = reconnect_batch(batch = batch[2], reconnect_last_panel_only = technical_timeout_single_handle)
    if error_outputs != []:
        if len(error_outputs) == 5:
            cancel_match()
            failsafe = True
        else:
            reconnect_error_panels(batch = batch[2], panels = error_outputs)

    # function to check for map loading.
    reconnection_output = map_loading_check_wrapper(map_name = map_name, method = batch[2], max_time = max_time_for_loading)
    if type(reconnection_output) == list and not current_round == total_rounds:
        cancel_match()
        failsafe = True

    # reconnection_output = map_loading_check_wrapper(map_name = map_name, method = batch[2], max_time = max_time_for_loading)
    # if type(reconnection_output) == list and not current_round == total_rounds:
    #     if len(reconnection_output) == 0:
    #         cancel_match()
    #         failsafe = True
    #     else:
    #         reconnect_error_panels(batch = batch[2], panels = reconnection_output)
    


    
    batch[4]+=1
    time.sleep(after_rc_wait_time)
    current_round+=1

for i in range(16): #i = 0                 #needed??
    print("......")
    print("Outer loop: %d"%(i))
    print("......")
    if failsafe:
        break                                
    while current_round <= total_rounds - 2:
        if failsafe:
            break
        for batch in [upper_batch, lower_batch]: #batch = upper_batch.copy()
            
            if failsafe:
                break
            
            after_dc_wait = 1
            # [:2] -> POS_X, POS_Y
            # [2]  -> batch_name
            # [3]  -> batch_icon
            # [4]  -> batch_count
            # [5]  -> batch_max_count
            POS_X, POS_Y = batch[:2]
            
            # if batch[5] - batch[4] == 4:
            #     if current_round <= 6:
            #         continue
            
            if batch[5] - batch[4] == 2:
                if current_round <= 14: #16: #14?
                    continue
            
            if batch[4] in [14, 15]:
                continue
            
            if batch[5] == batch[4]:
                continue
            if (batch[5] - batch[4])%2 == 1:
                #print("Disconnect and reconnect %s batch."%(batch[2]))
                after_dc_wait = 0
            
            if current_round == 16:
                print("HALFTIME. waiting 8 seconds")
                time.sleep(8)
                
            restart_if_panel_not_responding()
            if power_supply_check:
                power_connection_check()
            print("Disconnecting %s batch."%(batch[2]))
            error_outputs = disconnect_batch(batch = batch[2])
            
            if error_outputs != []:
                if len(error_outputs) == 5:
                    cancel_match()
                    failsafe = True
                else:
                    reconnect_error_panels(batch = batch[2], panels = error_outputs)
            
            if after_dc_wait == 1:
            #     round_completion_output = check_round_completion_wrapper(checker_images = ingame_win_checker_file)
            #     if round_completion_output == False:
            #         print("Error while confirming round %d completion."%(current_round))
            #         failsafe = True
                # else:
                print("Round %d completed!"%(current_round))
            
            if after_dc_wait == 1:
                batch[4]+=1
                current_round+=1
                print("Score: %d-%d"%(lower_batch[4], upper_batch[4]))
                print("\nCurrent Round: %d"%(current_round))
                print("Waiting for next round to start")
                time.sleep(after_dc_wait_time)
            
            if current_round == 16:
                print("HALFTIME. waiting 8 seconds")
                time.sleep(8)
            
            restart_if_panel_not_responding()
            if power_supply_check:
                power_connection_check()
            print("Reconnecting %s batch."%(batch[2]))
            # TODO add function to check for error snippets.
            error_outputs = reconnect_batch(batch = batch[2])
            
            if error_outputs != []:
                if len(error_outputs) == 5:
                    cancel_match()
                    failsafe = True
                else:
                    reconnect_error_panels(batch = batch[2], panels = error_outputs)

            # function to check for map loading.
            reconnection_output = map_loading_check_wrapper(map_name = map_name, method = batch[2], max_time = max_time_for_loading)
            if type(reconnection_output) == list:
                print("Error confirming map loadingg.")
                cancel_match()
                failsafe = True
            else:
                print("Reconnection Successful and map loading...")

            if after_dc_wait == 1:
                # round_completion_output = check_round_completion_wrapper(checker_images = ingame_win_checker_file)
                # if round_completion_output == False:
                #     print("Error while confirming round %d completion."%(current_round))
                #     failsafe = True
                # else:
                    print("Round %d completed!"%(current_round))

            batch[4]+=1
            current_round+=1

            print("Score: %d-%d"%(lower_batch[4], upper_batch[4]))
            print("\nCurrent Round: %d"%(current_round))
            print("Waiting for round to start.")
            time.sleep(after_rc_wait_time)

#%%

for batch in [upper_batch, lower_batch]: #batch = upper_batch.copy()
    
    if failsafe:
        break
    
    after_dc_wait = 1
    # [:2] -> POS_X, POS_Y
    # [2]  -> batch_name
    # [3]  -> batch_icon
    # [4]  -> batch_count
    # [5]  -> batch_max_count
    POS_X, POS_Y = batch[:2]
    
    # if batch[4] in [14, 15]:
    #     continue
    
    if batch[5] == batch[4]:
        continue
    if (batch[5] - batch[4])%2 == 1:
        #print("Disconnect and reconnect %s batch."%(batch[2]))
        after_dc_wait = 0

    if current_round == 15 + 1:
        print("HALFTIME. waiting 8 seconds")
        time.sleep(8)
    
    print("Score: %d-%d"%(lower_batch[4], upper_batch[4]))
    print("\nCurrent Round: %d"%(current_round))
    
    restart_if_panel_not_responding()
    if power_supply_check:
        power_connection_check()

    print("Disconnecting %s batch."%(batch[2]))
    error_outputs = disconnect_batch(batch = batch[2])
    if error_outputs != []:
        if len(error_outputs) == 5:
            cancel_match()
            failsafe = True
        else:
            reconnect_error_panels(batch = batch[2], panels = error_outputs)
    
    if after_dc_wait == 1:
        current_round+=1
        print("Waiting for next round to start")
        time.sleep(after_dc_wait_time)
        batch[4]+=1
    
    if current_round == 16:
        print("HALFTIME. waiting 8 seconds")
        time.sleep(8)
    
    print("Score: %d-%d"%(lower_batch[4], upper_batch[4]))
    print("\nCurrent Round: %d"%(current_round))
    
    restart_if_panel_not_responding()
    if power_supply_check:
        power_connection_check()

    print("Reconnecting %s batch"%(batch[2]))
    # TODO add function to check for error snippets.
    error_outputs = reconnect_batch(batch = batch[2])

    if error_outputs != []:
        if len(error_outputs) == 5:
            cancel_match()
            failsafe = True
        else:
            reconnect_error_panels(batch = batch[2], panels = error_outputs)

    # function to check for map loading.
    reconnection_output = map_loading_check_wrapper(map_name = map_name, method = batch[2], max_time = max_time_for_loading)
    if type(reconnection_output) == list and not current_round == total_rounds:
        cancel_match()
        failsafe = True
    
    batch[4]+=1
    time.sleep(after_rc_wait_time)
    current_round+=1



print("Final Score: %d-%d"%(lower_batch[4], upper_batch[4]))




if not failsafe:
    from dynamic_data_functions import toggle_match_completion
    
    toggle_match_completion()



















