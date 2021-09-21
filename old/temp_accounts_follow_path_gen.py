import multiprocessing
import random
import pandas as pd
import os
from itertools import combinations, permutations
from tqdm import tqdm 

data = pd.read_excel(os.path.join('database', 'batch_2_follow_path_to_use_6.xlsx'))


usernames = data['Username'].tolist()
m1 = data[1].tolist()
m2 = data[2].tolist()
m3 = data[3].tolist()
m4 = data[4].tolist()
m5 = data[5].tolist()
m6 = data[6].tolist()

follow_path = [m1[i] + m2[i] + m3[i] + m4[i] + m5[i] + m6[i] for i in range(len(usernames))]

accounts_rank_opened = [True if i.count('w') >= 10 else False for i in follow_path]

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
# finding next match combination.

### ??? TODO FIX
#%% when batch difference == absolute 0
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
#1 to 15 done
target = 124
print(target)
def get_batch(accounts_remaining, target = 0):
    temp_acc = accounts_remaining.copy()
    while True:
        random.shuffle(temp_acc)
        temp_batches = {}
        assert len(temp_acc) % 10 == 0
        for i in range(len(temp_acc) // 10):
            temp_batches[i] = {}
            temp_start = i * 10
            temp_end = (i+1) * 10
            temp_batches[i]['batch_1'] = temp_acc[temp_start:temp_start+5]
            temp_batches[i]['batch_2'] = temp_acc[temp_start+5:temp_end]
            batch_1_scores = [follow_path_score[i] for i in temp_batches[i]['batch_1']]
            batch_2_scores = [follow_path_score[i] for i in temp_batches[i]['batch_2']]
            temp_batches[i]['batch_1_score'] = batch_1_scores
            temp_batches[i]['batch_2_score'] = batch_2_scores
            temp_batches[i]['batch_1_total'] = sum(batch_1_scores)
            temp_batches[i]['batch_2_total'] = sum(batch_2_scores)
            temp_batches[i]['difference'] = abs(sum(batch_2_scores) - sum(batch_1_scores))
        total_difference = sum([temp_batches[i]['difference'] for i in range(len(temp_acc) // 10)])
        if total_difference == target:
            return temp_batches

#target_range = [0, 1000]

dataset = []
for i in tqdm(range(500000)):
    dataset.append(get_batch(accounts_remaining, target))
'''
batch_sums = {}
for j in range(len(dataset)): #data_ = dataset[0]
    l = []
    data_ = dataset[j]
    for i in range(len(accounts_remaining) // 10):
        l.append(abs(data_[i]['batch_1_total']))
    batch_sums[sum(l)] = batch_sums.get(sum(l), []) + [j]

# analyse batch_sums


index_final = batch_sums[32][0]     ### Change this #TODO

final_batches = dataset[index_final]

#%% apply changes!!!
for i in range(len(accounts_remaining) // 10):
    batch_1 = final_batches[i]['batch_1']
    batch_2 = final_batches[i]['batch_2']
    for j in range(5):
        next_match_outcome[batch_1[j]] = 'w'
        next_match_outcome[batch_2[j]] = 'l'


data[7] = next_match_outcome



data.to_excel(os.path.join('database', 'batch_2_follow_path_to_use_7.xlsx'))



'''













