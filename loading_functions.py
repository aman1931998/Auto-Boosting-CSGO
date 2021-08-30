import cv2, pickle, secrets
from PIL import Image
import numpy as np, pandas as pd
import os
from datetime import datetime
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
#from ElementTree_pretty import prettify
from tqdm import tqdm

#%% Loads all usernames for the batch | can be used anywhere for loading the list of usernames, so place it at top of all calls.
def load_usernames(usernames_path = os.path.join('database', 'batch_2.xlsx')):
    '''
    Loads all usernames for the complete batch.
    '''
    if usernames_path.split(".")[-1] == 'xlsx':
        usernames = pd.read_excel(usernames_path)['Username'].tolist()
    if usernames_path.split(".")[-1] == 'csv':
        usernames = pd.read_csv(usernames_path)['Username'].tolist()
    return usernames

#%% Loads MM_Rank Database as dict of numpy arrays. WIP{not used anywhere yet.}
def load_mm_rank_database(path = os.path.join('images', 'mm_ranks')): #, 'numpy_objects')):
    '''
    Loads MM Rank database in form of dict.
    '''
    list_files = os.listdir(path)
    try:
        list_files.remove('numpy_objects')
    except:
        pass
    try:
        list_files.remove('Thumbs.db')
    except:
        pass
    mm_ranks = ['expired', 'unranked', 's1', 's2', 's3', 's4', 'se', 'sem', 'gn1', 'gn2', 'gn3', 'gnm', 'mg1', 'mg2', 'mge', 'dmg', 'le', 'lem', 'smfc', 'ge']#, 'unknown']
    mm_ranks_data = {i:[] for i in mm_ranks}
    for file in list_files: #file = list_files[0]
        image = Image.open(os.path.join(path, file)).convert('RGB')
        image_array = np.array(image)
        # image_array = np.load(os.path.join(path, file))
        assert image_array.shape[-1] == 3
        image_rank = file.split("_")[0]
        try:
            mm_ranks_data[image_rank].append(image_array)
        except:
            pass
    return mm_ranks_data

def load_pr_rank_database(path = os.path.join('images', 'pr_ranks')): #, 'numpy_objects')):
    '''
    Loads PR Rank database in form of dict.
    '''
    list_files = os.listdir(path)
    try:
        list_files.remove('numpy_objects')
    except:
        pass
    try:
        list_files.remove('Thumbs.db')
    except:
        pass
    pr_ranks = [str(i) for i in range(1, 41)]# + ['unknown']
    pr_ranks_data = {i:[] for i in pr_ranks}
    for file in list_files: #file = list_files[0]
        image = Image.open(os.path.join(path, file)).convert('RGB')
        image_array = np.array(image)
        # image_array = np.load(os.path.join(path, file))
        assert image_array.shape[-1] == 3
        image_rank = file.split("_")[0]
        try:
            pr_ranks_data[image_rank].append(image_array)
        except:
            pass
    return pr_ranks_data


#%% Loads XML files of account and return the list. | helps in saving_functions/update_account_data_completed
def get_account_info_xml_objects(username, file_order = ['info','trade_info', 'mm_rank_info', 'pr_rank_info', 'cooldown_info', 'match_history', 'weekly_info'], get_root = True):
    '''
    Loads the XML files of the username given and return the ET objects in a list.
    '''
    return_objs = []
    base_path = os.path.join('database', 'open_database', username)
    for file in file_order: 
        # print(file)
        file_io = open(os.path.join(base_path, file + '.xml'), 'r')
        info_obj = ET.parse(file_io)
        if get_root:
            info_obj = info_obj.getroot()
        file_io.close()
        return_objs.append(info_obj)
    return return_objs

#%% Loads the account database of the usernames[list] supplied. | Used in mm_batch_creator_functions. and driver_code
def load_account_database(usernames = load_usernames(), return_type = "dict", username_oriented = True):
    '''
    Loads the account database of the usernames[list] supplied.
    
    usernames: list of usernames, default: load_usernames()
    return_type: 'dict' or 'dataframe'
    username_oriented: bool, to be used with return type, default is True.
    '''
    #open_database_directory = os.path.join('database', 'open_database')
    # account_data = pd.DataFrame()
    steamids, passwords, mm_ranks, mm_wins, pr_ranks, last_mm_rank_updates, last_cooldown_types, \
        last_cooldown_times, friend_codes, target_pr_ranks, mm_rank_historys, xp_gained_for_next_ranks, \
            current_week_numbers, current_week_number_match_counts, \
                match_historys, match_history_times = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
    for i in tqdm(range(len(usernames))): #i = 0
        username = usernames[i]
        # print(username, end = ',')
        info_io, trade_info_io, mm_rank_info_io, pr_rank_info_io, cooldown_info_io, \
            match_history_io, weekly_info_io = get_account_info_xml_objects(username, ['info','trade_info', 'mm_rank_info', 'pr_rank_info', \
                                                                                         'cooldown_info', 'match_history', \
                                                                                             'weekly_info'], get_root = True)
        # file_io = open(os.path.join('database', 'open_database', username, 'info.xml'))
        # info_io = ET.parse(file_io).getroot()
        # file_io.close()
        # file_io = open(os.path.join('database', 'open_database', username, 'info.xml'))
        # trade_info_io = ET.parse(os.path.join('database', 'open_database', username, 'trade_info.xml')).getroot()
        # file_io.close()
        # file_io = open(os.path.join('database', 'open_database', username, 'info.xml'))
        # mm_rank_info_io = ET.parse(os.path.join('database', 'open_database', username, 'mm_rank_info.xml')).getroot()
        # file_io.close()
        # file_io = open(os.path.join('database', 'open_database', username, 'info.xml'))
        # pr_rank_info_io = ET.parse(os.path.join('database', 'open_database', username, 'pr_rank_info.xml')).getroot()
        # file_io.close()
        # file_io = open(os.path.join('database', 'open_database', username, 'info.xml'))
        # weekly_info_io = ET.parse(os.path.join('database', 'open_database', username, 'weekly_info.xml')).getroot()
        # file_io.close()
        # file_io = open(os.path.join('database', 'open_database', username, 'info.xml'))
        # cooldown_info_io = ET.parse(os.path.join('database', 'open_database', username, 'cooldown_info.xml')).getroot()
        # file_io.close()
        # file_io = open(os.path.join('database', 'open_database', username, 'info.xml'))
        # match_history_io = ET.parse(os.path.join('database', 'open_database', username, 'match_history.xml')).getroot()
        # file_io.close()
        steamids.append(info_io.findtext('SteamID'))
        passwords.append(info_io.findtext('Password'))
        mm_ranks.append(info_io.findtext('MM_Rank'))
        mm_wins.append(int(info_io.findtext('MM_Wins')))
        pr_ranks.append(info_io.findtext('PR_Rank'))
        last_mm_rank_updates.append(datetime.strptime(info_io.findtext('Last_MM_Rank_Updated_Time'), r'%Y-%m-%d %H:%M:%S.%f')) ##
        last_cooldown_types.append(info_io.findtext('Last_Cooldown_Type'))
        last_cooldown_times.append(datetime.strptime(info_io.findtext('Last_Cooldown_Time'), r'%Y-%m-%d %H:%M:%S.%f') if info_io.findtext('Last_Cooldown_Time') != "No Info" else "No Info") ##
        friend_codes.append(info_io.findtext('Friend_Code'))
        target_pr_ranks.append(int(info_io.findtext('Target_PR_Rank')))
        t_mm_rank_history = []
        for element in mm_rank_info_io.find('MM_Rank_History').getchildren(): #element = mm_rank_info_io.find('MM_Rank_History').getchildren()[0]
            t_mm_rank_history.append(element.text)
        mm_rank_historys.append(t_mm_rank_history)
        xp_gained_for_next_ranks.append(float(pr_rank_info_io.findtext('XP_Gained_For_Next_Rank')))
        current_week_numbers.append(pr_rank_info_io.findtext('Current_Week_Number'))
        current_week_number_match_counts.append(int(pr_rank_info_io.findtext('Current_Week_Number_Match_Count')))
        t_match_history = []
        t_match_history_time = []
        for element in match_history_io.find('MatchIDs').getchildren()[-10:]: #element = match_history_io.find('MatchIDs').getchildren()[0]
            t_match_history.append(element.findtext('Output'))
            t_match_history_time.append(datetime.strptime(element.findtext('Datestamp'), r'%Y-%m-%d %H:%M:%S.%f'))
        match_historys.append(t_match_history) ###
        match_history_times.append(t_match_history_time)
    if return_type == 'dict':
        account_data = {}
        if username_oriented == True:
            for i in range(len(usernames)): #i = 0
                account_data[usernames[i]] = {}
                account_data[usernames[i]]['Username'] = usernames[i]
                account_data[usernames[i]]['SteamID'] = steamids[i]
                account_data[usernames[i]]['Password'] = passwords[i]
                account_data[usernames[i]]['MM_Rank'] = mm_ranks[i]
                account_data[usernames[i]]['MM_Wins'] = mm_wins[i]
                account_data[usernames[i]]['PR_Rank'] = pr_ranks[i]
                account_data[usernames[i]]['Last_MM_Rank_Updated_Time'] = last_mm_rank_updates[i]
                account_data[usernames[i]]['Last_Cooldown_Type'] = last_cooldown_types[i]
                account_data[usernames[i]]['Last_Cooldown_Time'] = last_cooldown_times[i]
                account_data[usernames[i]]['Friend_Code'] = friend_codes[i]
                account_data[usernames[i]]['Target_PR_Rank'] = target_pr_ranks[i]
                account_data[usernames[i]]['MM_Rank_History'] = mm_rank_historys[i]
                account_data[usernames[i]]['XP_Gained_For_Next_Rank'] = xp_gained_for_next_ranks[i]
                account_data[usernames[i]]['Current_Week_Number'] = current_week_numbers[i]
                account_data[usernames[i]]['Current_Week_Number_Match_Count'] = current_week_number_match_counts[i]
                account_data[usernames[i]]['Matches_History'] = match_historys[i]
                account_data[usernames[i]]['Matches_DateTime'] = match_history_times[i]
        else:
            account_data = {"Username": usernames, 
                            "SteamID": steamids, 
                            "Password": passwords, 
                            "MM_Rank": mm_ranks, 
                            "MM_Wins": mm_wins, 
                            "PR_Rank": pr_ranks, 
                            "Last_MM_Rank_Updated_Time": last_mm_rank_updates, 
                            "Last_Cooldown_Type": last_cooldown_types, 
                            "Last_Cooldown_Time": last_cooldown_times, 
                            "Friend_Code": friend_codes, 
                            "Target_PR_Rank": target_pr_ranks, 
                            "MM_Rank_History": mm_rank_historys, 
                            "XP_Gained_For_Next_Rank": xp_gained_for_next_ranks, 
                            "Current_Week_Number": current_week_numbers, 
                            "Current_Week_Number_Match_Count": current_week_number_match_counts, 
                            "Matches_History": match_historys, 
                            "Matches_DateTime": match_history_times, 
                            }
        return account_data

#%% [Internal Function] Gets MM Ranks of accounts from /<username>/mm_rank_info.xml
def get_mm_rank_of_accounts_internal(usernames):
    '''
    [Internal Function] Gets MM Ranks of accounts from /<username>/mm_rank_info.xml
    Wrapped by get_mm_rank_of_accounts
    '''
    data = []
    for username in usernames:
        data_info_path = os.path.join('database', 'open_database', username, 'mm_rank_info.xml')
        file_io = open(data_info_path)
        xml_object = ET.parse(file_io)
        xml_root = xml_object.getroot()
        data.append(str(xml_root.find('MM_Rank').text))
        file_io.close()
    return data

# Gets MM Ranks of accounts from /<username>/mm_rank_info.xml
def get_mm_rank_of_accounts(usernames):
    '''
    Gets MM Ranks of accounts from /<username>/mm_rank_info.xml
    Usernames can be a:
        list of 10
        list of 2 -> 5
        list of 1
        single element
    '''
    if type(usernames) == str:
        return get_mm_rank_of_accounts_internal([usernames])[0]
    elif type(usernames) == list:
        if len(usernames) == 10:
            return get_mm_rank_of_accounts_internal(usernames)
        elif len(usernames) == 2:
            assert len(usernames[0]) == 5 and len(usernames[1]) == 5
            data_1 = get_mm_rank_of_accounts_internal(usernames[0])
            data_2 = get_mm_rank_of_accounts_internal(usernames[1])
            return [data_1, data_2]
        elif len(usernames) == 1:
            return get_mm_rank_of_accounts_internal(usernames)

#%%
#%% [Internal Function] Gets PR Ranks of accounts from <username>/pr_rank_info.xml
def get_pr_rank_of_accounts_internal(usernames):
    '''
    [Internal Function] Gets PR Ranks of accounts from /<username>/pr_rank_info.xml
    Wrapped by get_pr_rank_of_accounts
    '''
    data = []
    for username in usernames:
        data_info_path = os.path.join('database', 'open_database', username, 'pr_rank_info.xml')
        file_io = open(data_info_path)
        xml_object = ET.parse(file_io)
        xml_root = xml_object.getroot()
        value = str(xml_root.find('PR_Rank').text)
        if value.isdigit():
            value = float(value)
        else:
            value = 0
        data.append(float())
        file_io.close()
    return data

def get_pr_rank_of_accounts(usernames):
    '''
    Gets PR Ranks of accounts from /<username>/pr_rank_info.xml
    Usernames can be a:
        list of 10
        list of 2 -> 5
        list of 1
        single element
    '''
    if type(usernames) == str:
        return get_pr_rank_of_accounts_internal([usernames])[0]
    elif type(usernames) == list:
        if len(usernames) == 10:
            return get_pr_rank_of_accounts_internal(usernames)
        elif len(usernames) == 2:
            assert len(usernames[0]) == 5 and len(usernames[1]) == 5
            data_1 = get_pr_rank_of_accounts_internal(usernames[0])
            data_2 = get_pr_rank_of_accounts_internal(usernames[1])
            return [data_1, data_2]
        elif len(usernames) == 1:
            return get_pr_rank_of_accounts_internal(usernames)

#%% [Internal Function] Gets Match Number of accounts from /<username>/match_history.xml
def get_match_number_of_accounts_internal(usernames):
    '''
    [Internal Function] Gets Match Number of accounts from /<username>/match_history.xml
    Wrapped by get_match_number_of_accounts
    '''
    data = []
    for username in usernames:
        data_info_path = os.path.join('database', 'open_database', username, 'match_history.xml')
        file_io = open(data_info_path)
        xml_object = ET.parse(file_io)
        xml_root = xml_object.getroot()
        data.append(str(xml_root.find('Match_Count').text))
        file_io.close()
    return data

# Gets Match Number of accounts from /<username>/match_history.xml
def get_match_number_of_accounts(usernames):
    '''
    Gets Match Number of accounts from /<username>/match_history.xml
    Usernames can be a:
        list of 10
        list of 2 -> 5
        list of 1
        single element
    '''
    if type(usernames) == str:
        return get_match_number_of_accounts_internal([usernames])[0]
    elif type(usernames) == list:
        if len(usernames) == 10:
            return get_match_number_of_accounts_internal(usernames)
        elif len(usernames) == 2:
            assert len(usernames[0]) == 5 and len(usernames[1]) == 5
            data_1 = get_match_number_of_accounts_internal(usernames[0])
            data_2 = get_match_number_of_accounts_internal(usernames[1])
            return [data_1, data_2]
        elif len(usernames) == 1:
            return get_match_number_of_accounts_internal(usernames)

#%% [Internal Gets Match Number of accounts from /<username>/match_history.xml
def get_xp_gained_for_next_week_of_accounts_internal(usernames):
    '''
    [Internal Function] Gets XP Gained For Next Week of accounts from /<username>/pr_rank_info.xml
    Wrapped by get_xp_gained_for_next_week_of_accounts
    '''
    data = []
    for username in usernames:
        data_info_path = os.path.join('database', 'open_database', username, 'pr_rank_info.xml')
        file_io = open(data_info_path)
        xml_object = ET.parse(file_io)
        xml_root = xml_object.getroot()
        data.append(str(xml_root.find('XP_Gained_For_Next_Rank').text))
        file_io.close()
    return data

# Gets XP Gained for this week from /<usernanme>/pr_rank_info.xml
def get_xp_gained_for_next_week_of_accounts(usernames):
    '''
    Gets XP Gained For Next Week of accounts from /<username>/pr_rank_info.xml
    Usernames can be a:
        list of 10
        list of 2 -> 5
        list of 1
        single element
    '''
    if type(usernames) == str:
        return get_xp_gained_for_next_week_of_accounts_internal([usernames])[0]
    elif type(usernames) == list:
        if len(usernames) == 10:
            return get_xp_gained_for_next_week_of_accounts_internal(usernames)
        elif len(usernames) == 2:
            assert len(usernames[0]) == 5 and len(usernames[1]) == 5
            data_1 = get_xp_gained_for_next_week_of_accounts_internal(usernames[0])
            data_2 = get_xp_gained_for_next_week_of_accounts_internal(usernames[1])
            return [data_1, data_2]
        elif len(usernames) == 1:
            return get_xp_gained_for_next_week_of_accounts_internal(usernames)


#%% [Internal Function] Gets Week Match Count of accounts from /<username>/match_history.xml
def get_week_match_count_of_accounts_internal(usernames):
    '''
    [Internal Function] Gets Week Match Count of accounts from /<username>/pr_rank_info.xml
    Wrapped by get_week_match_count_of_accounts
    '''
    data = []
    for username in usernames:
        data_info_path = os.path.join('database', 'open_database', username, 'pr_rank_info.xml')
        file_io = open(data_info_path)
        xml_object = ET.parse(file_io)
        xml_root = xml_object.getroot()
        data.append(str(xml_root.find('Current_Week_Number_Match_Count').text))
        file_io.close()
    return data

# Gets Week Match Count from /<username>/pr_rank_info.xml
def get_week_match_count_of_accounts(usernames):
    '''
    Gets Week Match Count of accounts from /<username>/pr_rank_info.xml
    Usernames can be a:
        list of 10
        list of 2 -> 5
        list of 1
        single element
    '''
    if type(usernames) == str:
        return get_week_match_count_of_accounts_internal([usernames])[0]
    elif type(usernames) == list:
        if len(usernames) == 10:
            return get_week_match_count_of_accounts_internal(usernames)
        elif len(usernames) == 2:
            assert len(usernames[0]) == 5 and len(usernames[1]) == 5
            data_1 = get_week_match_count_of_accounts_internal(usernames[0])
            data_2 = get_week_match_count_of_accounts_internal(usernames[1])
            return [data_1, data_2]
        elif len(usernames) == 1:
            return get_week_match_count_of_accounts_internal(usernames)


#%% [Internal Function] Gets Week Number of accounts from /<username>/match_history.xml
def get_week_number_of_accounts_internal(usernames):
    '''
    [Internal Function] Gets Week Number of accounts from /<username>/pr_rank_info.xml
    Wrapped by get_week_match_count_of_accounts
    '''
    data = []
    for username in usernames:
        data_info_path = os.path.join('database', 'open_database', username, 'pr_rank_info.xml')
        file_io = open(data_info_path)
        xml_object = ET.parse(file_io)
        xml_root = xml_object.getroot()
        data.append(str(xml_root.find('Current_Week_Number').text))
        file_io.close()
    return data

# Gets Week Number from /<username>/pr_rank_info.xml
def get_week_number_of_accounts(usernames):
    '''
    Gets Week Number of accounts from /<username>/pr_rank_info.xml
    Usernames can be a:
        list of 10
        list of 2 -> 5
        list of 1
        single element
    '''
    if type(usernames) == str:
        return get_week_number_of_accounts_internal([usernames])[0]
    elif type(usernames) == list:
        if len(usernames) == 10:
            return get_week_number_of_accounts_internal(usernames)
        elif len(usernames) == 2:
            assert len(usernames[0]) == 5 and len(usernames[1]) == 5
            data_1 = get_week_number_of_accounts_internal(usernames[0])
            data_2 = get_week_number_of_accounts_internal(usernames[1])
            return [data_1, data_2]
        elif len(usernames) == 1:
            return get_week_number_of_accounts_internal(usernames)














#%%
# def get_friend_code_of_accounts_internal(usernames):
#     '''
#     [Internal Gets friend code of accounts from /<username>/info.xml
#     Wrapped by get_match_number_of_accounts
#     '''
#     data = []
#     for username in usernames:
#         data_info_path = os.path.join('database', 'open_database', username, 'info.xml')
#         file_io = open(data_info_path)
#         xml_object = ET.parse(file_io)
#         xml_root = xml_object.getroot()
#         data.append(str(xml_root.find('Match_Count').text))
#         file_io.close()
#     return data


# def get_friend_code_of_accounts(usernames):
#     '''
#     Gets friend code of accounts from /<username>/info.xml
#     Usernames can be a:
#         list of 10
#         list of 2 -> 5
#         list of 1
#         single element
#     '''
#     if type(usernames) == str:
#         return get_friend_code_of_accounts_internal([usernames])[0]
#     elif type(usernames) == list:
#         if len(usernames) == 10:
#             return get_friend_code_of_accounts_internal(usernames)
#         elif len(usernames) == 2:
#             assert len(usernames[0]) == 5 and len(usernames[1]) == 5
#             data_1 = get_friend_code_of_accounts_internal(usernames[0])
#             data_2 = get_friend_code_of_accounts_internal(usernames[1])
#             return [data_1, data_2]
#         elif len(usernames) == 1:
#             return get_friend_code_of_accounts_internal(usernames)


