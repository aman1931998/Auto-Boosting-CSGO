#%% Can be used to save databases
#%% INDEPENDENT
#%% READY FOR CURRENT TASK -> UPDATE PR AND MM RANKS

from tqdm import tqdm
import pandas as pd
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import os, shutil
import numpy as np
import cv2
import sys
from datetime import datetime

def prettify(elem):
    """
    Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


# # %%
# from account_loading_functions import load_match_history_database, load_full_account_database, load_mm_mismatch_history_database
# match_history = load_match_history_database()
# account_database = load_full_account_database()
# mm_mismatch_history = load_mm_mismatch_history_database()

open_database_path = os.path.join('database', 'open_database')
match_history_path = os.path.join('database', 'matches_data')
mm_mismatch_history_path = os.path.join('database', 'mm_mismatch_data')

def save_match_history_database(match_history, match_history_path):
    for match_ID in tqdm(match_history.keys()): #match_ID = list(match_history.keys())[0]
        # print(match_ID)
        match_data = match_history[match_ID]
        save_match_history_data(match_data, match_history_path)
    
def save_mm_mismatch_history_database(mm_mismatch_history, mm_mismatch_history_path):
    for mm_mismatch_ID in tqdm(mm_mismatch_history): #mm_mismatch_ID = list(mm_mismatch_history.keys())[0]
        # print(mm_mismatch_ID)
        mismatch_data = mm_mismatch_history[mm_mismatch_ID]
        save_mm_mismatch_history_data(mismatch_data, mm_mismatch_history_path)

def save_account_database(account_database, open_database_path):
    for username in tqdm(account_database):
        # print(username)
        account_data = account_database[username]
        save_account_data(account_data, open_database_path)

#%%
# account_data = account_database['bleach0050transport52']

def save_account_data(account_data, open_database_path):
    # info
    if 'info' in account_data.keys():
        account_root = ET.Element('Acccount_Details')
        account_steam_id = ET.SubElement(account_root, 'SteamID')
        account_steam_id.text = str(account_data['info']['SteamID'])
        account_username = ET.SubElement(account_root, 'Username')
        account_username.text = str(account_data['info']['Username'])
        account_password = ET.SubElement(account_root, 'Password')
        account_password.text = str(account_data['info']['Password'])
        account_email_address = ET.SubElement(account_root, 'Email_Address')
        account_email_address.text = str(account_data['info']['Email_Address'])
        account_email_password = ET.SubElement(account_root, 'Email_Password')
        account_email_password.text = str(account_data['info']['Email_Password'])
        account_mm_rank = ET.SubElement(account_root, 'MM_Rank')
        account_mm_rank.text = str(account_data['info']['MM_Rank'])
        account_mm_wins = ET.SubElement(account_root, 'MM_Wins')
        account_mm_wins.text = str(account_data['info']['MM_Wins'])
        account_pr_rank = ET.SubElement(account_root, 'PR_Rank')
        account_pr_rank.text = str(account_data['info']['PR_Rank'])
        
        account_target_pr_rank = ET.SubElement(account_root, 'Target_PR_Rank')
        account_target_pr_rank.text = str(account_data['info']['Target_PR_Rank'])
        
        account_friend_code = ET.SubElement(account_root, 'Friend_Code')
        account_friend_code.text = str(account_data['info']['Friend_Code'])

        account_steam_profile_link = ET.SubElement(account_root, 'Steam_Profile_Link')
        account_steam_profile_link.text = str(account_data['info']['Steam_Profile_Link'])

        account_last_mm_rank_updated_time = ET.SubElement(account_root, 'Last_MM_Rank_Updated_Time')
        account_last_mm_rank_updated_time.text = str(account_data['info']['Last_MM_Rank_Updated_Time'])
        
        account_last_cooldown_type = ET.SubElement(account_root, 'Last_Cooldown_Type')
        account_last_cooldown_type.text = str(account_data['info']['Last_Cooldown_Type'])
        
        account_last_cooldown_time = ET.SubElement(account_root, 'Last_Cooldown_Time')
        account_last_cooldown_time.text = str(account_data['info']['Last_Cooldown_Time'])
        
        account_total_inventory_count = ET.SubElement(account_root, 'Total_Inventory_Count')
        account_total_inventory_count.text = str(account_data['info']['Total_Inventory_Count'])
        with open(os.path.join(open_database_path, account_data['info']['Username'], 'info.xml'), 'w') as file:
            file.write(prettify(account_root))
        
        # trade_info 
        
        # mm_rank_info
    if 'mm_rank_info' in account_data.keys():
        account_mm_rank_root = ET.Element('Account_MM_Rank_Details')
        
        account_mm_rank_mm_wins = ET.SubElement(account_mm_rank_root, 'MM_Wins')
        account_mm_rank_mm_wins.text = str(account_data['mm_rank_info']['MM_Wins'])
        account_mm_rank_mm_rank = ET.SubElement(account_mm_rank_root, 'MM_Rank')
        account_mm_rank_mm_rank.text = str(account_data['mm_rank_info']['MM_Rank'])
        
        account_mm_rank_last_mm_rank_updated_time = ET.SubElement(account_mm_rank_root, 'Last_MM_Rank_Updated_Time')
        account_mm_rank_last_mm_rank_updated_time.text = str(account_data['mm_rank_info']['Last_MM_Rank_Updated_Time'])
        
        account_mm_rank_last_mm_rank_update_matchID = ET.SubElement(account_mm_rank_root, 'Last_MM_Rank_Update_MatchID')
        account_mm_rank_last_mm_rank_update_matchID.text = str(account_data['mm_rank_info']['Last_MM_Rank_Update_MatchID'])
        
        account_mm_rank_rank_opened = ET.SubElement(account_mm_rank_root, 'Rank_Opened')
        account_mm_rank_rank_opened.text = str(account_data['mm_rank_info']['Rank_Opened'])
        
        account_mm_rank_rank_opened_date = ET.SubElement(account_mm_rank_root, 'Rank_Opened_Date')
        account_mm_rank_rank_opened_date.text = str(account_data['mm_rank_info']['Rank_Opened_Date'])
        
        account_mm_rank_rank_opened_matchID = ET.SubElement(account_mm_rank_root, 'Rank_Opened_MatchID')
        account_mm_rank_rank_opened_matchID.text = str(account_data['mm_rank_info']['Rank_Opened_MatchID'])
        
        account_mm_rank_mm_rank_history = ET.SubElement(account_mm_rank_root, 'MM_Rank_History')
        
        for index in account_data['mm_rank_info']['MM_Rank_History'].keys(): #index = list(account_data['mm_rank_info']['MM_Rank_History'].keys())[0]
            mm_rank_obj = ET.Element("Rank", attrib = {"Index": str(index)})
            mm_rank_obj.text = str(account_data['mm_rank_info']['MM_Rank_History'][index])
            account_mm_rank_mm_rank_history.extend([mm_rank_obj])
        
        account_mm_rank_mm_rank_time_history = ET.SubElement(account_mm_rank_root, 'MM_Rank_Time_History')
        
        for index in account_data['mm_rank_info']['MM_Rank_Time_History'].keys(): #index = list(account_data['mm_rank_info']['MM_Rank_Time_History'].keys())[0]
            datetime_obj = ET.Element('Time', attrib = {"Index":str(index)})
            datetime_obj.text = str(account_data['mm_rank_info']['MM_Rank_Time_History'][index])
            account_mm_rank_mm_rank_time_history.extend([datetime_obj])

        with open(os.path.join(open_database_path, account_data['info']['Username'], 'mm_rank_info.xml'), 'w') as file:
            file.write(prettify(account_mm_rank_root))
    
    # pr_rank_info
    if 'pr_rank_info' in account_data.keys():
        account_pr_rank_root = ET.Element('Account_PR_Rank_Details')
        
        account_pr_rank_pr_rank = ET.SubElement(account_pr_rank_root, 'PR_Rank')
        account_pr_rank_pr_rank.text = str(account_data['pr_rank_info']['PR_Rank'])
        
        account_pr_rank_xp_gained_for_next_rank = ET.SubElement(account_pr_rank_root, 'XP_Gained_For_Next_Rank')
        account_pr_rank_xp_gained_for_next_rank.text = str(account_data['pr_rank_info']['XP_Gained_For_Next_Rank'])
        
        account_pr_rank_current_week_number = ET.SubElement(account_pr_rank_root, 'Current_Week_Number')
        account_pr_rank_current_week_number.text = str(account_data['pr_rank_info']['Current_Week_Number'])
        
        account_pr_rank_current_week_match_count = ET.SubElement(account_pr_rank_root, 'Current_Week_Number_Match_Count')
        account_pr_rank_current_week_match_count.text = str(account_data['pr_rank_info']['Current_Week_Number_Match_Count'])
        
        account_pr_rank_pr_rank_history = ET.SubElement(account_pr_rank_root, 'PR_Rank_History')
        
        for index in account_data['pr_rank_info']['PR_Rank_History'].keys(): #index = list(account_data['pr_rank_info']['PR_Rank_History'].keys())[0]

            week_index = ET.Element('Week', attrib = {"Index": index})
            week_start_datestamp = ET.SubElement(week_index, 'Week_Start_Datestamp')
            week_start_datestamp.text = str(account_data['pr_rank_info']['PR_Rank_History'][index]['Week_Start_Datestamp'])
            week_xp_gained = ET.SubElement(week_index, 'Weekly_XP_Gained')
            week_xp_gained.text = str(account_data['pr_rank_info']['PR_Rank_History'][index]['Weekly_XP_Gained'])
            account_pr_rank_pr_rank_history.extend([week_index])
        with open(os.path.join(open_database_path, account_data['info']['Username'], 'pr_rank_info.xml'), 'w') as file:
            file.write(prettify(account_pr_rank_root))
    
    # match_history
    if 'match_history' in account_data.keys():
        account_match_history_root = ET.Element('Account_Match_History_Details')
        
        account_match_history_match_count = ET.SubElement(account_match_history_root, 'Match_Count')
        account_match_history_match_count.text = str(account_data['match_history']['Match_Count'])
        
        account_match_history_matchIDs = ET.SubElement(account_match_history_root, 'MatchIDs')
        
        for index in account_data['match_history']['MatchIDs'].keys(): #index = '1'
            match_index = ET.Element('Match', attrib = {"Index": str(index)})
            mid = ET.SubElement(match_index, 'MatchID')
            mid.text = str(account_data['match_history']['MatchIDs'][index]['MatchID'])
            mdatestamp = ET.SubElement(match_index, 'Datestamp')
            mdatestamp.text = str(account_data['match_history']['MatchIDs'][index]['Datestamp'])
            moutput = ET.SubElement(match_index, 'Output')
            moutput.text = str(account_data['match_history']['MatchIDs'][index]['Output'])
            account_match_history_matchIDs.extend([match_index])
        with open(os.path.join(open_database_path, account_data['info']['Username'], 'match_history.xml'), 'w') as file:
            file.write(prettify(account_match_history_root))

        # cooldown_info
    if 'cooldown_info' in account_data.keys(): 
        account_cooldown_root = ET.Element('Account_Cooldown_Details')
        
        account_cooldown_last_cooldown_type = ET.SubElement(account_cooldown_root, 'Last_Cooldown_Type')
        account_cooldown_last_cooldown_type.text = str(account_data['cooldown_info']['Last_Cooldown_Type'])
        
        account_cooldown_last_cooldown_time = ET.SubElement(account_cooldown_root, 'Last_Cooldown_Time')
        account_cooldown_last_cooldown_time.text = str(account_data['cooldown_info']['Last_Cooldown_Time']) #"No Info"
        
        account_cooldown_cooldown_type_history = ET.SubElement(account_cooldown_root, 'Cooldown_Type_History')
        
        for index in account_data['cooldown_info']['Cooldown_Type_History'].keys(): #index = list(account_data['cooldown_info']['Cooldown_Type_History'])[0]
            cooldown_type_obj = ET.Element('Type', attrib = {"Index": str(index)})
            cooldown_type_obj.text = str(account_data['cooldown_info']['Cooldown_Type_History'][index])
            account_cooldown_cooldown_type_history.extend([cooldown_type_obj])

        
        account_cooldown_cooldown_time_history = ET.SubElement(account_cooldown_root, 'Cooldown_Time_History')

        for index in account_data['cooldown_info']['Cooldown_Time_History'].keys(): #index = list(account_data['cooldown_info']['Cooldown_Time_History'])[0]
            cooldown_time_obj = ET.Element('Time', attrib = {"Index": str(index)})
            cooldown_time_obj.text = str(account_data['cooldown_info']['Cooldown_Time_History'][index])
            account_cooldown_cooldown_time_history.extend([cooldown_time_obj])

        
        account_cooldown_cooldown_matchID_history = ET.SubElement(account_cooldown_root, 'Cooldown_MatchID_History')

        for index in account_data['cooldown_info']['Cooldown_MatchID_History'].keys(): #index = list(account_data['cooldown_info']['Cooldown_MatchID_History'])[0]
            cooldown_matchID_obj = ET.Element('MatchID', attrib = {"Index": str(index)})
            cooldown_matchID_obj.text = account_data['cooldown_info']['Cooldown_MatchID_History'][index]
            account_cooldown_cooldown_matchID_history.extend([cooldown_matchID_obj])

        
        with open(os.path.join(open_database_path, account_data['info']['Username'], 'cooldown_info.xml'), 'w') as file:
            file.write(prettify(account_cooldown_root))
    
        # weekly_info
    if 'weekly_info' in account_data.keys():
        account_weekly_root = ET.Element('Account_Weekly_Details')
        
        account_weekly_current_week_number = ET.SubElement(account_weekly_root, "Current_Week_Number")
        account_weekly_current_week_number.text = str(account_data['weekly_info']['Current_Week_Number'])
        account_weekly_current_week_number_match_count = ET.SubElement(account_weekly_root, "Current_Week_Number_Match_Count")
        account_weekly_current_week_number_match_count.text = str(account_data['weekly_info']['Current_Week_Number_Match_Count'])
        
        account_weekly_detailed_info = ET.SubElement(account_weekly_root, "Detailed_Info")
        
        for index in account_data['weekly_info']['Detailed_Info'].keys(): #index = list(account_data['weekly_info']['Detailed_Info'].keys())[0]
            week_index = ET.Element('Week', attrib = {"Index": index})
            week_match_count_ = ET.SubElement(week_index, 'Week_Match_Count')
            week_match_count_.text = str(account_data['weekly_info']['Detailed_Info'][index]['Week_Match_Count'])
            week_IDs_ = ET.SubElement(week_index, 'IDs')
            account_weekly_detailed_info.extend([week_index])
        
        with open(os.path.join(open_database_path, account_data['info']['Username'], 'weekly_info.xml'), 'w') as file:
            file.write(prettify(account_weekly_root))

        # error_info

        # mismatch_info



#%%
# match_data = match_history['match_5e9212ec7048d9d0a5b9086c7291546a']

def save_match_history_data(match_data, match_history_path):

    log_match_root = ET.Element("Match_Details")                               ###

    log_match_match_ID = ET.SubElement(log_match_root, "MatchID")
    log_match_match_ID.text = str(match_data['MatchID'])

    log_match_team_1 = ET.SubElement(log_match_root, 'Team_1')                 ###
    log_match_team_2 = ET.SubElement(log_match_root, 'Team_2')                 ###

    log_match_team_1_lobby_leader = ET.SubElement(log_match_team_1, "Lobby_Leader")
    log_match_team_1_lobby_leader.text = str(match_data['Team_1']['Lobby_Leader'])
    log_match_team_2_lobby_leader = ET.SubElement(log_match_team_2, "Lobby_Leader")
    log_match_team_2_lobby_leader.text = str(match_data['Team_2']['Lobby_Leader'])

    log_match_teammates_1 = ET.SubElement(log_match_team_1, 'Players')
    log_match_teammates_2 = ET.SubElement(log_match_team_2, 'Players')
    log_match_team_1_players, log_match_team_2_players = [], []
    
    for i in range(5): #i = 0
        log_match_player = ET.Element("Player_%d"%(i+1))
        log_match_player_username = ET.SubElement(log_match_player, "Username")
        log_match_player_username.text = str(match_data['Team_1']['Players']["Player_%d"%(i+1)]['Username'])
        log_match_player_mm_rank = ET.SubElement(log_match_player, "MM_Rank")
        log_match_player_mm_rank.text = str(match_data['Team_1']['Players']["Player_%d"%(i+1)]['MM_Rank'])
        log_match_player_mm_rank_update = ET.SubElement(log_match_player, "MM_Rank_Update")
        log_match_player_mm_rank_update.text = str(match_data['Team_1']['Players']["Player_%d"%(i+1)]['MM_Rank_Update'])
        log_match_player_pr_rank = ET.SubElement(log_match_player, "PR_Rank")
        log_match_player_pr_rank.text = str(match_data['Team_1']['Players']["Player_%d"%(i+1)]['PR_Rank'])
        log_match_player_pr_rank_update = ET.SubElement(log_match_player, "PR_Rank_Update")
        log_match_player_pr_rank_update.text = str(match_data['Team_1']['Players']["Player_%d"%(i+1)]['PR_Rank_Update'])
        log_match_player_match_number = ET.SubElement(log_match_player, "Match_Number")
        log_match_player_match_number.text = str(match_data['Team_1']['Players']["Player_%d"%(i+1)]['Match_Number'])
        log_match_player_week_number = ET.SubElement(log_match_player, "Week_Number")
        log_match_player_week_number.text = str(match_data['Team_1']['Players']["Player_%d"%(i+1)]['Week_Number'])
        log_match_player_week_match_number = ET.SubElement(log_match_player, "Week_Match_Number")
        log_match_player_week_match_number.text = str(match_data['Team_1']['Players']["Player_%d"%(i+1)]['Week_Match_Number'])
        log_match_player_xp_earned = ET.SubElement(log_match_player, "XP_Gained")
        log_match_player_xp_earned.text = str(match_data['Team_1']['Players']["Player_%d"%(i+1)]['XP_Gained'])
        log_match_team_1_players.append(log_match_player)

        log_match_player = ET.Element("Player_%d"%(i+1))
        log_match_player_username = ET.SubElement(log_match_player, "Username")
        log_match_player_username.text = str(match_data['Team_2']['Players']["Player_%d"%(i+1)]['Username'])
        log_match_player_mm_rank = ET.SubElement(log_match_player, "MM_Rank")
        log_match_player_mm_rank.text = str(match_data['Team_2']['Players']["Player_%d"%(i+1)]['MM_Rank'])
        log_match_player_mm_rank_update = ET.SubElement(log_match_player, "MM_Rank_Update")
        log_match_player_mm_rank_update.text = str(match_data['Team_2']['Players']["Player_%d"%(i+1)]['MM_Rank_Update'])
        log_match_player_pr_rank = ET.SubElement(log_match_player, "PR_Rank")
        log_match_player_pr_rank.text = str(match_data['Team_2']['Players']["Player_%d"%(i+1)]['PR_Rank'])
        log_match_player_pr_rank_update = ET.SubElement(log_match_player, "PR_Rank_Update")
        log_match_player_pr_rank_update.text = str(match_data['Team_2']['Players']["Player_%d"%(i+1)]['PR_Rank_Update'])
        log_match_player_match_number = ET.SubElement(log_match_player, "Match_Number")
        log_match_player_match_number.text = str(match_data['Team_2']['Players']["Player_%d"%(i+1)]['Match_Number'])
        log_match_player_week_number = ET.SubElement(log_match_player, "Week_Number")
        log_match_player_week_number.text = str(match_data['Team_2']['Players']["Player_%d"%(i+1)]['Week_Number'])
        log_match_player_week_match_number = ET.SubElement(log_match_player, "Week_Match_Number")
        log_match_player_week_match_number.text = str(match_data['Team_2']['Players']["Player_%d"%(i+1)]['Week_Match_Number'])
        log_match_player_xp_earned = ET.SubElement(log_match_player, "XP_Gained")
        log_match_player_xp_earned.text = str(match_data['Team_2']['Players']["Player_%d"%(i+1)]['XP_Gained'])
        log_match_team_2_players.append(log_match_player)
    log_match_teammates_1.extend(log_match_team_1_players)
    log_match_teammates_2.extend(log_match_team_2_players)

    dstamp = ET.Element('Timestamp')
    dstamp.text = str(match_data['Timestamp'])
    log_match_root.append(dstamp)
    
    log_match_search_details = ET.SubElement(log_match_root, "Search_Details")
    log_match_search_start_time = ET.SubElement(log_match_search_details, "Search_Start_Time")
    log_match_search_start_time.text = str(match_data['Search_Details']['Search_Start_Time'])
    log_match_search_error_count = ET.SubElement(log_match_search_details, "Search_Error_Count")
    log_match_search_error_count.text = str(match_data['Search_Details']['Search_Error_Count'])
    log_match_search_mismatchID = ET.SubElement(log_match_search_details, 'MM_MismatchID')
    log_match_search_mismatchID.text = str(match_data['Search_Details']['MM_MismatchID'])
    # log_match_search_error_details = get_search_error_details_xml_object(search_error_details)
    # log_match_search_details.append(log_match_search_error_details)
    log_match_search_end_time = ET.SubElement(log_match_search_details, "Search_End_Time")
    log_match_search_end_time.text = str(match_data['Search_Details']['Search_End_Time'])
    log_match_search_duration = ET.SubElement(log_match_search_details, "Search_Duration")
    log_match_search_duration.text = str(match_data['Search_Details']['Search_Duration'])   ###!~!
    
    log_match_time_details = ET.SubElement(log_match_root, "Match_Time_Details")
    log_match_start_time = ET.SubElement(log_match_time_details, "Match_Start_Time")
    log_match_start_time.text = str(match_data['Match_Time_Details']['Match_Start_Time'])
    log_match_end_time = ET.SubElement(log_match_time_details, "Match_End_Time")
    log_match_end_time.text = str(match_data['Match_Time_Details']['Match_End_Time'])
    log_match_duration = ET.SubElement(log_match_time_details, "Match_Duration")
    log_match_duration.text = str(match_data['Match_Time_Details']['Match_Duration'])  ###~!
    
    with open(os.path.join(match_history_path, str(match_data['MatchID']) + '.xml'), 'w') as file:
        file.write(prettify(log_match_root))


#%%
# mismatch_data = mm_mismatch_history['mismatch_81f354109d24bba7']

def save_mm_mismatch_history_data(mismatch_data, mm_mismatch_history_path):

    log_mismatch = ET.Element('Mismatch_Details')
    
    log_mismatch_mismatchID = ET.SubElement(log_mismatch, 'MismatchID')
    log_mismatch_mismatchID.text = str(mismatch_data['MismatchID'])
    log_mismatch_match_found = ET.SubElement(log_mismatch, 'Match_Found')
    log_mismatch_match_found.text = str(mismatch_data['Match_Found'])
    log_mismatch_team_1 = ET.SubElement(log_mismatch, 'Team1')
    log_mismatch_team_1_list = []
    for i in range(5):#i = 0
        ll = ET.Element("Player", attrib = {"Index": str(i+1)})
        ll.text  = str(mismatch_data['Team1'][i])
        log_mismatch_team_1_list.append(ll)
    log_mismatch_team_1.extend(log_mismatch_team_1_list)
    log_mismatch_team_2 = ET.SubElement(log_mismatch, 'Team2')
    log_mismatch_team_2_list = []
    for i in range(5):#i = 0
        ll = ET.Element("Player", attrib = {"Index": str(i+1)})
        ll.text  = mismatch_data['Team2'][i]
        log_mismatch_team_2_list.append(ll)
    log_mismatch_team_2.extend(log_mismatch_team_2_list)
    log_mismatch_total_search_time = ET.SubElement(log_mismatch, 'Total_Search_Time')
    log_mismatch_total_search_time.text = str(mismatch_data['Total_Search_Time'])

    log_mismatch_history = ET.Element('History')
    if len(mismatch_data['History'].keys()) == 0:
        log_mismatch_history.text = "No Error"
    else:
        log_mismatch_history_list = []
        for key in mismatch_data['History'].keys(): #key = list(mismatch_data['History'].keys())[0]
            mismatch_history_node_obj = ET.Element('Mismatch', attrib = {"Index":str(key)})
            mismatch_history_node_match_found_for_obj = ET.SubElement(mismatch_history_node_obj, 'Match_Found_For')
            mismatch_history_node_match_found_for_obj.text = str(mismatch_data['History'][key]['Match_Found_For'])
            mismatch_history_node_match_timestamp_recorded_obj = ET.SubElement(mismatch_history_node_obj, 'Timestamp_Recorded')
            mismatch_history_node_match_timestamp_recorded_obj.text = str(mismatch_data['History'][key]['Timestamp_Recorded'])
            log_mismatch_history_list.append(mismatch_history_node_obj)
        log_mismatch_history.extend(log_mismatch_history_list)

    log_mismatch.append(log_mismatch_history)
    
    with open(os.path.join(mm_mismatch_history_path, str(mismatch_data['MismatchID']) + '.xml'), 'w') as file:
        file.write(prettify(log_mismatch))
























