import cv2, pickle, secrets
from PIL import Image
import numpy as np, pandas as pd
import os
from datetime import datetime
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from tqdm import tqdm
#from ElementTree_pretty import prettify

from loading_functions import get_mm_rank_of_accounts, get_pr_rank_of_accounts, get_account_info_xml_objects
from xml_functions import get_mm_mismatch_Mismatch_history_xml_object, get_new_cooldown_history_objects, get_match_ID_xml_object, get_mm_rank_history_objects
from helper_functions import prettify
from saving_functions import save_account_info_xml_objects

#%% mm_mismatch_data/mismatch_id.xml
# is called after every search completion [Match found or not]
def log_current_mismatch_details(mm_mismatchID, mm_batch, mismatch_data, match_found = False, total_search_time = 750):
    '''
    OUTPUT: mm_mismatch_data/mismatchID.xml
    
    mm_mismatchID: str, mismatchID of 8 characters
    mm_batch: dict of 9 keys
        batch_1, batch_2: list of 5 usernames
        batch_1_score, batch_2_score: list of 5
        batch_1_total, batch_2_total: list of 5
        absolute_difference: abs diff of batches
        match_played: match outcome
        winner: batch_1 or batch_2
    mismatch_data: dict of n mismatches
        '1': dict of 2
            "Match_Found_For": "team1" or "team2"
            "Timestamp_Recorded": datetime object
    match_found: bool, default is False
    total_search_time: int (or str), time in seconds.
    '''
    log_mismatch = ET.Element('Mismatch_Details')
    
    log_mismatch_mismatchID = ET.SubElement(log_mismatch, 'MismatchID')
    log_mismatch_mismatchID.text = str(mm_mismatchID)
    log_mismatch_match_found = ET.SubElement(log_mismatch, 'Match_Found')
    log_mismatch_match_found.text = str(match_found)
    log_mismatch_team_1 = ET.SubElement(log_mismatch, 'Team1')
    log_mismatch_team_1_list = []
    for i in range(5):#i = 0
        ll = ET.Element("Player", attrib = {"Index": str(i+1)})
        ll.text  = mm_batch['batch_1'][i]
        log_mismatch_team_1_list.append(ll)
    log_mismatch_team_1.extend(log_mismatch_team_1_list)
    log_mismatch_team_2 = ET.SubElement(log_mismatch, 'Team2')
    log_mismatch_team_2_list = []
    for i in range(5):#i = 0
        ll = ET.Element("Player", attrib = {"Index": str(i+1)})
        ll.text  = mm_batch['batch_2'][i]
        log_mismatch_team_2_list.append(ll)
    log_mismatch_team_2.extend(log_mismatch_team_2_list)
    log_mismatch_total_search_time = ET.SubElement(log_mismatch, 'Total_Search_Time')
    log_mismatch_total_search_time.text = str(total_search_time)
    log_mismatch_history = get_mm_mismatch_Mismatch_history_xml_object(mismatch_data)
    log_mismatch.append(log_mismatch_history)
    
    with open(os.path.join('database', 'mm_mismatch_data', str(mm_mismatchID) + '.xml'), 'w') as file:
        file.write(prettify(log_mismatch))
    
    return True

#%% matches_data/match_id.xml
def log_current_match_details(match_id, team1, team2, time_stamp, search_details, match_time_details, xp_gained_details):
    '''
    OUTPUT: matches_data/match_id.xml
    
    match_id: str, unique
    team1 and team2: dict
        username: list of 5
        mm_rank_update: list of 5
        pr_rank_update: list of 5
        match_number: list of 5
        week_number: list of 5
        week_match_count: list of 5
    time_stamp: datetime object
    search_details: dict
        search_start_time: datetime object
        search_error_count: str or int
        search_mismatchID: str, mismatchID for the session
        search_end_time: datetime object
    match_time_details: dict
        match_start_time: datetime object
        match_end_time: datetime object
    xp_gained_details: dict
        team1_xp_gained: list of 5
        team2_xp_gained: list of 5
    '''
    team1_username, team2_username = team1['username'], team2['username']
    team1_mm_rank, team2_mm_rank = get_mm_rank_of_accounts([team1['username'], team2['username']])
    team1_mm_rank_update, team2_mm_rank_update = team1['mm_rank_update'], team2['mm_rank_update']
    team1_pr_rank, team2_pr_rank = get_pr_rank_of_accounts([team1['username'], team2['username']])
    team1_pr_rank_update, team2_pr_rank_update = team1['pr_rank_update'], team2['pr_rank_update']
    team1_match_number, team2_match_number = team1['match_number'], team2['match_number']
    team1_week_number, team2_week_number = team1['week_number'], team2['week_number']
    team1_week_match_count, team2_week_match_count = team1['week_match_count'], team2['week_match_count']
    
    search_start_time = search_details['search_start_time']   #datetime object
    search_error_count = search_details['search_error_count'] #LIST
    #search_error_details = search_details['search_error_details'] #dict?
    search_mismatchID = search_details['search_mismatchID']
    search_end_time = search_details['search_end_time']   #datetime object
    search_duration = search_end_time - search_start_time ####
    
    match_start_time = match_time_details['match_start_time'] #datetime object
    match_end_time = match_time_details['match_end_time'] #datetime object
    match_duration = match_end_time - match_start_time ####
    
    team1_xp_gained, team2_xp_gained = xp_gained_details['team1_xp_gained'], xp_gained_details['team2_xp_gained']
    
    datetime_stamp = str(time_stamp)
    
    log_match_root = ET.Element("Match_Details")                               ###
    
    log_match_match_ID = ET.SubElement(log_match_root, "MatchID")
    log_match_match_ID.text = str(match_id)
    
    log_match_team_1 = ET.SubElement(log_match_root, 'Team_1')                 ###
    log_match_team_2 = ET.SubElement(log_match_root, 'Team_2')                 ###

    log_match_team_1_lobby_leader = ET.SubElement(log_match_team_1, "Lobby_Leader")
    log_match_team_1_lobby_leader.text = str(team1_username[0])
    log_match_team_2_lobby_leader = ET.SubElement(log_match_team_2, "Lobby_Leader")
    log_match_team_2_lobby_leader.text = str(team2_username[0])

    log_match_teammates_1 = ET.SubElement(log_match_team_1, 'Players')
    log_match_teammates_2 = ET.SubElement(log_match_team_2, 'Players')
    log_match_team_1_players, log_match_team_2_players = [], []
    
    for i in range(5):
        log_match_player = ET.Element("Player_%d"%(i+1))
        log_match_player_username = ET.SubElement(log_match_player, "Username")
        log_match_player_username.text = str(team1_username[i])
        log_match_player_mm_rank = ET.SubElement(log_match_player, "MM_Rank")
        log_match_player_mm_rank.text = str(team1_mm_rank[i])
        log_match_player_mm_rank_update = ET.SubElement(log_match_player, "MM_Rank_Update")
        log_match_player_mm_rank_update.text = str(team1_mm_rank_update[i])
        log_match_player_pr_rank = ET.SubElement(log_match_player, "PR_Rank")
        log_match_player_pr_rank.text = str(team1_pr_rank[i])
        log_match_player_pr_rank_update = ET.SubElement(log_match_player, "PR_Rank_Update")
        log_match_player_pr_rank_update.text = str(team1_pr_rank_update[i])
        log_match_player_match_number = ET.SubElement(log_match_player, "Match_Number")
        log_match_player_match_number.text = str(team1_match_number[i])
        log_match_player_week_number = ET.SubElement(log_match_player, "Week_Number")
        log_match_player_week_number.text = str(team1_week_number[i])
        log_match_player_week_match_number = ET.SubElement(log_match_player, "Week_Match_Number")
        log_match_player_week_match_number.text = str(team1_week_match_count[i])
        log_match_player_xp_earned = ET.SubElement(log_match_player, "XP_Gained")
        log_match_player_xp_earned.text = str(team1_xp_gained[i])
        log_match_team_1_players.append(log_match_player)

        log_match_player = ET.Element("Player_%d"%(i+1))
        log_match_player_username = ET.SubElement(log_match_player, "Username")
        log_match_player_username.text = str(team2_username[i])
        log_match_player_mm_rank = ET.SubElement(log_match_player, "MM_Rank")
        log_match_player_mm_rank.text = str(team2_mm_rank[i])
        log_match_player_mm_rank_update = ET.SubElement(log_match_player, "MM_Rank_Update")
        log_match_player_mm_rank_update.text = str(team2_mm_rank_update[i])
        log_match_player_pr_rank = ET.SubElement(log_match_player, "PR_Rank")
        log_match_player_pr_rank.text = str(team2_pr_rank[i])
        log_match_player_pr_rank_update = ET.SubElement(log_match_player, "PR_Rank_Update")
        log_match_player_pr_rank_update.text = str(team2_pr_rank_update[i])
        log_match_player_match_number = ET.SubElement(log_match_player, "Match_Number")
        log_match_player_match_number.text = str(team2_match_number[i])
        log_match_player_week_number = ET.SubElement(log_match_player, "Week_Number")
        log_match_player_week_number.text = str(team2_week_number[i])
        log_match_player_week_match_number = ET.SubElement(log_match_player, "Week_Match_Number")
        log_match_player_week_match_number.text = str(team2_week_match_count[i])
        log_match_player_xp_earned = ET.SubElement(log_match_player, "XP_Gained")
        log_match_player_xp_earned.text = str(team2_xp_gained[i])
        log_match_team_2_players.append(log_match_player)
    log_match_teammates_1.extend(log_match_team_1_players)
    log_match_teammates_2.extend(log_match_team_2_players)

    dstamp = ET.Element('Timestamp')
    dstamp.text = datetime_stamp
    log_match_root.append(dstamp)
    
    log_match_search_details = ET.SubElement(log_match_root, "Search_Details")
    log_match_search_start_time = ET.SubElement(log_match_search_details, "Search_Start_Time")
    log_match_search_start_time.text = str(search_start_time)
    log_match_search_error_count = ET.SubElement(log_match_search_details, "Search_Error_Count")
    log_match_search_error_count.text = str(search_error_count)
    log_match_search_mismatchID = ET.SubElement(log_match_search_details, 'MM_MismatchID')
    log_match_search_mismatchID.text = str(search_mismatchID)
    # log_match_search_error_details = get_search_error_details_xml_object(search_error_details)
    # log_match_search_details.append(log_match_search_error_details)
    log_match_search_end_time = ET.SubElement(log_match_search_details, "Search_End_Time")
    log_match_search_end_time.text = str(search_end_time)
    log_match_search_duration = ET.SubElement(log_match_search_details, "Search_Duration")
    log_match_search_duration.text = str(search_duration)
    
    log_match_time_details = ET.SubElement(log_match_root, "Match_Time_Details")
    log_match_start_time = ET.SubElement(log_match_time_details, "Match_Start_Time")
    log_match_start_time.text = str(match_start_time)
    log_match_end_time = ET.SubElement(log_match_time_details, "Match_End_Time")
    log_match_end_time.text = str(match_end_time)
    log_match_duration = ET.SubElement(log_match_time_details, "Match_Duration")
    log_match_duration.text = str(match_duration)
    
    with open(os.path.join('database', 'matches_data', str(match_id) + '.xml'), 'w') as file:
        file.write(prettify(log_match_root))
    
    return True

#%% Saves/Updates the account info files after match completion.
# <username>/info.xml, pr_rank_info.xml... etc.
def update_account_data_completed(mm_batch, match_id, team1, team2, time_stamp, xp_gained_details, cooldown_details, week_index): ###WIP ???
    '''
    OUTPUT: <username>/info.xml, pr_rank_info.xml... etc.
        Saves/Updates the account info files after match completion.
    
    
    mm_batch: dict of 9 keys, from mm_batches list
        batch_1, batch_2: list of 5 usernames
        batch_1_score, batch_2_score: list of 5
        batch_1_total, batch_2_total: list of 5
        absolute_difference: abs diff of batches
        match_played: match outcome
        winner: batch_1 or batch_2
    match_id: str, unique, from get_matchID function
    team1 and team2: dict, generated after match completed. 
        username: list of 5, from sheet
        mm_rank_update: list of 5 mm ranks (including if update.)
        pr_rank_update: list of 5 pr ranks (including if update.)
        week_number: list of 5 week_numbers (including if update.)
    time_stamp: datetime object
    xp_gained_details: dict
        team1_xp_gained: list of 5
        team2_xp_gained: list of 5
    cooldown_details: dict
        team1: list of 5
        team2: list of 5
    week_index: str or int| isdigit() = True
    '''
    assert mm_batch != None
    # if dynamic_account_data is None: global dynamic_account_data
    assert set(team1['username']) == set(mm_batch['batch_1'])
    assert set(team2['username']) == set(mm_batch['batch_2'])
    winner = mm_batch['winner']
    match_details = {"batch_1": team1, 
                     "batch_2": team2}
    for batch in ['batch_1', 'batch_2']: #batch = 'batch_1'
        batch_no = int(batch.split("_")[-1])
        for i in range(len(mm_batch[batch])): #i = 0
            username = mm_batch[batch][i]
            info_io, mm_rank_info_io, pr_rank_info_io, cooldown_info_io, match_history_io, weekly_info_io = get_account_info_xml_objects(username, file_order = ['info', 'mm_rank_info', 'pr_rank_info', 'cooldown_info', 'match_history', 'weekly_info'], get_root = True)
            # assert needed?
            # mm_rank
            #info_io.find('MM_Rank').text = match_details[batch]['mm_rank_update'][i]
            # Checkinf if MM rank has changed
            if str(info_io.find('MM_Rank').text) != str(match_details[batch]['mm_rank_update'][i]):
                # Checking if rank has opened
                if str(info_io.find('MM_Rank').text) == 'unranked' and str(match_details[batch]['mm_rank_update'][i]) != 'unranked':
                    # mm_rank_info/Rank_Opened
                    mm_rank_info_io.find('Rank_Opened').text = str(match_details[batch]['mm_rank_update'][i])
                    # mm_rank_info/Rank_Opened_Date
                    mm_rank_info_io.find('Rank_Opened_Date').text = str(time_stamp)
                    # mm_rank_info/Rank_Opened_MatchID
                    mm_rank_info_io.find('Rank_Opened_MatchID').text = str(match_id)
                
                # Getting MM Rank update index.
                mm_rank_updated_index = len(mm_rank_info_io.find('MM_Rank_History').getchildren()) + 1
                mm_rank_obj_, datetime_obj_ = get_mm_rank_history_objects(str(match_details[batch]['mm_rank_update'][i]), time_stamp, mm_rank_updated_index)
                print(mm_rank_obj_, datetime_obj_)
                # Adding a node with updated MM Rank
                # mm_rank_info/MM_Rank_History
                try:
                    mm_rank_info_io.find('MM_Rank_History').append(mm_rank_obj_)
                except:
                    mm_rank_info_io.find('MM_Rank_History').extend([mm_rank_obj_])
                    # mm_rank_info/MM_Rank_Time_History
                try:
                    mm_rank_info_io.find('MM_Rank_Time_History').append(datetime_obj_)
                except:
                    mm_rank_info_io.find('MM_Rank_Time_History').extend([datetime_obj_])
                # # info/MM_Rank
                # mm_rank_info_io.find('MM_Rank_History').extend([mm_rank_obj_])
                # # mm_rank_info/MM_Rank_Time_History
                # mm_rank_info_io.find('MM_Rank_Time_History').extend([datetime_obj_])
                # info/MM_Rank
                info_io.find('MM_Rank').text = str(match_details[batch]['mm_rank_update'][i])
                # mm_rank_info/MM_Rank
                mm_rank_info_io.find('MM_Rank').text = str(match_details[batch]['mm_rank_update'][i])
                # info/Last_MM_Rank_Updated_Time
                info_io.find("Last_MM_Rank_Updated_Time").text = str(time_stamp)
                # mm_rank_info/Last_MM_Rank_Updated_Time
                mm_rank_info_io.find("Last_MM_Rank_Updated_Time").text = str(time_stamp)
                # mm_rank_info/Last_MM_Rank_Update_MatchID
                mm_rank_info_io.find("Last_MM_Rank_Update_MatchID").text = str(match_id)
            # Checking for cooldown
            if cooldown_details['team' + str(batch_no)][i]['type'] in ['Yellow', 'Green']:
                # database_check
                assert type(cooldown_details['team' + str(batch_no)][i]) == dict
                # cooldown_info/Last_Cooldown_Type
                cooldown_info_io.find('Last_Cooldown_Type').text = str(cooldown_details['team' + str(batch_no)][i]['type'])
                # cooldown_info/Last_Cooldown_Time
                cooldown_info_io.find('Last_Cooldown_Time').text = str(cooldown_details['team' + str(batch_no)][i]['time'])
                # info/Last_Cooldown_Type
                info_io.find('Last_Cooldown_Type').text = str(cooldown_details['team' + str(batch_no)][i]['type'])
                # info/Last_Cooldown_Time
                info_io.find('Last_Cooldown_Time').text = str(cooldown_details['team' + str(batch_no)][i]['time'])
                # Getting Cooldown history index and objects
                cooldown_updated_index = len(cooldown_info_io.find('Cooldown_Time_History').getchildren()) + 1
                cooldown_type_new_obj_, cooldown_time_new_obj_, cooldown_matchID_new_obj_ = get_new_cooldown_history_objects(str(cooldown_details['team' + str(batch_no)][i]['type']), str(cooldown_details['team' + str(batch_no)][i]['time']), cooldown_updated_index, match_id)
                # cooldown_info/Cooldown_Type_History
                cooldown_info_io.find('Cooldown_Type_History').extend([cooldown_type_new_obj_])
                # cooldown_info/Cooldown_Time_History
                cooldown_info_io.find('Cooldown_Time_History').extend([cooldown_time_new_obj_])
                # cooldown_info/Cooldown_MatchID_History
                cooldown_info_io.find('Cooldown_MatchID_History').extend([cooldown_matchID_new_obj_])
            # Checking if account won the match
            if mm_batch['winner'] == batch:
                # database_check
                #assert info_io.find('MM_Wins').text == mm_rank_info_io.find('MM_Wins').text
                if info_io.find('MM_Wins').text != mm_rank_info_io.find('MM_Wins').text:
                    print("Database validation failed for MM_Wins.")
                # info/MM_Wins
                info_io.find('MM_Wins').text = str(int(info_io.find('MM_Wins').text) + 1)
                # mm_rank_info/MM_Wins
                mm_rank_info_io.find('MM_Wins').text = str(int(mm_rank_info_io.find('MM_Wins').text) + 1)
            # info/PR_Rank
            info_io.find('PR_Rank').text = str(match_details[batch]['pr_rank_update'][i])
            # pr_rank_info/PR_Rank
            pr_rank_info_io.find('PR_Rank').text = str(match_details[batch]['pr_rank_update'][i])
            # pr_rank_info/XP_Gained_For_Next_Rank
            pr_rank_info_io.find('XP_Gained_For_Next_Rank').text = str(float(pr_rank_info_io.find('XP_Gained_For_Next_Rank').text) + float(xp_gained_details['team%d_xp_gained'%(batch_no)][i]))
            # pr_rank_info/PR_Rank_History
            pr_rank_info_io.find('PR_Rank_History').find("./Week[@Index='%s']"%(str(week_index))).find('Weekly_XP_Gained').text = str(float(pr_rank_info_io.find('PR_Rank_History').find("./Week[@Index='%s']"%(str(week_index))).find('Weekly_XP_Gained').text) + float(xp_gained_details['team%d_xp_gained'%(batch_no)][i]))
            # database_check_commented
            # assert pr_rank_info_io.find('Current_Week_Number').text == weekly_info_io.find('Current_Week_Number').text
            if pr_rank_info_io.find('Current_Week_Number').text != weekly_info_io.find('Current_Week_Number').text:
                print("Database validation failed for Current_Week_Number.")
            # pr_rank_info/Current_Week_Number
            pr_rank_info_io.find('Current_Week_Number').text = str(match_details[batch]['week_number'][i])
            # weekly_info/Current_Week_Number
            weekly_info_io.find('Current_Week_Number').text = str(match_details[batch]['week_number'][i])
            # database_check
            #assert pr_rank_info_io.find('Current_Week_Number_Match_Count').text == weekly_info_io.find('Current_Week_Number_Match_Count').text
            if pr_rank_info_io.find('Current_Week_Number_Match_Count').text != weekly_info_io.find('Current_Week_Number_Match_Count').text:
                print("Database validation failed for Current_Week_Number_Match_Count.")
            # pr_rank_info/Current_Week_Number_Match_Count
            pr_rank_info_io.find('Current_Week_Number_Match_Count').text = str(int(pr_rank_info_io.find('Current_Week_Number_Match_Count').text) + 1)
            # weekly_info/Current_Week_Number_Match_Count
            weekly_info_io.find('Current_Week_Number_Match_Count').text = str(int(weekly_info_io.find('Current_Week_Number_Match_Count').text) + 1)
            # match_history/Match_Count
            match_history_io.find('Match_Count').text = str(int(match_history_io.find('Match_Count').text) + 1)
            # MatchIDs count
            match_matchIDs_updated_count_ = len(list(match_history_io.find('MatchIDs'))) + 1
            # match_history/MatchIDs
            try:
                match_history_io.find('MatchIDs').extend([get_match_ID_xml_object(match_id, time_stamp, output = 'w' if mm_batch['winner'] == batch else 'l', matchID_updated_count = match_matchIDs_updated_count_)])
            except:
                match_history_io.find('MatchIDs').append(get_match_ID_xml_object(match_id, time_stamp, output = 'w' if mm_batch['winner'] == batch else 'l', matchID_updated_count = match_matchIDs_updated_count_))
            # Saving all details.
            save_account_info_xml_objects(mm_batch[batch][i], [info_io, mm_rank_info_io, pr_rank_info_io, cooldown_info_io, match_history_io, weekly_info_io])

#%%