"""
PART 2 of RANK CHECK
Script to update the database with new rank snippet definitons
Needs rank_update_functions, account_loading_functions, account_saving_functions
"""


from tqdm import tqdm
import pickle
import shutil
import os
import cv2
from PIL import Image, ImageGrab
import numpy as np
import sys

#%%
from rank_update_functions import get_rank_count, load_to_ignore_lists, load_conversion_tables
from account_loading_functions import load_usernames, load_full_account_database, load_match_history_database, load_mm_mismatch_history_database
from account_saving_functions import save_match_history_database, save_mm_mismatch_history_database, save_account_database


#%%
rank_replace_path = os.path.join('images', 'replace_dict')
open_database_path = os.path.join('database', 'open_database')
match_history_path = os.path.join('database', 'matches_data')
#mm_mismatch_history_path = os.path.join('database', 'mm_mismatch_data')


#%% Loading databases
mm_conversion_table, pr_conversion_table = load_conversion_tables(rank_replace_path = os.path.join('images', 'replace_dict'), order = ['mm', 'pr'])
# mm_to_ignore, pr_to_ignore = load_to_ignore_lists(rank_replace_path = os.path.join('images', 'replace_dict'), order = ['mm', 'pr'])
match_history = load_match_history_database()
account_database = load_full_account_database()
#mm_mismatch_history = load_mm_mismatch_history_database()

#%% Loading existing reports
try:
    with open(os.path.join('database', 'rank_reports', 'account_data_reports.pkl'), 'rb') as file:
        account_data_reports = pickle.load(file)
except:
    account_data_reports = {}
try:
    with open(os.path.join('database', 'rank_reports', 'match_data_reports.pkl'), 'rb') as file:
        match_data_reports = pickle.load(file)
except:
    match_data_reports = {}

#%%
# account_data_reports = {}
for username in tqdm(account_database.keys()): #username, data = list(account_database.keys())[0], account_database[list(account_database.keys())[0]]
    # username = 'cellar2dance5'
    # data = account_database[username]
    print("Selected Username:: %s"%(username))
    account_data_reports[username] = {}
    
    # cooldown_info -> NO CHANGE NEEDED
    account_data_reports[username]['cooldown_info'] = {}    
    
    # info ->
    account_data_reports[username]['info'] = {}
    
    info_mm_rank = account_database[username]['info']['MM_Rank']
    if str(info_mm_rank) + '.png' in mm_conversion_table.keys():
        info_mm_rank_new = mm_conversion_table[str(info_mm_rank) + '.png']
        print("Changing info/MM_Rank from %s to %s"%(info_mm_rank, info_mm_rank_new))
        account_data_reports[username]['info']['MM_Rank'] = {"old": info_mm_rank, 
                                                             "new": info_mm_rank_new}
        account_database[username]['info']['MM_Rank'] = info_mm_rank_new

    info_pr_rank = account_database[username]['info']['PR_Rank']
    if str(info_pr_rank) + '.png' in pr_conversion_table.keys():
        info_pr_rank_new = pr_conversion_table[str(info_pr_rank) + '.png']
        print("Changing info/PR_Rank from %s to %s"%(info_pr_rank, info_pr_rank_new))
        account_data_reports[username]['info']['PR_Rank'] = {"old": info_pr_rank, 
                                                             "new": info_pr_rank_new}
        account_database[username]['info']['PR_Rank'] = info_pr_rank_new
    
    # match_history -> NO CHANGES NEEDED
    account_data_reports[username]['match_history'] = {}
    
    # mm_rank_info -> NO CHANGES NEEDED
    account_data_reports[username]['mm_rank_info'] = {}
    
    mm_rank_info_mm_rank = account_database[username]['mm_rank_info']['MM_Rank']
    if str(mm_rank_info_mm_rank) + '.png' in mm_conversion_table.keys():
        mm_rank_info_mm_rank_new = mm_conversion_table[str(mm_rank_info_mm_rank) + '.png']
        print("Changing mm_rank_info/MM_Rank from %s to %s"%(mm_rank_info_mm_rank, mm_rank_info_mm_rank_new))
        account_data_reports[username]['mm_rank_info']['MM_Rank'] = {"old": mm_rank_info_mm_rank, 
                                                                     "new": mm_rank_info_mm_rank_new}
        account_database[username]['mm_rank_info']['MM_Rank'] = mm_rank_info_mm_rank_new
    
    mm_rank_info_mm_rank_history = account_database[username]['mm_rank_info']['MM_Rank_History']
    account_data_reports[username]['mm_rank_info']['MM_Rank_History'] = {}
    for index, mm_rank_info_mm_rank_history_mm_rank in mm_rank_info_mm_rank_history.items(): #index, mm_rank_info_mm_rank_history_mm_rank = list(mm_rank_info_mm_rank_history.items())[6]
        if str(mm_rank_info_mm_rank_history_mm_rank) + '.png' in mm_conversion_table.keys():
            mm_rank_info_mm_rank_history_mm_rank_new = mm_conversion_table[str(mm_rank_info_mm_rank_history_mm_rank) + '.png']
            print("Changing mm_rank_info/MM_Rank_History/%s from %s to %s"%(str(index), mm_rank_info_mm_rank_history_mm_rank, mm_rank_info_mm_rank_history_mm_rank_new))
            account_data_reports[username]['mm_rank_info']['MM_Rank_History'][index] = {"old": mm_rank_info_mm_rank_history_mm_rank, 
                                                                                      "new": mm_rank_info_mm_rank_history_mm_rank_new}
            account_database[username]['mm_rank_info']['MM_Rank_History'][index] = mm_rank_info_mm_rank_history_mm_rank_new
    
    mm_rank_info_rank_opened = account_database[username]['mm_rank_info']['Rank_Opened']
    if str(mm_rank_info_rank_opened) + '.png' in mm_conversion_table.keys():
        mm_rank_info_rank_opened_new = mm_conversion_table[str(mm_rank_info_rank_opened) + '.png']
        print("Changing mm_rank_info/Rank_Opened from %s to %s"%(mm_rank_info_rank_opened, mm_rank_info_rank_opened_new))
        account_data_reports[username]['mm_rank_info']['Rank_Opened'] = {"old": mm_rank_info_rank_opened, 
                                                                         "new": mm_rank_info_rank_opened_new}
        account_database[username]['mm_rank_info']['Rank_Opened'] = mm_rank_info_rank_opened_new
    
    # pr_rank_info ->
    account_data_reports[username]['pr_rank_info'] = {}
    
    pr_rank_info_pr_rank = account_database[username]['pr_rank_info']['PR_Rank']
    if str(pr_rank_info_pr_rank) + '.png' in pr_conversion_table.keys():
        pr_rank_info_pr_rank_new = pr_conversion_table[str(pr_rank_info_pr_rank) + '.png']
        print("Changing pr_rank_info/PR_Rank from %s to %s"%(pr_rank_info_pr_rank, pr_rank_info_pr_rank_new))
        account_data_reports[username]['pr_rank_info']['PR_Rank'] = {"old": pr_rank_info_pr_rank, 
                                                                     "new": pr_rank_info_pr_rank_new}
        account_database[username]['pr_rank_info']['PR_Rank'] = pr_rank_info_pr_rank_new
        
    # weekly_info -> NO CHANGE NEEDED
    

#%%
# match_data_reports = {}
for matchID in tqdm(match_history.keys()): #matchID = list(match_history.keys())[0]:
    # matchID = ''
    # match_details = match_history[matchID]
    match_data_reports[matchID] = {}
    match_data_reports[matchID]['Team_1'] = {}
    match_data_reports[matchID]['Team_2'] = {}
    for team in ['Team_1', 'Team_2']: #team = 'Team_1'
        match_data_reports[matchID][team]['Players'] = {}
        for player in match_history[matchID][team]['Players'].keys(): #player = 'Player_1'
            match_data_reports[matchID][team]['Players'][player] = {}
            mm_rank = match_history[matchID][team]['Players'][player]['MM_Rank']
            mm_rank_update = match_history[matchID][team]['Players'][player]['MM_Rank_Update']
            pr_rank = match_history[matchID][team]['Players'][player]['PR_Rank']
            pr_rank_update = match_history[matchID][team]['Players'][player]['PR_Rank_Update']
            
            if str(mm_rank) + '.png' in mm_conversion_table.keys():
                mm_rank_new = mm_conversion_table[str(mm_rank) + '.png']
                print("Changing %s/MM_Rank from %s to %s"%(matchID, mm_rank, mm_rank_new))
                match_data_reports[matchID][team]['Players'][player]['MM_Rank'] = {"old": mm_rank, 
                                                                                   "new": mm_rank_new}
                match_history[matchID][team]['Players'][player]['MM_Rank'] = mm_rank_new

            if str(mm_rank_update) + '.png' in mm_conversion_table.keys():
                mm_rank_update_new = mm_conversion_table[str(mm_rank_update) + '.png']
                print("Changing %s/MM_Rank_Update from %s to %s"%(matchID, mm_rank_update, mm_rank_update_new))
                match_data_reports[matchID][team]['Players'][player]['MM_Rank_Update'] = {"old": mm_rank_update, 
                                                                                          "new": mm_rank_update_new}
                match_history[matchID][team]['Players'][player]['MM_Rank_Update'] = mm_rank_update_new

            if str(pr_rank) + '.png' in pr_conversion_table.keys():
                pr_rank_new = pr_conversion_table[str(pr_rank) + '.png']
                print("Changing %s/PR_Rank from %s to %s"%(matchID, pr_rank, pr_rank_new))
                match_data_reports[matchID][team]['Players'][player]['PR_Rank'] = {"old": pr_rank, 
                                                                                   "new": pr_rank_new}
                match_history[matchID][team]['Players'][player]['PR_Rank'] = pr_rank_new

            if str(pr_rank_update) + '.png' in pr_conversion_table.keys():
                pr_rank_update_new = pr_conversion_table[str(pr_rank_update) + '.png']
                print("Changing %s/PR_Rank_Update from %s to %s"%(matchID, pr_rank_update, pr_rank_update_new))
                match_data_reports[matchID][team]['Players'][player]['PR_Rank_Update'] = {"old": pr_rank_update, 
                                                                                          "new": pr_rank_update_new}
                match_history[matchID][team]['Players'][player]['PR_Rank_Update'] = pr_rank_update_new
            



#%% Saving databases
save_match_history_database(match_history, match_history_path)
save_account_database(account_database, open_database_path)

with open(os.path.join('database', 'rank_reports', 'account_data_reports.pkl'), 'wb') as file:
    pickle.dump(account_data_reports, file)
with open(os.path.join('database', 'rank_reports', 'match_data_reports.pkl'), 'wb') as file:
    pickle.dump(match_data_reports, file)

#%% Remove useless images
# cant_remove_mm_snippets, cant_remove_pr_snippets = [], []
# for image_name in tqdm(pr_to_ignore): #image_name = pr_to_ignore[0]
#     target_path = os.path.join('images', 'pr_ranks', image_name)
#     target_path_numpy = os.path.join('images', 'pr_ranks', 'numpy_objects', image_name.split('.')[0] + '.npy')
#     try:
#         os.remove(target_path)
#     except:
#         print("Unable to remove pr_ranks/%s."%(image_name))
#         cant_remove_pr_snippets.append(image_name)
#     try:
#         os.remove(target_path_numpy)
#     except:
#         print("Unable to remove pr_ranks/numpy_objects/%s."%(image_name.split('.')[0] + '.npy'))
#         cant_remove_pr_snippets.append(image_name.split('.')[0] + '.npy')

# for image_name in tqdm(mm_to_ignore): #image_name = mm_to_ignore[0]
#     target_path = os.path.join('images', 'mm_ranks', image_name)
#     target_path_numpy = os.path.join('images', 'mm_ranks', 'numpy_objects', image_name.split('.')[0] + '.npy')
#     try:
#         os.remove(target_path)
#     except:
#         print("Unable to remove mm_ranks/%s."%(image_name))
#         cant_remove_mm_snippets.append(image_name)
#     try:
#         os.remove(target_path_numpy)
#     except:
#         print("Unable to remove mm_ranks/numpy_objects/%s."%(image_name.split('.')[0] + '.npy'))
#         cant_remove_mm_snippets.append(image_name.split('.')[0] + '.npy')


#%% Changing rank names
try:
    with open(os.path.join('images', 'replace_dict', 'pr_snippet_updated.pkl'), 'rb') as file:
        pr_snippet_updated = pickle.load(file)
except:
    print("pr_snippet_updated ot Found")
    pr_snippet_updated = []
try:
    with open(os.path.join('images', 'replace_dict', 'mm_snippet_updated.pkl'), 'rb') as file:
        mm_snippet_updated = pickle.load(file)
except:
    print("mm_snippet_updated Not Found")
    mm_snippet_updated = []


for image_name, rank in tqdm(mm_conversion_table.items()): #image_name, rank = list(mm_conversion_table.items())[0]
    if image_name in mm_snippet_updated:
        print("Skipping. Already done.")
        continue
    try:
        source_path = os.path.join('images', 'mm_ranks', image_name)
        source_path_numpy = os.path.join('images', 'mm_ranks', 'numpy_objects', image_name.split('.')[0] + '.npy')
        rank = str(rank) + "_" + str(get_rank_count(base_path = os.path.join('images', 'mm_ranks'), new_rank = rank) + 1) + ".png"
        target_path = os.path.join('images', 'mm_ranks', rank)
        target_path_numpy = os.path.join('images', 'mm_ranks', 'numpy_objects', rank.split('.')[0] + '.npy')
        # print(rank)
        shutil.move(source_path, target_path)
        shutil.move(source_path_numpy, target_path_numpy)
    except:
        pass
        # print("mm_ranks/%s"%(image_name))

for image_name, rank in tqdm(pr_conversion_table.items()): #image_name, rank = list(mm_conversion_table.items())[0]
    try:
        if image_name in pr_snippet_updated:
            print("Skipping. Already done.")
            continue
        source_path = os.path.join('images', 'pr_ranks', image_name)
        source_path_numpy = os.path.join('images', 'pr_ranks', 'numpy_objects', image_name.split('.')[0] + '.npy')
        rank = str(rank) + "_" + str(get_rank_count(base_path = os.path.join('images', 'pr_ranks'), new_rank = rank) + 1) + ".png"
        target_path = os.path.join('images', 'pr_ranks', rank)
        target_path_numpy = os.path.join('images', 'pr_ranks', 'numpy_objects', rank.split('.')[0] + '.npy')
        # print(rank)
        shutil.move(source_path, target_path)
        shutil.move(source_path_numpy, target_path_numpy)
    except:
        #print("pr_ranks/%s"%(image_name))
        pass

with open(os.path.join('images', 'replace_dict', 'pr_snippet_updated.pkl'), 'wb') as file:
    pickle.dump(pr_snippet_updated, file)
with open(os.path.join('images', 'replace_dict', 'mm_snippet_updated.pkl'), 'wb') as file:
    pickle.dump(mm_snippet_updated, file)



#%% Remove useless images
print("Removing unknown_*.png and unknown_*.npy images.")
mm_to_ignore = os.listdir(os.path.join('images', 'mm_ranks'))
mm_to_ignore = [i for i in mm_to_ignore if 'unknown' in i]
pr_to_ignore = os.listdir(os.path.join('images', 'pr_ranks'))
pr_to_ignore = [i for i in pr_to_ignore if 'unknown' in i]

for image_name in tqdm(pr_to_ignore): #image_name = pr_to_ignore[0]
    target_path = os.path.join('images', 'pr_ranks', image_name)
    target_path_numpy = os.path.join('images', 'pr_ranks', 'numpy_objects', image_name.split('.')[0] + '.npy')
    try:
        os.remove(target_path)
    except:
        #print("Unable to remove pr_ranks/%s."%(image_name))
        pass
        # cant_remove_pr_snippets.append(image_name)
    try:
        os.remove(target_path_numpy)
    except:
        print("Unable to remove pr_ranks/numpy_objects/%s."%(image_name.split('.')[0] + '.npy'))
        # cant_remove_pr_snippets.append(image_name.split('.')[0] + '.npy')

for image_name in tqdm(mm_to_ignore): #image_name = mm_to_ignore[0]
    target_path = os.path.join('images', 'mm_ranks', image_name)
    target_path_numpy = os.path.join('images', 'mm_ranks', 'numpy_objects', image_name.split('.')[0] + '.npy')
    try:
        os.remove(target_path)
    except:
        print("Unable to remove mm_ranks/%s."%(image_name))
        # cant_remove_mm_snippets.append(image_name)
    try:
        os.remove(target_path_numpy)
    except:
        print("Unable to remove mm_ranks/numpy_objects/%s."%(image_name.split('.')[0] + '.npy'))
        # cant_remove_mm_snippets.append(image_name.split('.')[0] + '.npy')





print("SUCCESSFUL!")




