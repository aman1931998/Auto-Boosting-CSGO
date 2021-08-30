import multiprocessing
import random
import pandas as pd
import os, sys
from itertools import combinations, permutations
from tqdm import tqdm 
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

from loading_functions import load_usernames, load_account_database
from helper_functions import calculate_matches_to_play
#TODO
#%% Gets account data dict for batch creation.
def get_account_data_for_batch_creator(account_data = None):# , batch_creation_type = "")
    '''
    Gets account data dict for batch creation.
    '''
    if account_data == None:
        account_data = load_account_database()
    account_data_ = {username:{"history": account_data[username]['Matches_History'], 
                               "follow_path": account_data[username]['Matches_History'], 
                               "score":sum([1 if j == 'w' else -1 for j in account_data[username]['Matches_History']]), 
                               "wins": account_data[username]['MM_Wins'], 
                               "mm_rank_opened":True if account_data[username]['MM_Rank'] in ['s1', 's2', 's3', 's4', 'se', 'sem', 'gn1', 'gn2', 'gn3', 'gnm', 'mg1', 'mg2', 'mge', 'dmg', 'le', 'lem', 'smfc', 'ge'] else False, 
                               "last_cooldown_time": account_data[username]['Last_Cooldown_Time']} for username in account_data.keys()
                     }
#    account_data_ = {account_data['Username'][i]:{"history": account_data['Matches_History'][i], "follow_path":account_data['Matches_History'][i], "score":sum([1 if j == 'w' else -1 for j in account_data['Matches_History'][i]]), "wins": account_data['MM_Wins'][i], "mm_rank_opened":False, "last_cooldown_time": account_data['Last_Cooldown_Time'][i]} for i in range(len(account_data['Username']))}
    return account_data_

#%% Creates MM Batches for current Session.
def get_mm_batches(account_data = None, batch_creation_mode = "greedy", shuffle_sub_categories = True, consider_cooldown = False):
    '''
    Creates MM Batches for current Session
    batch_creation_mode: 
        1. greedy: will consider all accounts for creation irrespective of mm_rank opened or not.
        2. no_rank_greedy: will consider all accounts (without mm_rank) for creation 
        3. hierarchical: will consider hierarchy for account creation.
    shuffle_sub_categories: bool, Shuffle score based sub categories, default: True
    consider_cooldown: bool, sort accounts based on cooldown, default: False
    '''
    account_data_keys = list(account_data[list(account_data.keys())[0]].keys())
    if account_data == None or 'Username' in account_data_keys or \
        'Username' in account_data_keys or \
            'MM_Rank' in account_data_keys or \
                'Matches_History' in account_data_keys or \
                    'Last_Cooldown_Time' in account_data_keys or \
                        'Target_PR_Rank' in account_data_keys:
        account_data = get_account_data_for_batch_creator(account_data)
    if batch_creation_mode == 'greedy':
        return get_mm_batches_greedy(account_data = account_data, shuffle_sub_categories = shuffle_sub_categories, consider_cooldown = consider_cooldown)
    elif batch_creation_mode == 'no_rank_greedy':
        return get_mm_batches_no_rank_greedy(account_data = account_data, shuffle_sub_categories = shuffle_sub_categories, consider_cooldown = consider_cooldown)
    elif batch_creation_mode == 'hierarchical':
        print("Hierarchical mode is under development. Please choose another.")
        #return get_mm_batches_hierarchical(account_data)
        sys.exit(0)
        

#%% [Internal Function] Creates MM Batches in greedy mode.
def get_mm_batches_greedy(account_data, shuffle_sub_categories, consider_cooldown):
    '''
    [Internal Function] Creates MM Batches in greedy mode.
    '''
    mm_batches = []
    usernames_daddy = list(account_data.keys())
#    for current_match_index in range(1, 50): #current_match_index = 1  #might change to 1 only: remove for loop # might remove mm_batches and append(?) and return a list.
    usernames = usernames_daddy.copy()
    accounts_rank_opened = [account_data[username]['mm_rank_opened'] for username in usernames]
    print(set(accounts_rank_opened))
    number_of_accounts_with_rank = accounts_rank_opened.count(True)
    print("Rank Opened in: %d"%(number_of_accounts_with_rank))
    number_of_accounts_to_remove = number_of_accounts_with_rank - (number_of_accounts_with_rank % 10)
    print("Removing %d accounts as per criteria."%(number_of_accounts_to_remove))
    follow_path = ["".join(account_data[username]['follow_path']) for username in usernames]
    #account_wins = [account_data[username]['wins'] for username in usernames]
    
    #next_match_outcome = [None] * len(usernames) #TODO
    accounts_remaining = list(range(len(usernames)))
    follow_path_score = [account_data[username]['score'] for username in usernames]
    unique_follow_path_score = list(sorted(list(set(follow_path_score)), reverse = True))
    d = {}
    for score in unique_follow_path_score: #score = unique_follow_path_score[0]
        d[score] = d.get(score, {})
        for index in range(len(usernames)):
            if follow_path_score[index] == score:
                d[score][follow_path[index]] = d[score].get(follow_path[index], []) + [index]

    if shuffle_sub_categories:
        for score in d.keys():
            for pattern in d[score].keys():
                random.shuffle(d[score][pattern])
    
    non_cooldown_datetime_stamp = datetime.now() - timedelta(days = 1)
    lambda_get_last_cooldown_time = lambda x: account_data[usernames[x]]['last_cooldown_time'] if type(account_data[usernames[x]]['last_cooldown_time']) == datetime else non_cooldown_datetime_stamp
    #lambda_get_cooldown_expiry_time = lambda x: max(account_data[usernames[x]]['last_cooldown_time'] + timedelta(hours = 21, minutes = 10) - datetime.now(), timedelta(0)) if type(account_data[usernames[x]]['last_cooldown_time']) == datetime else timedelta(0)
    if consider_cooldown:
        for score in d.keys(): #score = 4
            for pattern in d[score].keys(): #pattern = 'wwww' 
                d[score][pattern] = list(sorted(d[score][pattern], key = lambda_get_last_cooldown_time))
    
    # getting absolutes
    for score in unique_follow_path_score: # score = unique_follow_path_score[1]
        for pattern in sorted(d[score].keys()): #pattern = 'l'
            while len(d[score][pattern]) >= 10:
                current_batch = {"batch_1": [], "batch_2": [], "batch_1_score": [], "batch_2_score": [], 
                                 "batch_1_total": 0,  "batch_2_total": 0, 
                                 "absolute_difference": None,  #TODO
                                 "match_played": "Not Played Yet"}
                batch_1 = [usernames[i] for i in d[score][pattern][0:5]]
                batch_2 = [usernames[i] for i in d[score][pattern][5:10]]
                batch_1_scores = [account_data[usernames[i]]['score'] for i in d[score][pattern][0:5]]
                batch_2_scores = [account_data[usernames[i]]['score'] for i in d[score][pattern][5:10]]
                current_batch['batch_1'] = batch_1
                current_batch['batch_2'] = batch_2
                current_batch['batch_1_score'] = batch_1_scores
                current_batch['batch_2_score'] = batch_2_scores
                current_batch['batch_1_total'] = sum(batch_1_scores)
                current_batch['batch_2_total'] = sum(batch_2_scores)
                current_batch['absolute_difference'] = abs(sum(batch_1_scores) - sum(batch_2_scores))
                current_batch['winner'] = ['batch_1']
                mm_batches.append(current_batch)
                
                for i in d[score][pattern][0:5]:
                    accounts_remaining.remove(i)
                    account_data[usernames[i]]['follow_path'].append('w')
                    account_data[usernames[i]]['score'] += 1
                    account_data[usernames[i]]['wins'] += 1
                    account_data[usernames[i]]['mm_rank_opened'] = True if account_data[usernames[i]]['wins'] >= 10 else False
                for i in d[score][pattern][5:10]:
                    accounts_remaining.remove(i)
                    account_data[usernames[i]]['follow_path'].append('l')
                    account_data[usernames[i]]['score'] -= 1
                d[score][pattern] = d[score][pattern][10:]
    
    scores_dict = {}
    for index in accounts_remaining: #index = accounts_remaining[0]
        score = follow_path_score[index]
        scores_dict[score] = scores_dict.get(score, []) + [index]
    
    if shuffle_sub_categories:
        for score in scores_dict.keys():
            random.shuffle(scores_dict[score])
    
    if consider_cooldown:
        for score in scores_dict.keys(): #score = 4
            scores_dict[score] = list(sorted(scores_dict[score], key = lambda_get_last_cooldown_time))

    number_of_batches = len(accounts_remaining) // 10
    for i in range(number_of_batches): #i = 0
        current_batch = {}
        batch_1 = []
        batch_2 = []
        batch_1_score = []
        batch_2_score = []
        for j in range(5): #j = 0
            def clear_empty_scores(scores_dict):
                new_dict = {}
                for score in scores_dict.keys():
                    if len(scores_dict[score]) == 0: continue
                    new_dict[score] = scores_dict[score]
                return new_dict

            scores_dict = clear_empty_scores(scores_dict)
            max_score_in_dict = max(scores_dict.keys())
            
            get_index_with_max_score = scores_dict[max_score_in_dict].pop()
            accounts_remaining.remove(get_index_with_max_score)
            
            batch_1.append(usernames[get_index_with_max_score])
            batch_1_score.append(account_data[usernames[get_index_with_max_score]]['score'])
            
            account_data[usernames[get_index_with_max_score]]['follow_path'].append('w')
            account_data[usernames[get_index_with_max_score]]['score'] += 1
            account_data[usernames[get_index_with_max_score]]['wins'] += 1
            account_data[usernames[get_index_with_max_score]]['mm_rank_opened'] = True if account_data[usernames[get_index_with_max_score]]['wins'] >= 10 else False
            
            scores_dict = clear_empty_scores(scores_dict)
            max_score_in_dict = max(scores_dict.keys())
            
            get_index_with_max_score = scores_dict[max_score_in_dict].pop()
            accounts_remaining.remove(get_index_with_max_score)

            batch_2.append(usernames[get_index_with_max_score])
            batch_2_score.append(account_data[usernames[get_index_with_max_score]]['score'])
            
            account_data[usernames[get_index_with_max_score]]['follow_path'].append('l')
            account_data[usernames[get_index_with_max_score]]['score'] -= 1
        
        current_batch['batch_1'] = batch_1
        current_batch['batch_2'] = batch_2
        current_batch['batch_1_score'] = batch_1_score
        current_batch['batch_2_score'] = batch_2_score
        current_batch['batch_1_total'] = sum(batch_1_score)
        current_batch['batch_2_total'] = sum(batch_2_score)
        current_batch['absolute_difference'] = abs(sum(batch_1_score) - sum(batch_2_score))
        current_batch['winner'] = ['batch_1']
        current_batch['match_played'] = "Not Played Yet"
        mm_batches.append(current_batch)

    accounts_rank_opened = [account_data[username]['mm_rank_opened'] for username in usernames_daddy]
    number_of_accounts_with_rank = accounts_rank_opened.count(True)
    print("Expected Rank opened in this batch: %d"%(number_of_accounts_with_rank))

    #account_wins = [account_data[username]['wins'] for username in usernames_daddy]
    return mm_batches

#%% [Internal Function] Creates MM Batches in greedy mode while excluding ranked accounts.
def get_mm_batches_no_rank_greedy(account_data, shuffle_sub_categories, consider_cooldown):
    '''
    [Internal Function] Creates MM Batches in greedy mode while excluding ranked accounts.
    '''
    mm_batches = []
    usernames_daddy = list(account_data.keys())
#    for current_match_index in range(1, 50): #current_match_index = 1  #might change to 1 only: remove for loop # might remove mm_batches and append(?) and return a list.
    #usernames = usernames_daddy.copy()
    #username = usernames[0]
    
    #accounts_rank_opened = [account_data[username]['mm_rank_opened'] for username in usernames]
    ranked_accounts = [username for username in usernames_daddy if account_data[username]['mm_rank_opened']]
    if (len(ranked_accounts) > len(usernames_daddy) - 10) and (len(ranked_accounts) < len(usernames_daddy)):
        number_of_accounts_to_use = len(usernames_daddy) - 10
    else:
        number_of_accounts_to_use = len(usernames_daddy) - len(ranked_accounts)
    usernames = usernames_daddy.copy()
    # Removing accs
    for i in range(len(usernames_daddy) - number_of_accounts_to_use):
        usernames.remove(ranked_accounts[i])


    print(ranked_accounts)
    print("Rank Opened in: %d"%(len(ranked_accounts)))
    
    #usernames = [username for username in usernames if not account_data[username]['mm_rank_opened']]
    
    follow_path = ["".join(account_data[username]['follow_path']) for username in usernames]
    #account_wins = [account_data[username]['wins'] for username in usernames]
    
    #next_match_outcome = [None] * len(usernames) #TODO
    accounts_remaining = list(range(len(usernames)))
    follow_path_score = [account_data[username]['score'] for username in usernames]
    unique_follow_path_score = list(sorted(list(set(follow_path_score)), reverse = True))
    d = {}
    for score in unique_follow_path_score: #score = unique_follow_path_score[0]
        d[score] = d.get(score, {})
        for index in range(len(usernames)):
            if follow_path_score[index] == score:
                d[score][follow_path[index]] = d[score].get(follow_path[index], []) + [index]
    
    if shuffle_sub_categories:
        for score in d.keys():
            for pattern in d[score].keys():
                random.shuffle(d[score][pattern])
    
    non_cooldown_datetime_stamp = datetime.now() - timedelta(days = 1)
    lambda_get_last_cooldown_time = lambda x: account_data[usernames[x]]['last_cooldown_time'] if type(account_data[usernames[x]]['last_cooldown_time']) == datetime else non_cooldown_datetime_stamp
    #lambda_get_cooldown_expiry_time = lambda x: max(account_data[usernames[x]]['last_cooldown_time'] + timedelta(hours = 21, minutes = 10) - datetime.now(), timedelta(0)) if type(account_data[usernames[x]]['last_cooldown_time']) == datetime else timedelta(0)
    if consider_cooldown:
        for score in d.keys(): #score = 4
            for pattern in d[score].keys(): #pattern = 'wwww' 
                d[score][pattern] = list(sorted(d[score][pattern], key = lambda_get_last_cooldown_time))

    # getting absolutes
    for score in unique_follow_path_score: # score = unique_follow_path_score[1]
        for pattern in sorted(d[score].keys()): #pattern = 'l'
            while len(d[score][pattern]) >= 10:
                current_batch = {"batch_1": [], "batch_2": [], "batch_1_score": [], "batch_2_score": [], 
                                 "batch_1_total": 0,  "batch_2_total": 0, 
                                 "absolute_difference": None,  #TODO
                                 "match_played": "Not Played Yet"}
                batch_1 = [usernames[i] for i in d[score][pattern][0:5]]
                batch_2 = [usernames[i] for i in d[score][pattern][5:10]]
                batch_1_scores = [account_data[usernames[i]]['score'] for i in d[score][pattern][0:5]]
                batch_2_scores = [account_data[usernames[i]]['score'] for i in d[score][pattern][5:10]]
                current_batch['batch_1'] = batch_1
                current_batch['batch_2'] = batch_2
                current_batch['batch_1_score'] = batch_1_scores
                current_batch['batch_2_score'] = batch_2_scores
                current_batch['batch_1_total'] = sum(batch_1_scores)
                current_batch['batch_2_total'] = sum(batch_2_scores)
                current_batch['absolute_difference'] = abs(sum(batch_1_scores) - sum(batch_2_scores))
                current_batch['winner'] = ['batch_1', 'batch_2', 'batch_1', 'batch_2', 'batch_1', 'batch_2']
                mm_batches.append(current_batch)
                
                for i in d[score][pattern][0:5]:
                    accounts_remaining.remove(i)
                    account_data[usernames[i]]['follow_path'].append('w')
                    account_data[usernames[i]]['score'] += 1
                    account_data[usernames[i]]['wins'] += 1
                    account_data[usernames[i]]['mm_rank_opened'] = True if account_data[usernames[i]]['wins'] >= 10 else False
                for i in d[score][pattern][5:10]:
                    accounts_remaining.remove(i)
                    account_data[usernames[i]]['follow_path'].append('l')
                    account_data[usernames[i]]['score'] -= 1
                d[score][pattern] = d[score][pattern][10:]
    
    scores_dict = {}
    for index in accounts_remaining: #index = accounts_remaining[0]
        score = follow_path_score[index]
        scores_dict[score] = scores_dict.get(score, []) + [index]
    
    if shuffle_sub_categories:
        for score in scores_dict.keys():
            random.shuffle(scores_dict[score])
    
    if consider_cooldown:
        for score in scores_dict.keys(): #score = 4
            scores_dict[score] = list(sorted(scores_dict[score], key = lambda_get_last_cooldown_time))

    number_of_batches = len(accounts_remaining) // 10
    for i in range(number_of_batches): #i = 0
        current_batch = {}
        batch_1 = []
        batch_2 = []
        batch_1_score = []
        batch_2_score = []
        for j in range(5): #j = 0
            def clear_empty_scores(scores_dict):
                new_dict = {}
                for score in scores_dict.keys():
                    if len(scores_dict[score]) == 0: continue
                    new_dict[score] = scores_dict[score]
                return new_dict

            scores_dict = clear_empty_scores(scores_dict)
            max_score_in_dict = max(scores_dict.keys())
            
            get_index_with_max_score = scores_dict[max_score_in_dict].pop()
            accounts_remaining.remove(get_index_with_max_score)
            
            batch_1.append(usernames[get_index_with_max_score])
            batch_1_score.append(account_data[usernames[get_index_with_max_score]]['score'])
            
            account_data[usernames[get_index_with_max_score]]['follow_path'].append('w')
            account_data[usernames[get_index_with_max_score]]['score'] += 1
            account_data[usernames[get_index_with_max_score]]['wins'] += 1
            account_data[usernames[get_index_with_max_score]]['mm_rank_opened'] = True if account_data[usernames[get_index_with_max_score]]['wins'] >= 10 else False
            
            scores_dict = clear_empty_scores(scores_dict)
            max_score_in_dict = max(scores_dict.keys())
            
            get_index_with_max_score = scores_dict[max_score_in_dict].pop()
            accounts_remaining.remove(get_index_with_max_score)

            batch_2.append(usernames[get_index_with_max_score])
            batch_2_score.append(account_data[usernames[get_index_with_max_score]]['score'])
            
            account_data[usernames[get_index_with_max_score]]['follow_path'].append('l')
            account_data[usernames[get_index_with_max_score]]['score'] -= 1
        
        current_batch['batch_1'] = batch_1
        current_batch['batch_2'] = batch_2
        current_batch['batch_1_score'] = batch_1_score
        current_batch['batch_2_score'] = batch_2_score
        current_batch['batch_1_total'] = sum(batch_1_score)
        current_batch['batch_2_total'] = sum(batch_2_score)
        current_batch['absolute_difference'] = abs(sum(batch_1_score) - sum(batch_2_score))
        current_batch['winner'] = ['batch_1', 'batch_2', 'batch_1', 'batch_2', 'batch_1', 'batch_2']
        current_batch['match_played'] = "Not Played Yet"
        mm_batches.append(current_batch)

    accounts_rank_opened = [account_data[username]['mm_rank_opened'] for username in usernames_daddy]
    number_of_accounts_with_rank = accounts_rank_opened.count(True)
    print("Expected Rank opened in this batch: %d"%(number_of_accounts_with_rank))

    #account_wins = [account_data[username]['wins'] for username in usernames_daddy]
    return mm_batches


#%% Creates MM Batches of Ranked Accounts for current Session
def get_mm_batches_ranked(match_count_oriented_usernames_dict, account_data, maintain_on_unequal = 'match_count', target_xp = 5000):
    '''
    match_count_oriented_usernames_dict: dict with keys as match_count(s) | returned by get_number_of_matches_to_play(usernames, account_data)
        6: dict of mm_ranks 
            s1: list of username(s)
            s2: list of username(s)
            .
            .
        4: ...
    account_data: dict with usernames as keys
    maintain_on_unequal: 'match_count' or 'mm_rank'
        'match_count' -> [Called eventually] will wipe out all accounts by creating mm_batch of unequal mm_ranks
        'mm_rank' ->  will prefer mm_ranks and ignores match_count
    target_xp: int (or str), target_xp_to_gain.
    '''
    mm_rank_names = ['ge', 'smfc', 'lem', 'le', 'dmg', 'mge', 'mg2', 'mg1', 'gnm', 'gn3', 'gn2', 'gn1', 'sem', 'se', 's4', 's3', 's2', 's1']
    mm_rank_score = {"s1"   :    1, "s2"   :    2, "s3"   :    3, "s4"   :    4, "se"   :    5, "sem"  :    6, "gn1"  :    7, "gn2"  :    8, "gn3"  :    9, 
                     "gnm"  :   10, "mg1"  :   11, "mg2"  :   12, "mge"  :   13, "dmg"  :   14, "le"   :   15, "lem"  :   16, "smfc" :   17, "ge"   :   18
                     } #, 'unranked': -1
    assert type(match_count_oriented_usernames_dict) == dict
    mm_batches = []
    '''
    # Getting equal batches
    for match_count in list(sorted(list(match_count_oriented_usernames_dict.keys()), reverse = True)): # match_count = list(sorted(list(match_count_oriented_usernames_dict.keys()), reverse = True))[0]
        for mm_rank in mm_rank_names: #mm_rank = mm_rank_names[7]
            random.shuffle(match_count_oriented_usernames_dict[match_count][mm_rank])
            while len(match_count_oriented_usernames_dict[match_count][mm_rank]) >= 10:
                mm_batch = {'batch_1': [],                          # DONE
                            'batch_2': [],                          # DONE
                            'batch_1_score': [],                    # DONE
                            'batch_1_mm_rank': [], 
                            'batch_2_score': [],                    # DONE
                            'batch_2_mm_rank': [], 
                            'batch_1_total': 0,                     # DONE
                            'batch_2_total': 0,                     # DONE
                            'absolute_difference': 0,               # DONE
                            'match_played': 'Not Played Yet',       # DONE
                            'winner': 'batch_1'} # or 'batch_2'     # DONE
                mm_batch_usernames = match_count_oriented_usernames_dict[match_count][mm_rank][:10]
                mm_batch_usernames_sorted = list(sorted(mm_batch_usernames, key = lambda x: account_data[x]['Matches_History'][::-1], reverse = True))
                
                batch_1_last_match_win_count = len([1 for username in mm_batch_usernames_sorted[:5] if account_data[username]['Matches_History'][-1] == 'w'])
                batch_2_last_match_win_count = len([1 for username in mm_batch_usernames_sorted[5:10] if account_data[username]['Matches_History'][-1] == 'w'])
                if batch_1_last_match_win_count > batch_2_last_match_win_count:
                    mm_batch['winner'] = ['batch_2', 'batch_1'] * (match_count//2)
                elif batch_1_last_match_win_count < batch_2_last_match_win_count:
                    mm_batch['winner'] = ['batch_1', 'batch_2'] * (match_count//2)
                elif batch_1_last_match_win_count == batch_2_last_match_win_count:
                    batch_1_llast_match_win_count = len([1 for username in mm_batch_usernames_sorted[:5] if account_data[username]['Matches_History'][-2] == 'w'])
                    batch_2_llast_match_win_count = len([1 for username in mm_batch_usernames_sorted[5:10] if account_data[username]['Matches_History'][-2] == 'w'])
                    if batch_1_llast_match_win_count > batch_2_llast_match_win_count:
                        mm_batch['winner'] = ['batch_2', 'batch_1'] * (match_count//2)
                    elif batch_1_llast_match_win_count < batch_2_llast_match_win_count:
                        mm_batch['winner'] = ['batch_1', 'batch_2'] * (match_count//2)
                    elif batch_1_llast_match_win_count == batch_2_llast_match_win_count:
                        mm_batch['winner'] = random.choice([['batch_2', 'batch_1'] * (match_count//2), ['batch_1', 'batch_2'] * (match_count//2)])
                
                mm_batch['batch_1'] = mm_batch_usernames_sorted[:5]
                mm_batch['batch_2'] = mm_batch_usernames_sorted[5:10]
                mm_batch['batch_1_score'] = [mm_rank_score[account_data[username]['MM_Rank']] for username in mm_batch['batch_1']]
                mm_batch['batch_1_mm_rank'] = [account_data[username]['MM_Rank'] for username in mm_batch['batch_1']]
                mm_batch['batch_2_score'] = [mm_rank_score[account_data[username]['MM_Rank']] for username in mm_batch['batch_2']]
                mm_batch['batch_2_mm_rank'] = [account_data[username]['MM_Rank'] for username in mm_batch['batch_2']]
                mm_batch['batch_1_total'] = sum(mm_batch['batch_1_score'])
                mm_batch['batch_2_total'] = sum(mm_batch['batch_2_score'])
                mm_batch['absolute_difference'] = abs(sum(mm_batch['batch_1_score']) - sum(mm_batch['batch_2_score']))

                match_count_oriented_usernames_dict[match_count][mm_rank] = match_count_oriented_usernames_dict[match_count][mm_rank][10:]
                mm_batches.append(mm_batch)
    
    if maintain_on_unequal == 'mm_rank':
        # Creating dict with mm_rank only [No match_count]
        usernames_with_rank = {rank: [] for rank in mm_rank_names}
        #max_match_count = max(list(sorted(list(match_count_oriented_usernames_dict.keys()), reverse = True)))
        for match_count in list(sorted(list(match_count_oriented_usernames_dict.keys()), reverse = True)): # match_count = list(sorted(list(match_count_oriented_usernames_dict.keys()), reverse = True))[0]
            for mm_rank in match_count_oriented_usernames_dict[match_count].keys(): #mm_rank = 'smfc'
                usernames_with_rank[mm_rank] += match_count_oriented_usernames_dict[match_count][mm_rank]
        
        
        # Getting equal rank batches with unequal matches_to_be_played.
        for mm_rank in list(usernames_with_rank.keys()): #mm_rank = 'smfc'
            while len(usernames_with_rank[mm_rank]) >= 10:
                mm_batch = {'batch_1': [],                          # DONE
                            'batch_2': [],                          # DONE
                            'batch_1_score': [],                    # DONE
                            'batch_1_mm_rank': [], 
                            'batch_2_score': [],                    # DONE
                            'batch_2_mm_rank': [], 
                            'batch_1_total': 0,                     # DONE
                            'batch_2_total': 0,                     # DONE
                            'absolute_difference': 0,               # DONE
                            'match_played': 'Not Played Yet',       # DONE
                            'winner': 'batch_1'} # or 'batch_2'     # DONE
                mm_batch_usernames = usernames_with_rank[mm_rank][:10]
                mm_batch_usernames_sorted = list(sorted(mm_batch_usernames, key = lambda x: account_data[x]['Matches_History'][::-1], reverse = True))
                match_count = max([calculate_matches_to_play(account_data[username]['XP_Gained_For_Next_Rank'], target_xp = target_xp) for username in mm_batch_usernames_sorted])
                batch_1_last_match_win_count = len([1 for username in mm_batch_usernames_sorted[:5] if account_data[username]['Matches_History'][-1] == 'w'])
                batch_2_last_match_win_count = len([1 for username in mm_batch_usernames_sorted[5:10] if account_data[username]['Matches_History'][-1] == 'w'])
                if batch_1_last_match_win_count > batch_2_last_match_win_count:
                    mm_batch['winner'] = ['batch_2', 'batch_1'] * (match_count//2)
                elif batch_1_last_match_win_count < batch_2_last_match_win_count:
                    mm_batch['winner'] = ['batch_1', 'batch_2'] * (match_count//2)
                elif batch_1_last_match_win_count == batch_2_last_match_win_count:
                    batch_1_llast_match_win_count = len([1 for username in mm_batch_usernames_sorted[:5] if account_data[username]['Matches_History'][-2] == 'w'])
                    batch_2_llast_match_win_count = len([1 for username in mm_batch_usernames_sorted[5:10] if account_data[username]['Matches_History'][-2] == 'w'])
                    if batch_1_llast_match_win_count > batch_2_llast_match_win_count:
                        mm_batch['winner'] = ['batch_2', 'batch_1'] * (match_count//2)
                    elif batch_1_llast_match_win_count < batch_2_llast_match_win_count:
                        mm_batch['winner'] = ['batch_1', 'batch_2'] * (match_count//2)
                    elif batch_1_llast_match_win_count == batch_2_llast_match_win_count:
                        mm_batch['winner'] = random.choice([['batch_2', 'batch_1'] * (match_count//2), ['batch_1', 'batch_2'] * (match_count//2)])
                
                mm_batch['batch_1'] = mm_batch_usernames_sorted[:5]
                mm_batch['batch_2'] = mm_batch_usernames_sorted[5:10]
                mm_batch['batch_1_score'] = [mm_rank_score[account_data[username]['MM_Rank']] for username in mm_batch['batch_1']]
                mm_batch['batch_1_mm_rank'] = [account_data[username]['MM_Rank'] for username in mm_batch['batch_1']]
                mm_batch['batch_2_score'] = [mm_rank_score[account_data[username]['MM_Rank']] for username in mm_batch['batch_2']]
                mm_batch['batch_2_mm_rank'] = [account_data[username]['MM_Rank'] for username in mm_batch['batch_2']]
                mm_batch['batch_1_total'] = sum(mm_batch['batch_1_score'])
                mm_batch['batch_2_total'] = sum(mm_batch['batch_2_score'])
                mm_batch['absolute_difference'] = abs(sum(mm_batch['batch_1_score']) - sum(mm_batch['batch_2_score']))
    
                usernames_with_rank[mm_rank] = usernames_with_rank[mm_rank][10:]
                mm_batches.append(mm_batch)
    '''

    #elif maintain_on_unequal == 'match_count':
    # Getting unequal rank batches with same match_count
    usernames_in_order = []
    for match_count in list(sorted(list(match_count_oriented_usernames_dict.keys()), reverse = True)): # match_count = list(sorted(list(match_count_oriented_usernames_dict.keys()), reverse = True))[0]
        usernames_with_rank = match_count_oriented_usernames_dict[match_count]
        for mm_rank in mm_rank_names: #mm_rank = 'ge'
            for user_i in usernames_with_rank[mm_rank]:
                usernames_in_order.append(user_i)
    for index in range(len(usernames_in_order)//10): #index = 0
        usernames_for_this_batch = usernames_in_order[:10]
        batch_1 = [usernames_for_this_batch[i] for i in range(len(usernames_for_this_batch)) if i%2 == 0]
        batch_2 = [usernames_for_this_batch[i] for i in range(len(usernames_for_this_batch)) if i%2 == 1]        
        mm_batch = {'batch_1': [],                          # DONE
                    'batch_2': [],                          # DONE
                    'batch_1_score': [],                    # DONE
                    'batch_2_score': [],                    # DONE
                    'batch_1_total': 0,                     # DONE
                    'batch_2_total': 0,                     # DONE
                    'absolute_difference': 0,               # DONE
                    'match_played': 'Not Played Yet',       # DONE
                    'winner': 'batch_1'} # or 'batch_2'     # DONE
        #mm_batch_usernames = usernames_with_rank[mm_rank][:10]
        mm_batch_usernames_arranged = batch_1 + batch_2 #list(sorted(mm_batch_usernames, key = lambda x: account_data[x]['Matches_History'][::-1], reverse = True))
        match_count = max([calculate_matches_to_play(account_data[username]['XP_Gained_For_Next_Rank'], target_xp = target_xp) for username in mm_batch_usernames_arranged])
        batch_1_last_match_win_count = len([1 for username in mm_batch_usernames_arranged[:5] if account_data[username]['Matches_History'][-1] == 'w'])
        batch_2_last_match_win_count = len([1 for username in mm_batch_usernames_arranged[5:10] if account_data[username]['Matches_History'][-1] == 'w'])
        if batch_1_last_match_win_count > batch_2_last_match_win_count:
            mm_batch['winner'] = ['batch_2', 'batch_1'] * (match_count//2)
        elif batch_1_last_match_win_count < batch_2_last_match_win_count:
            mm_batch['winner'] = ['batch_1', 'batch_2'] * (match_count//2)
        elif batch_1_last_match_win_count == batch_2_last_match_win_count:
            batch_1_llast_match_win_count = len([1 for username in mm_batch_usernames_arranged[:5] if account_data[username]['Matches_History'][-2] == 'w'])
            batch_2_llast_match_win_count = len([1 for username in mm_batch_usernames_arranged[5:10] if account_data[username]['Matches_History'][-2] == 'w'])
            if batch_1_llast_match_win_count > batch_2_llast_match_win_count:
                mm_batch['winner'] = ['batch_2', 'batch_1'] * (match_count//2)
            elif batch_1_llast_match_win_count < batch_2_llast_match_win_count:
                mm_batch['winner'] = ['batch_1', 'batch_2'] * (match_count//2)
            elif batch_1_llast_match_win_count == batch_2_llast_match_win_count:
                mm_batch['winner'] = random.choice([['batch_2', 'batch_1'] * (match_count//2), ['batch_1', 'batch_2'] * (match_count//2)])
        
        mm_batch['batch_1'] = mm_batch_usernames_arranged[:5]
        mm_batch['batch_2'] = mm_batch_usernames_arranged[5:10]
        mm_batch['batch_1_score'] = [mm_rank_score[account_data[username]['MM_Rank']] for username in mm_batch['batch_1']]
        mm_batch['batch_2_score'] = [mm_rank_score[account_data[username]['MM_Rank']] for username in mm_batch['batch_2']]
        mm_batch['batch_1_total'] = sum(mm_batch['batch_1_score'])
        mm_batch['batch_2_total'] = sum(mm_batch['batch_2_score'])
        mm_batch['absolute_difference'] = abs(sum(mm_batch['batch_1_score']) - sum(mm_batch['batch_2_score']))

        usernames_with_rank[mm_rank] = usernames_with_rank[mm_rank][10:]
        mm_batches.append(mm_batch)
        usernames_in_order = usernames_in_order[10:]
    match_count_oriented_usernames_dict = {i:{rank: [] for rank in mm_rank_names} for i in list(match_count_oriented_usernames_dict.keys())}
    
    return mm_batches



#%% Reorders all MM batches based on cooldown, placing non cooldown matches at first.
def reorder_mm_batches(account_data, mm_batches):
    '''
    Reorders all MM batches based on cooldown, placing non cooldown matches at first.
    '''
    batches_cooldown_time_remaining = []
    non_cooldown_datetime_stamp = datetime.now() - timedelta(days = 1)
    lambda_get_last_cooldown_time = lambda x: account_data[x]['Last_Cooldown_Time'] if type(account_data[x]['Last_Cooldown_Time']) == datetime else non_cooldown_datetime_stamp
    #lambda_get_cooldown_expiry_time = lambda x: max(account_data[x]['Last_Cooldown_Time'] + timedelta(hours = 21, minutes = 10) - datetime.now(), timedelta(0)) if type(account_data[x]['Last_Cooldown_Time']) == datetime else timedelta(0)
    for mm_batch in mm_batches: #mm_batch = mm_batches[0]
        batch_cooldown_time_remaining = []
        for i in range(5): #i = 0
            batch_cooldown_time_remaining.append(lambda_get_last_cooldown_time(mm_batch['batch_1'][i]))
            batch_cooldown_time_remaining.append(lambda_get_last_cooldown_time(mm_batch['batch_2'][i]))
        batches_cooldown_time_remaining.append(max(batch_cooldown_time_remaining))
        mm_batch['batch_last_cooldown_time'] = max(batch_cooldown_time_remaining)
    
    mm_batches = list(sorted(mm_batches, key = lambda x: batches_cooldown_time_remaining))
    return mm_batches

#%% WIP
def batches_available_to_run(mm_batches): #TODO
    '''
    Need MM batches with "batch_last_cooldown_time" key
    '''
    approved_mm_batches = []
    for mm_batch in mm_batches: #mm_batch = mm_batches[0]
        if mm_batch['batch_last_cooldown_time']  + timedelta(hours = 21) < datetime.now():
            approved_mm_batches.append(mm_batch)
    return approved_mm_batches
