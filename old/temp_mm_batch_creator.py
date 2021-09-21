import multiprocessing
import random
import pandas as pd
import os
from itertools import combinations, permutations
from tqdm import tqdm 

data = pd.read_excel(os.path.join('database', 'batch_2_follow_path.xlsx'))

usernames_daddy = data['Username'].tolist()
usernames = usernames_daddy.copy()

account_data = {username:{"follow_path":[], "score":0, "wins": 0, "mm_rank_opened":False} for username in usernames}
match_history = {}

# For match 1
current_match_index = 1
match_history[current_match_index] = []
for i in range(len(usernames) // 10): #i = 0
    start_index = i * 10
    end_index = (i + 1) * 10
    batch_1, batch_2, batch_1_score, batch_2_score = [], [], [], []
    for j in range(start_index, start_index + 5): #j = start_index
        batch_1.append(usernames[j])
        batch_1_score.append(account_data[usernames[j]]['score'])
        
        account_data[usernames[j]]['follow_path'].append('w')
        account_data[usernames[j]]['score'] += 1
        account_data[usernames[j]]['wins'] += 1
    
    for j in range(start_index + 5, end_index): #j = start_index + 5
        batch_2.append(usernames[j])
        batch_2_score.append(account_data[usernames[j]]['score'])
        
        account_data[usernames[j]]['follow_path'].append('l')
        account_data[usernames[j]]['score'] -= 1
    match_history[current_match_index].append({"batch_1": batch_1, 
                                               "batch_2": batch_2, 
                                               "batch_1_score": batch_1_score, 
                                               "batch_2_score": batch_2_score, 
                                               "batch_1_total": sum(batch_1_score), 
                                               "batch_2_total": sum(batch_2_score), 
                                               "absolute_difference": abs(sum(batch_1_score) - sum(batch_2_score)), 
                                               "match_played": "Not Played Yet"
                                               })

#%%
for current_match_index in range(2, 20): #current_match_index = 50
    match_history[current_match_index] = []
    usernames = usernames_daddy.copy()
    
    # removing ranked accs in batches of 10
    accounts_rank_opened = [account_data[username]['mm_rank_opened'] for username in usernames]
    set(accounts_rank_opened)
    number_of_accounts_with_rank = accounts_rank_opened.count(True)
#    print("Index: %d | Rank Opened in: %d"%(current_match_index, number_of_accounts_with_rank))
    number_of_accounts_to_remove = number_of_accounts_with_rank - (number_of_accounts_with_rank % 10)
    # for i in range(number_of_accounts_to_remove):
    #     usernames.remove(usernames[accounts_rank_opened.index(True)])
    usernames = [username for username in usernames if not account_data[username]['mm_rank_opened']]
    print("Using %d"%(len(usernames)))
    follow_path = ["".join(account_data[username]['follow_path']) for username in usernames]
    account_wins = [account_data[username]['wins'] for username in usernames]
    
    next_match_outcome = [None] * len(usernames) #TODO
    accounts_remaining = list(range(len(usernames)))
    follow_path_score = [account_data[username]['score'] for username in usernames]
    unique_follow_path_score = list(sorted(list(set(follow_path_score)), reverse = True))
    d = {}
    for score in unique_follow_path_score: #score = unique_follow_path_score[0]
        d[score] = d.get(score, {})
        for index in range(len(usernames)):
            if follow_path_score[index] == score:
                d[score][follow_path[index]] = d[score].get(follow_path[index], []) + [index]
    
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
                match_history[current_match_index].append(current_batch)
                
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
        current_batch['match_played'] = "Not Played Yet"
        match_history[current_match_index].append(current_batch)

    accounts_rank_opened = [account_data[username]['mm_rank_opened'] for username in usernames_daddy]
    number_of_accounts_with_rank = accounts_rank_opened.count(True)
    print("Index: %d | Rank Opened in: %d"%(current_match_index, number_of_accounts_with_rank))

    account_wins = [account_data[username]['wins'] for username in usernames_daddy]
            
















