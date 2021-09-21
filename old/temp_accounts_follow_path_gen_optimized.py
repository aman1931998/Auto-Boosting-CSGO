import multiprocessing
import random
import pandas as pd
import os
from itertools import combinations, permutations
from tqdm import tqdm 

current_col_number = 10
new_col_number = current_col_number + 1
data = pd.read_excel(os.path.join('database', 'batch_2_follow_path_to_use_optimized_' + str(current_col_number) + '.xlsx'))

'''
for i in range(50):
    print('m%d = data[%d].tolist()'%(i+1, i+1))

'''


usernames = data['Username'].tolist()

matches_dict = {}
for i in [i for i in list(data.columns) if type(i) == int]:
    matches_dict[i] = data[i]

follow_path = []
for i in range(len(usernames)):
    path = ""
    for j in matches_dict.keys(): path += matches_dict[j][i]
    follow_path.append(path)

accounts_wins = [i.count('w') for i in follow_path]
accounts_rank_opened = [True if i.count('w') >= 10 else False for i in follow_path]
print(set(accounts_rank_opened), accounts_rank_opened.count(True))

#%%
def convert_to_digit(x):
    return [1 if i == 'w' else -1 for i in list(x)]
def convert_to_wins(x):
    return sum([1 for i in list(x) if i == 'w'])


next_match_outcome = [None] * 1000
accounts_remaining = list(range(1000))


follow_path_score = [sum(convert_to_digit(i)) for i in follow_path]
unique_follow_path_score = list(sorted(list(set(follow_path_score)), reverse = True))

# Get account_data in dict
d = {}
for score in unique_follow_path_score: #score = unique_follow_path_score[0]
    d[score] = d.get(score, {})
    for index in range(len(usernames)):
        if follow_path_score[index] == score:
            d[score][follow_path[index]] = d[score].get(follow_path[index], []) + [index]



batches_covered = {"0": {}}
#%
for score in unique_follow_path_score: #score = unique_follow_path_score[0]
    batches_covered["0"][score] = []
    for pattern in sorted(d[score].keys()): #pattern = sorted(d[score].keys())[0]
        while True:
            if len(d[score][pattern]) >= 10:
                current_batch = {}
                current_batch['1'] = d[score][pattern][0:5]
                current_batch['2'] = d[score][pattern][5:10]
                for index in d[score][pattern][0:5]: next_match_outcome[index] = 'w'; accounts_remaining.remove(index)
                for index in d[score][pattern][5:10]: next_match_outcome[index] = 'l'; accounts_remaining.remove(index)
                d[score][pattern] = d[score][pattern][10:]
                batches_covered["0"][score].append(current_batch)
            else:
                break




#%%
#%% # Optimized
batch_difference = 0
dataset = []
accs = accounts_remaining.copy()
scores_dict = {}
for index in accs: # index = accs[0]    
    score = follow_path_score[index]
    scores_dict[score] = scores_dict.get(score, []) + [index]

number_of_batches = len(accs) // 10
for i in range(number_of_batches):
    batch_details = {}
    batch_1 = []
    batch_2 = []
    batch_1_score = []
    batch_2_score = []
    for j in range(5):
        def clear_empty_scores(scores_dict):
            new_dict = {}
            for score in scores_dict.keys():
                if len(scores_dict[score]) == 0: continue
                new_dict[score] = scores_dict[score]
            return new_dict

        scores_dict = clear_empty_scores(scores_dict)
        max_score_in_dict = max(scores_dict.keys())

        get_index_with_max_score = scores_dict[max_score_in_dict].pop()
        batch_1.append(get_index_with_max_score)
        batch_1_score.append(max_score_in_dict)

        scores_dict = clear_empty_scores(scores_dict)
        max_score_in_dict = max(scores_dict.keys())

        get_index_with_max_score = scores_dict[max_score_in_dict].pop()
        batch_2.append(get_index_with_max_score)
        batch_2_score.append(max_score_in_dict)
    
    batch_details['max_score_of_2'] = max(sum(batch_1_score), sum(batch_2_score))
    batch_details['absolute_difference'] = abs(sum(batch_1_score) - sum(batch_2_score))
    batch_details['min_score_of_2'] = min(sum(batch_1_score), sum(batch_2_score))
    batch_details['batch_1'] = batch_1
    batch_details['batch_2'] = batch_2
    batch_details['batch_1_score'] = batch_1_score
    batch_details['batch_2_score'] = batch_2_score
    batch_details['batch_1_sum'] = sum(batch_1_score)
    batch_details['batch_2_sum'] = sum(batch_2_score)
    
    dataset.append(batch_details)


for i in range(len(range(len(accounts_remaining) // 10))): #i = 0
    batch_1 = dataset[i]['batch_1']
    batch_2 = dataset[i]['batch_2']
    batch_1_sum = dataset[i]['batch_1_sum']
    batch_2_sum = dataset[i]['batch_2_sum']
    if batch_1_sum >= batch_2_sum: 
        for j in range(5):# j = 0
            next_match_outcome[batch_1[j]] = 'w'
            next_match_outcome[batch_2[j]] = 'l'
    else:
        for j in range(5):# j = 0
            next_match_outcome[batch_1[j]] = 'l'
            next_match_outcome[batch_2[j]] = 'w'

print(set(next_match_outcome), next_match_outcome.count(None))

#%%
data[new_col_number] = next_match_outcome

new_follow_path = [follow_path[i] + next_match_outcome[i] for i in range(len(usernames))]
new_accounts_wins = [i.count('w') for i in new_follow_path]
new_accounts_rank_opened = [True if i.count('w') >= 10 else False for i in new_follow_path]

for i in range(len(usernames)):
    if new_accounts_rank_opened[i]:
        print(i, end = " ")

data.to_excel(os.path.join('database', 'batch_2_follow_path_to_use_optimized_' + str(new_col_number) + '.xlsx'))








