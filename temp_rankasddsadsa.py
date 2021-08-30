# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 07:50:32 2021

@author: Aman Agarwal
"""

import os
from PIL import Image, ImageGrab
from account_loading_functions import load_full_account_database
from account_saving_functions import save_account_database

account_database = load_full_account_database()

usernames = os.listdir(os.path.join('mm_snippets_username_oriented'))

d ={}

# for username in usernames:
#     image = Image.open(os.path.join('mm_snippets_username_oriented', username)).convert("RGB")
#     for i in range(len(d)):
#         if np.all(np.array(image) == np.array(d[i]))

open_database_path = os.path.join('database', 'open_database')





for username in usernames:
    print(username)
    display(Image.open(os.path.join('mm_snippets_username_oriented', username)).convert("RGB"))
    x = input("Enter Rank: ")
    if x == "":
        x = 'unranked'
    if x == '0':
        continue
    # elif x == 'u' or x == 'U':
    #     x = 'unranked'
    d[username] = x

for username in d.keys(): #username = 'zephyr36settle154.png'
    username = username.split('.')[0]
    account_database[username]['info']['MM_Rank'] = d[username + ".png"]
    account_database[username]['mm_rank_info']['MM_Rank'] = d[username + ".png"]


save_account_database(account_database, open_database_path)
