from account_loading_functions import load_full_account_database

account_database = load_full_account_database()
mm_rank_data = {}
mm_wins_data = {}
pr_rank_data = {}
for username in account_database.keys():
    mm_rank = account_database[username]['info']["MM_Rank"] 
    mm_wins = account_database[username]['info']["MM_Wins"] 
    pr_rank = account_database[username]['info']['PR_Rank']
    try:
        pr_rank = str(int(float(pr_rank)))
    except:
        pr_rank = str(pr_rank)
    if mm_rank in mm_rank_data:
        mm_rank_data[mm_rank].append(username)
    else :
        mm_rank_data[mm_rank]=[username]
    if mm_wins in mm_wins_data:
        mm_wins_data[mm_wins].append(username)
    else: 
        mm_wins_data[mm_wins] = [username]
    if pr_rank in pr_rank_data:
        pr_rank_data[pr_rank].append(username)
    else: 
        pr_rank_data[pr_rank] = [username]

mm_rank_series = ['ge', 'smfc', 'lem', 'le', 'dmg', 'mge', 'mg2', 'mg1', 'gnm', 'gn3', 'gn2', 'gn1', 'sem', 'se', 's4', 's3', 's2', 's1', 'unranked', 'expired']


print("MM Rank Data")
for mm_rank in mm_rank_series:
    if mm_rank not in mm_rank_data.keys(): continue
    print(mm_rank, " " * (9 - len(mm_rank)) , "  -> ", len(mm_rank_data[mm_rank]))
print("MM Wins Data")
for mm_wins in sorted(mm_wins_data.keys(), key = lambda x: int(x)):
    print(mm_wins, "Wins", " " * (3 - len(str(mm_wins))) , "   -> ", len(mm_wins_data[mm_wins]))
print("PR Rank Data")
for pr_rank in pr_rank_data.keys(): #sorted(pr_rank_data.keys(), key = lambda x: int(x)):
    print("Rank", pr_rank, " " * (3 - len(str(pr_rank))) , "   -> ", len(pr_rank_data[pr_rank]))

#%%
import pandas as pd
import os
usernames = list(account_database.keys())
pr_ranks = [account_database[i]['pr_rank_info']['PR_Rank'] for i in usernames]
mm_ranks = [account_database[i]['mm_rank_info']['MM_Rank'] for i in usernames]
mm_winss = [account_database[i]['mm_rank_info']['MM_Wins'] for i in usernames]
df = pd.DataFrame()
df['Username'] = usernames
df['PR_Rank'] = pr_ranks
df['MM_Rank'] = mm_ranks
df['MM_Wins'] = mm_winss
df.to_excel(os.path.join("database", "pr_rank_sheet.xlsx"), index = False)


# import pandas as pd
# x = '''11
# 12
# 13
# 14
# 15
# 16
# 17
# 18
# 19
# unknown_7
# unknown_8
# unknown_9
# unknown_28
# unknown_29
# unknown_30
# unknown_47
# unknown_48
# unknown_49
# unknown_62
# unknown_63
# unknown_87
# unknown_88
# unknown_92
# unknown_98
# unknown_102
# unknown_112
# unknown_113
# unknown_120
# unknown_121
# unknown_127
# unknown_128'''.split("\n")
# l = []
# for i in x:
#     l += pr_rank_data[i]
# print(*l, sep = "\n")
# df = pd.DataFrame()
# df['Username'] = l
# df.to_excel('active_usernames.xlsx', index = False)

# pr rank
# no. matcches in current week












