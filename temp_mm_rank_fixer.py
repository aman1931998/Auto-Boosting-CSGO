# -*- coding: utf-8 -*-
"""
Created on Tue May  4 12:10:20 2021

@author: Devansh Thapliyal
"""
import os
from PIL import Image
from account_loading_functions import load_full_account_database
from account_saving_functions import save_account_database
import numpy as np

accepted_mm_ranks = ['s1', 's2', 's3', 's4', 'se', 'sem', 
                     'gn1', 'gn2', 'gn3', 'gnm', 'mg1', 'mg2', 'mge', 
                     'dmg', 'le', 'lem', 'smfc', 'ge'] + ['unranked', 'expired']

account_database = load_full_account_database()

usernames = list(account_database.keys())

d = {}
for username in account_database.keys():
    mm_rank_snippet = Image.open(os.path.join('mm_snippets_username_oriented', username + '.png')).convert("RGB")
    d[username] = np.array(mm_rank_snippet)[:, :, :3]

df = []
for username in usernames: #username = usernames[1]
    found = False
    for data in df:
        if np.all(data["snippet"] == d[username]):
            found = True
            data['username'].append(username)
    if found == False:
        df.append({"username": [username], "snippet": d[username]})

for data in df:
    u_list = data['username']
    print(*u_list)
    for username in u_list:
        display(Image.fromarray(d[username]))
    rank = input("Enter rank")
    # if rank == "": rank = 'gn3'
    if rank == "":
        continue
    data['rank'] = rank
    
rank_data = {}
for data in df:
    for username in data['username']:
        try:
            rank_data[username] = data['rank']
        except:
            pass


for username in rank_data.keys():
    account_database[username]['mm_rank_info']['MM_Rank'] = rank_data[username]
    account_database[username]['info']['MM_Rank'] = rank_data[username]
    account_database[username]['mm_rank_info']['MM_Rank_History'][str(len(account_database[username]['mm_rank_info']['MM_Rank_History']))] = rank_data[username]


# count = 0
# for username in account_database.keys(): #username = 'KatheBender'
#     count += 1
#     print("Current Index: %d"%(count))
#     while True:
#         try:
#             print("Current Username: %s"%(username))
#             mm_rank_snippet = Image.open(os.path.join('mm_snippets_username_oriented', username + '.png')).convert("RGB")
#             display(mm_rank_snippet)
#             new_mmr = input("Enter rank for this snippet: ").lower()
#             if new_mmr == 'u': new_mmr = 'unranked'
#             if new_mmr == 'e': new_mmr = 'expired'
#             assert new_mmr in accepted_mm_ranks
#             account_database[username]['mm_rank_info']['MM_Rank'] = new_mmr
#             account_database[username]['info']['MM_Rank'] = new_mmr
#             break
#         except:
#             print()
#             pass






save_account_database(account_database, os.path.join('database', 'open_database'))


