#%% Can be used to load databases
#%% INDEPENDENT
#%% READY FOR CURRENT TASK -> UPDATE PR AND MM RANKS

from tqdm import tqdm
import pandas as pd
import xml.etree.ElementTree as ET
import os, shutil
import numpy as np
import cv2
import sys
from datetime import datetime, timedelta
from project_path import steam_path

def load_usernames():
    return pd.read_excel(os.path.join('database', 'batch_2.xlsx'))['Username'].tolist()


def full_account_data(username, open_database_path):
    account_data_path = os.path.join(open_database_path, username)
    username = {"cooldown_info": {}, 
                # "error_info": {}, 
                "info": {}, 
                "match_history": {}, 
                #"mismatch_info": {}, 
                "mm_rank_info": {}, 
                "pr_rank_info": {}, 
                #"trade_info": {}, 
                "weekly_info": {}
                }
    #%% cooldown_info
    # print("Cooldown")
    cooldown_info_io = open(os.path.join(account_data_path, "cooldown_info.xml"), 'r')
    cooldown_info_obj = ET.parse(cooldown_info_io).getroot()
    cooldown_info_io.close()
    
    username['cooldown_info']['Last_Cooldown_Type'] = cooldown_info_obj.find('Last_Cooldown_Type').text

    username['cooldown_info']['Last_Cooldown_Time'] = datetime.strptime(cooldown_info_obj.find('Last_Cooldown_Time').text, "%Y-%m-%d %H:%M:%S.%f")

    username['cooldown_info']['Cooldown_Type_History'] = {}
    for obj in cooldown_info_obj.find('Cooldown_Type_History').getchildren(): #obj = cooldown_info_obj.find('Cooldown_Type_History').getchildren()[0]
        index = str(cooldown_info_obj.find('Cooldown_Type_History').getchildren().index(obj) + 1)
        cooldown_type = obj.text
        username['cooldown_info']['Cooldown_Type_History'][index] = cooldown_type

    username['cooldown_info']['Cooldown_Time_History'] = {}
    for obj in cooldown_info_obj.find('Cooldown_Time_History').getchildren(): #obj = cooldown_info_obj.find('Cooldown_Time_History').getchildren()[0]
        index = str(cooldown_info_obj.find('Cooldown_Time_History').getchildren().index(obj) + 1)
        cooldown_time = datetime.strptime(obj.text, "%Y-%m-%d %H:%M:%S.%f")
        username['cooldown_info']['Cooldown_Time_History'][index] = cooldown_time
    
    username['cooldown_info']['Cooldown_MatchID_History'] = {}
    for obj in cooldown_info_obj.find('Cooldown_MatchID_History').getchildren(): #obj = cooldown_info_obj.find('Cooldown_MatchID_History').getchildren()[0]
        index = str(cooldown_info_obj.find('Cooldown_MatchID_History').getchildren().index(obj) + 1)
        cooldown_matchID = obj.text
        username['cooldown_info']['Cooldown_MatchID_History'][index] = cooldown_matchID
    
    #%% weekly_info
    # print("Weekly")
    weekly_info_io = open(os.path.join(account_data_path, "weekly_info.xml"), 'r')
    weekly_info_obj = ET.parse(weekly_info_io).getroot()
    weekly_info_io.close()
    
    username['weekly_info']['Current_Week_Number'] = weekly_info_obj.find('Current_Week_Number').text
    username['weekly_info']['Current_Week_Number_Match_Count'] = weekly_info_obj.find('Current_Week_Number_Match_Count').text
    
    username['weekly_info']['Detailed_Info'] = {}
    for obj in weekly_info_obj.find('Detailed_Info').getchildren(): #obj = weekly_info_obj.find('Detailed_Info').getchildren()[0]
        index = str(weekly_info_obj.find('Detailed_Info').getchildren().index(obj) + 1)
        week_match_count = int(obj.find('Week_Match_Count').text)
        IDs = obj.find('IDs').text
        username['weekly_info']['Detailed_Info'][index] = {}
        username['weekly_info']['Detailed_Info'][index]['Week_Match_Count'] = week_match_count
        username['weekly_info']['Detailed_Info'][index]['IDs'] = IDs
    
    #%% pr_rank_info
    # print("PR_RANK")
    pr_rank_info_io = open(os.path.join(account_data_path, 'pr_rank_info.xml'), 'r')
    pr_rank_info_obj = ET.parse(pr_rank_info_io).getroot()
    pr_rank_info_io.close()
    
    username['pr_rank_info']['PR_Rank'] = pr_rank_info_obj.find('PR_Rank').text
    username['pr_rank_info']['XP_Gained_For_Next_Rank'] = pr_rank_info_obj.find('XP_Gained_For_Next_Rank').text
    username['pr_rank_info']['Current_Week_Number'] = pr_rank_info_obj.find('Current_Week_Number').text
    username['pr_rank_info']['Current_Week_Number_Match_Count'] = pr_rank_info_obj.find('Current_Week_Number_Match_Count').text
    
    username['pr_rank_info']['PR_Rank_History'] = {}
    for obj in pr_rank_info_obj.find('PR_Rank_History').getchildren(): #obj = pr_rank_info_obj.find('PR_Rank_History').getchildren()[0]
        index = str(pr_rank_info_obj.find('PR_Rank_History').getchildren().index(obj) + 1)
        week_start_datestamp = datetime.strptime(obj.find('Week_Start_Datestamp').text, "%Y-%m-%d %H:%M:%S")
        weekly_xp_gained = obj.find('Weekly_XP_Gained').text
        username['pr_rank_info']['PR_Rank_History'][index] = {}
        username['pr_rank_info']['PR_Rank_History'][index]['Week_Start_Datestamp'] = week_start_datestamp
        username['pr_rank_info']['PR_Rank_History'][index]['Weekly_XP_Gained'] = weekly_xp_gained
    
    #%% mm_rank_info
    # print("MM_RANk")
    mm_rank_info_io = open(os.path.join(account_data_path, 'mm_rank_info.xml'), 'r')
    mm_rank_info_obj = ET.parse(mm_rank_info_io).getroot()
    mm_rank_info_io.close()
    
    username['mm_rank_info']['MM_Wins'] = mm_rank_info_obj.find('MM_Wins').text
    username['mm_rank_info']['MM_Rank'] = mm_rank_info_obj.find('MM_Rank').text
    try:
        username['mm_rank_info']['Last_MM_Rank_Updated_Time'] = datetime.strptime(mm_rank_info_obj.find('Last_MM_Rank_Updated_Time').text, "%Y-%m-%d %H:%M:%S.%f")
    except:
        username['mm_rank_info']['Last_MM_Rank_Updated_Time'] = mm_rank_info_obj.find('Last_MM_Rank_Updated_Time').text
    username['mm_rank_info']['Last_MM_Rank_Update_MatchID'] = mm_rank_info_obj.find('Last_MM_Rank_Update_MatchID').text
    username['mm_rank_info']['Rank_Opened'] = mm_rank_info_obj.find('Rank_Opened').text
    try:
        username['mm_rank_info']['Rank_Opened_Date'] = datetime.strptime(mm_rank_info_obj.find('Rank_Opened_Date').text, "%Y-%m-%d %H:%M:%S.%f")
    except:
        username['mm_rank_info']['Rank_Opened_Date'] = mm_rank_info_obj.find('Rank_Opened_Date').text
    username['mm_rank_info']['Rank_Opened_MatchID'] = mm_rank_info_obj.find('Rank_Opened_MatchID').text
    
    username['mm_rank_info']['MM_Rank_History'] = {}    
    for obj in mm_rank_info_obj.find('MM_Rank_History').getchildren(): #obj = mm_rank_info_obj.find('MM_Rank_History').getchildren()[0]
        index = str(mm_rank_info_obj.find('MM_Rank_History').getchildren().index(obj) + 1)                                         # cooldown_info_obj.findall('Cooldown_Type_History')[0]
        # if obj.attrib['Index'] in username['mm_rank_info']['MM_Rank_History'].keys():
        #     index += "_" * list(username['mm_rank_info']['MM_Rank_History'].keys()).count(index)
        rank = obj.text
        #print(index)
        username['mm_rank_info']['MM_Rank_History'][index] = rank

    username['mm_rank_info']['MM_Rank_Time_History'] = {}    
    for obj in mm_rank_info_obj.find('MM_Rank_Time_History').getchildren(): #obj = mm_rank_info_obj.find('MM_Rank_History').getchildren()[0]
        index = str(mm_rank_info_obj.find('MM_Rank_Time_History').getchildren().index(obj) + 1)                                         # cooldown_info_obj.findall('Cooldown_Type_History')[0]
        # if obj.attrib['Index'] in username['mm_rank_info']['MM_Rank_Time_History'].keys():
        #     index += "_" * list(username['mm_rank_info']['MM_Rank_Time_History'].keys()).count(index)
        rank_datetime = datetime.strptime(obj.text, "%Y-%m-%d %H:%M:%S.%f")
        #print(index)
        username['mm_rank_info']['MM_Rank_Time_History'][index] = rank_datetime
    
    #%% mismatch_info
    # print("MM_MISMATCH")
    # mismatch_info_io = open(os.path.join(account_data_path, 'mismatch_info.xml'), 'r')
    # mismatch_info_obj = ET.parse(mismatch_info_io).getroot()
    # mismatch_info_io.close()
    
    # username['mismatch_info']['MM_Mismatch_Count'] = mismatch_info_obj.find('MM_Mismatch_Count').text
    # username['mismatch_info']['Last_MM_Mismatch_ID'] = mismatch_info_obj.find('Last_MM_Mismatch_ID').text
    # try:
    #     username['mismatch_info']['Last_MM_Mismatch_Timestamp'] = datetime.strptime(mismatch_info_obj.find('Last_MM_Mismatch_Timestamp').text, "%Y-%m-%d %H:%M:%S")
    # except:
    #     username['mismatch_info']['Last_MM_Mismatch_Timestamp'] = mismatch_info_obj.find('Last_MM_Mismatch_Timestamp').text #"No Info"
    
    # username['mismatch_info']['MM_Mismatch_History'] = {}
    
    #%% match_history
    # print("Match_History")
    match_history_io = open(os.path.join(account_data_path, 'match_history.xml'), 'r')
    match_history_obj = ET.parse(match_history_io).getroot()
    match_history_io.close()
    
    username['match_history']['Match_Count'] = int(match_history_obj.find('Match_Count').text)
    
    username['match_history']['MatchIDs'] = {}
    
    for obj in match_history_obj.find('MatchIDs').getchildren(): #obj = match_history_obj.find('MatchIDs').getchildren()[0]
        index = str(match_history_obj.find('MatchIDs').getchildren().index(obj) + 1)
        username['match_history']['MatchIDs'][index] = {}
        matchID = obj.find('MatchID').text
        datestamp = datetime.strptime(obj.find('Datestamp').text, "%Y-%m-%d %H:%M:%S.%f")
        output = obj.find('Output').text
        username['match_history']['MatchIDs'][index]['MatchID'] = matchID
        username['match_history']['MatchIDs'][index]['Datestamp'] = datestamp
        username['match_history']['MatchIDs'][index]['Output'] = output
    
    #%% info
    # print("Info")
    info_io = open(os.path.join(account_data_path, 'info.xml'), 'r')
    info_obj = ET.parse(info_io).getroot()
    info_io.close()
    
    username['info']['SteamID'] = info_obj.find('SteamID').text
    username['info']['Username'] = info_obj.find('Username').text
    username['info']['Password'] = info_obj.find('Password').text
    username['info']['Email_Address'] = info_obj.find('Email_Address').text
    username['info']['Email_Password'] = info_obj.find('Email_Password').text
    username['info']['MM_Rank'] = info_obj.find('MM_Rank').text
    username['info']['MM_Wins'] = info_obj.find('MM_Wins').text
    username['info']['PR_Rank'] = info_obj.find('PR_Rank').text
    username['info']['Target_PR_Rank'] = info_obj.find('Target_PR_Rank').text
    username['info']['Friend_Code'] = info_obj.find('Friend_Code').text
    username['info']['Steam_Profile_Link'] = info_obj.find('Steam_Profile_Link').text
    username['info']['Last_MM_Rank_Updated_Time'] = datetime.strptime(info_obj.find('Last_MM_Rank_Updated_Time').text, "%Y-%m-%d %H:%M:%S.%f")
    username['info']['Last_Cooldown_Type'] = info_obj.find('Last_Cooldown_Type').text
    username['info']['Last_Cooldown_Time'] = datetime.strptime(info_obj.find('Last_Cooldown_Time').text, "%Y-%m-%d %H:%M:%S.%f")
    username['info']['Total_Inventory_Count'] = info_obj.find('Total_Inventory_Count').text
    
    #%% trade_info
    # print("Trade Info")
    # trade_info_io = open(os.path.join(account_data_path, 'trade_info.xml'), 'r')
    # trade_info_obj = ET.parse(trade_info_io).getroot()
    # trade_info_io.close()
    
    # username['trade_info']['Trade_Url'] = trade_info_obj.find('Trade_Url').text
    # username['trade_info']['Total_Inventory_Count'] = trade_info_obj.find('Total_Inventory_Count').text

    # username['trade_info']['Inventory_Items'] = {}

    # username['trade_info']['Last_Trade_Date'] = trade_info_obj.find('Last_Trade_Date').text
    # username['trade_info']['Last_Trade_Item_Count'] = trade_info_obj.find('Last_Trade_Item_Count').text
    # username['trade_info']['Last_Trade_TradeOfferID'] = trade_info_obj.find('Last_Trade_TradeOfferID').text

    # #%%
    # username['trade_info']['Trade_Date_History'] = {}
    # username['trade_info']['Trade_Items_History'] = {}
    # username['trade_info']['Trade_TradeOfferIDs'] = {}
    return username


def load_full_account_database(usernames = load_usernames()):
    open_database_path = os.path.join('database', 'open_database')
    account_database = {}
    for username in tqdm(usernames): #username = usernames[155]
        # print(username)
        account_database[username] = full_account_data(username, open_database_path)
    
    return account_database

def load_match_history_database(match_history_path = os.path.join('database', 'matches_data')):
    match_IDs = os.listdir(match_history_path)
    matches_database = {}
    for match_ID in tqdm(match_IDs): #match_ID = match_IDs[0]
        # print(match_ID)
        matches_database[match_ID.split('.')[0]] = load_match_history(match_ID, match_history_path)
    
    return matches_database


def load_mm_mismatch_history_database(mm_mismatch_history_path = os.path.join('database', 'mm_mismatch_data')):
    mm_mismatch_IDs = os.listdir(mm_mismatch_history_path)
    mm_mismatch_database = {}
    for mm_mismatch_ID in tqdm(mm_mismatch_IDs): #mm_mismatch_ID = mm_mismatch_IDs[0]
        # print(mm_mismatch_ID)
        mm_mismatch_database[mm_mismatch_ID.split('.')[0]] = load_mm_mismatch_history(mm_mismatch_ID, mm_mismatch_history_path)
    
    return mm_mismatch_database

def load_mm_mismatch_history(mm_mismatch_ID, mm_mismatch_history_path):
    mismatch_dict = {}
    #mm_mismatch_ID = 'mismatch_1b096f36bc91433e.xml'
    obj_io = open(os.path.join(mm_mismatch_history_path, mm_mismatch_ID), 'r')
    obj = ET.parse(obj_io).getroot()
    obj_io.close()
    
    mismatch_dict['MismatchID'] = mm_mismatch_ID.split('.')[0]
    mismatch_dict['Match_Found'] = obj.find('Match_Found').text
    team1_obj = obj.find('Team1')
    team2_obj = obj.find('Team2')
    mismatch_dict['Team1'] = []
    mismatch_dict['Team2'] = []
    for i in range(len(team1_obj.getchildren())): #player = team1_obj.getchildren()[0]
        mismatch_dict['Team1'].append(team1_obj.getchildren()[i].text)
        mismatch_dict['Team2'].append(team2_obj.getchildren()[i].text)
    mismatch_dict['Total_Search_Time'] = obj.find('Total_Search_Time').text
    mismatch_dict['History'] = {}
    for mh in obj.find('History').getchildren(): #mh = obj.find('History').getchildren()[0]
        index = obj.find('History').getchildren().index(mh)
        mismatch_dict['History'][str(index + 1)] = {"Match_Found_For": mh.find('Match_Found_For').text, 
                                                "Timestamp_Recorded": datetime.strptime(mh.find('Timestamp_Recorded').text, "%Y-%m-%d %H:%M:%S.%f")}
    return mismatch_dict

def load_match_history(match_ID, match_history_path):
    match_ID_dict = {}
    # match_ID = 'match_f9cfd0ef2b47d7aec9c48680cadcaeae.xml'
    obj_io = open(os.path.join(match_history_path, match_ID), 'r')
    obj = ET.parse(obj_io).getroot()
    obj_io.close()
    
    match_ID_dict['MatchID'] = match_ID.split('.')[0]
    
    team_1_obj = obj.find('Team_1')
    match_ID_dict['Team_1'] = {}
    match_ID_dict['Team_1']['Lobby_Leader'] = team_1_obj.find('Lobby_Leader').text
    team_1_players_obj = team_1_obj.find('Players')
    match_ID_dict['Team_1']['Players'] = {}
    for i in range(len(team_1_players_obj.getchildren())): #player = team_1_players_obj.getchildren()[0]
        player = team_1_players_obj.getchildren()[i]
        match_ID_dict['Team_1']['Players']['Player_%d'%(i+1)] = {}
        match_ID_dict['Team_1']['Players']['Player_%d'%(i+1)]['Username'] = player.find("Username").text
        match_ID_dict['Team_1']['Players']['Player_%d'%(i+1)]['MM_Rank'] = player.find("MM_Rank").text
        match_ID_dict['Team_1']['Players']['Player_%d'%(i+1)]['MM_Rank_Update'] = player.find("MM_Rank_Update").text
        match_ID_dict['Team_1']['Players']['Player_%d'%(i+1)]['PR_Rank'] = player.find("PR_Rank").text
        match_ID_dict['Team_1']['Players']['Player_%d'%(i+1)]['PR_Rank_Update'] = player.find("PR_Rank_Update").text
        match_ID_dict['Team_1']['Players']['Player_%d'%(i+1)]['Match_Number'] = player.find("Match_Number").text
        match_ID_dict['Team_1']['Players']['Player_%d'%(i+1)]['Week_Number'] = player.find("Week_Number").text
        match_ID_dict['Team_1']['Players']['Player_%d'%(i+1)]['Week_Match_Number'] = player.find("Week_Match_Number").text
        match_ID_dict['Team_1']['Players']['Player_%d'%(i+1)]['XP_Gained'] = player.find("XP_Gained").text

    team_2_obj = obj.find('Team_2')
    match_ID_dict['Team_2'] = {}
    match_ID_dict['Team_2']['Lobby_Leader'] = team_2_obj.find('Lobby_Leader').text
    team_2_players_obj = team_2_obj.find('Players')
    match_ID_dict['Team_2']['Players'] = {}
    for i in range(len(team_2_players_obj.getchildren())): #player = team_2_players_obj.getchildren()[0]
        player = team_2_players_obj.getchildren()[i]
        match_ID_dict['Team_2']['Players']['Player_%d'%(i+1)] = {}
        match_ID_dict['Team_2']['Players']['Player_%d'%(i+1)]['Username'] = player.find("Username").text
        match_ID_dict['Team_2']['Players']['Player_%d'%(i+1)]['MM_Rank'] = player.find("MM_Rank").text
        match_ID_dict['Team_2']['Players']['Player_%d'%(i+1)]['MM_Rank_Update'] = player.find("MM_Rank_Update").text
        match_ID_dict['Team_2']['Players']['Player_%d'%(i+1)]['PR_Rank'] = player.find("PR_Rank").text
        match_ID_dict['Team_2']['Players']['Player_%d'%(i+1)]['PR_Rank_Update'] = player.find("PR_Rank_Update").text
        match_ID_dict['Team_2']['Players']['Player_%d'%(i+1)]['Match_Number'] = player.find("Match_Number").text
        match_ID_dict['Team_2']['Players']['Player_%d'%(i+1)]['Week_Number'] = player.find("Week_Number").text
        match_ID_dict['Team_2']['Players']['Player_%d'%(i+1)]['Week_Match_Number'] = player.find("Week_Match_Number").text
        match_ID_dict['Team_2']['Players']['Player_%d'%(i+1)]['XP_Gained'] = player.find("XP_Gained").text
    
    match_ID_dict['Timestamp'] = datetime.strptime(obj.find('Timestamp').text, "%Y-%m-%d %H:%M:%S.%f")
    
    search_obj = obj.find('Search_Details')
    match_ID_dict['Search_Details'] = {}
    match_ID_dict['Search_Details']['Search_Start_Time'] = datetime.strptime(search_obj.find('Search_Start_Time').text, "%Y-%m-%d %H:%M:%S.%f")
    match_ID_dict['Search_Details']['Search_Error_Count'] = search_obj.find('Search_Error_Count').text
    match_ID_dict['Search_Details']['MM_MismatchID'] = search_obj.find('MM_MismatchID').text
    match_ID_dict['Search_Details']['Search_End_Time'] = datetime.strptime(search_obj.find('Search_End_Time').text, "%Y-%m-%d %H:%M:%S.%f")
    t = datetime.strptime(search_obj.find('Search_Duration').text, "%H:%M:%S.%f")
    match_ID_dict['Search_Details']['Search_Duration'] = str(timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)) + "." + str(t.microsecond)

    match_time_obj = obj.find('Match_Time_Details')
    match_ID_dict['Match_Time_Details'] = {}
    match_ID_dict['Match_Time_Details']['Match_Start_Time'] = datetime.strptime(match_time_obj.find('Match_Start_Time').text, "%Y-%m-%d %H:%M:%S.%f")
    match_ID_dict['Match_Time_Details']['Match_End_Time'] = datetime.strptime(match_time_obj.find('Match_End_Time').text, "%Y-%m-%d %H:%M:%S.%f")
    t = datetime.strptime(match_time_obj.find('Match_Duration').text, "%H:%M:%S.%f")
    match_ID_dict['Match_Time_Details']['Match_Duration'] = str(timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)) + "." + str(t.microsecond)


    return match_ID_dict


















