#from functions import *
from tqdm import tqdm
from datetime import datetime, timedelta
import pandas as pd
import os
import numpy as np
import xml.dom as minidom
import xml.etree.ElementTree as ET

### #TODO CHECK ALL FUNCTIONS imports.
from driver_functions import *
from get_details_from_xml import *
from xml_functions import *
from helper_functions import *

database_path = os.path.join('database')
assert os.path.isdir(database_path)
open_database_path = os.path.join('database', 'open_database')
assert os.path.isdir(open_database_path)

raw_data_sheet = pd.read_excel(os.path.join(database_path, 'batch_2.xlsx'))

steam_profile_link = raw_data_sheet['community link'].to_list()
username = raw_data_sheet['Username'].to_list()
password = raw_data_sheet['Password'].to_list()
email_address = raw_data_sheet['Email Address'].to_list()
email_password = raw_data_sheet['Email Password'].to_list()

mm_rank = ['unranked'] * len(raw_data_sheet)
mm_wins = [0] * len(raw_data_sheet)
pr_rank = [2.0] * len(raw_data_sheet)

weekly_datestamps = load_new_week_datestamps()

# follow_path = [""] * len(raw_data_sheet)

for i in tqdm(range(len(raw_data_sheet))): #i=0
    account_name = username[i]
    account_folder = os.path.join(open_database_path, account_name)
    if not os.path.isdir(account_folder): os.mkdir(account_folder)
    if os.path.isfile(os.path.join(account_folder, 'info.xml')):
        pass
    else:
        #%% <username>/info.xml
        account_root = ET.Element('Acccount_Details')        
        
        datetime_now_object = datetime.now()

        account_steam_id = ET.SubElement(account_root, 'SteamID')
        account_steam_id.text = str(Convert(str(steam_profile_link[i][steam_profile_link[i].find('les/')+4:steam_profile_link[i].find('les/')+4 + 17])).steam_id32_converter())
        account_username = ET.SubElement(account_root, 'Username')
        account_username.text = str(account_name)
        account_password = ET.SubElement(account_root, 'Password')
        account_password.text = str(password[i])
        account_email_address = ET.SubElement(account_root, 'Email_Address')
        account_email_address.text = str(email_address[i])
        account_email_password = ET.SubElement(account_root, 'Email_Password')
        account_email_password.text = str(email_password[i])
        account_mm_rank = ET.SubElement(account_root, 'MM_Rank')
        account_mm_rank.text = str(mm_rank[i])
        account_mm_wins = ET.SubElement(account_root, 'MM_Wins')
        account_mm_wins.text = str(mm_wins[i])
        account_pr_rank = ET.SubElement(account_root, 'PR_Rank')
        account_pr_rank.text = str(pr_rank[i])
        
        account_target_pr_rank = ET.SubElement(account_root, 'Target_PR_Rank')
        account_target_pr_rank.text = str(21)
        
        account_friend_code = ET.SubElement(account_root, 'Friend_Code')
        account_friend_code.text = "No Info"
        # account_earned_xp = ET.SubElement(account_root, 'Earned_XP')
        # account_earned_xp.text = '0'

        account_steam_profile_link = ET.SubElement(account_root, 'Steam_Profile_Link')
        account_steam_profile_link.text = str(steam_profile_link[i])
        # account_steam_trade_url = ET.SubElement(account_root, 'Steam_Trade_Url')
        # account_steam_trade_url.text = ""

        account_last_mm_rank_updated_time = ET.SubElement(account_root, 'Last_MM_Rank_Updated_Time')
        account_last_mm_rank_updated_time.text = str(datetime_now_object)
        
        account_last_cooldown_type = ET.SubElement(account_root, 'Last_Cooldown_Type')
        account_last_cooldown_type.text = "No Info"
        
        account_last_cooldown_time = ET.SubElement(account_root, 'Last_Cooldown_Time')
        account_last_cooldown_time.text = str(datetime.now() - timedelta(days = 1)) #"No Info"
        
        account_total_inventory_count = ET.SubElement(account_root, 'Total_Inventory_Count')
        account_total_inventory_count.text = "0"

        with open(os.path.join(account_folder, 'info.xml'), 'w') as file:
            file.write(prettify(account_root))
        
        #%% <username>/trade_info.xml
        account_trade_root = ET.Element('Account_Trade_Details')
        
        account_trade_url = ET.SubElement(account_trade_root, 'Trade_Url')
        account_trade_url.text = "No Info"
        
        account_trade_total_inventory_count = ET.SubElement(account_trade_root, 'Total_Inventory_Count')
        account_trade_total_inventory_count.text = "0"
        
        account_trade_inventory_items = ET.SubElement(account_trade_root, 'Inventory_Items')
        
        account_trade_last_trade_date = ET.SubElement(account_trade_root, 'Last_Trade_Date')
        account_trade_last_trade_date.text = "No Info"
        
        account_trade_last_trade_item_count = ET.SubElement(account_trade_root, 'Last_Trade_Item_Count')
        account_trade_last_trade_item_count.text = "No Info"
        
        account_trade_last_trade_tradeofferid = ET.SubElement(account_trade_root, 'Last_Trade_TradeOfferID')
        account_trade_last_trade_tradeofferid.text = 'No Info'
        
        account_trade_trade_date_history = ET.SubElement(account_trade_root, 'Trade_Date_History')
        
        account_trade_trade_items_history = ET.SubElement(account_trade_root, 'Trade_Items_History')
        
        account_trade_trade_tradeofferids = ET.SubElement(account_trade_root, 'Trade_TradeOfferIDs')
        
        with open(os.path.join(account_folder, 'trade_info.xml'), 'w') as file:
            file.write(prettify(account_trade_root))
        
        #%% <username>/mm_rank_info.xml
        account_mm_rank_root = ET.Element('Account_MM_Rank_Details')
        
        account_mm_rank_mm_wins = ET.SubElement(account_mm_rank_root, 'MM_Wins')
        account_mm_rank_mm_wins.text = str(mm_wins[i])
        account_mm_rank_mm_rank = ET.SubElement(account_mm_rank_root, 'MM_Rank')
        account_mm_rank_mm_rank.text = str(mm_rank[i])
        
        account_mm_rank_last_mm_rank_updated_time = ET.SubElement(account_mm_rank_root, 'Last_MM_Rank_Updated_Time')
        account_mm_rank_last_mm_rank_updated_time.text = "No Info"
        
        account_mm_rank_last_mm_rank_update_matchID = ET.SubElement(account_mm_rank_root, 'Last_MM_Rank_Update_MatchID')
        account_mm_rank_last_mm_rank_update_matchID.text = 'No Info'
        
        account_mm_rank_rank_opened = ET.SubElement(account_mm_rank_root, 'Rank_Opened')
        account_mm_rank_rank_opened.text = 'No Info'

        account_mm_rank_rank_opened_date = ET.SubElement(account_mm_rank_root, 'Rank_Opened_Date')
        account_mm_rank_rank_opened_date.text = 'No Info'

        account_mm_rank_rank_opened_matchID = ET.SubElement(account_mm_rank_root, 'Rank_Opened_MatchID')
        account_mm_rank_rank_opened_matchID.text = 'No Info'

        account_mm_rank_mm_rank_history = ET.SubElement(account_mm_rank_root, 'MM_Rank_History')
        temp_account_mm_rank = ET.Element('Rank', attrib = {"Index":"1"})
        temp_account_mm_rank.text = str(mm_rank[i])
        account_mm_rank_mm_rank_history.extend([temp_account_mm_rank])

        account_mm_rank_mm_rank_time_history = ET.SubElement(account_mm_rank_root, 'MM_Rank_Time_History')
        temp_account_mm_rank_history = ET.Element('Time', attrib = {"Index":"1"})
        temp_account_mm_rank_history.text = str(datetime_now_object)
        account_mm_rank_mm_rank_time_history.extend([temp_account_mm_rank_history])
        
        with open(os.path.join(account_folder, 'mm_rank_info.xml'), 'w') as file:
            file.write(prettify(account_mm_rank_root))

        #%% <username>/pr_rank_info.xml
        account_pr_rank_root = ET.Element('Account_PR_Rank_Details')
        
        account_pr_rank_pr_rank = ET.SubElement(account_pr_rank_root, 'PR_Rank')
        account_pr_rank_pr_rank.text = str(pr_rank[i])
        
        account_pr_rank_xp_gained_for_next_rank = ET.SubElement(account_pr_rank_root, 'XP_Gained_For_Next_Rank')
        account_pr_rank_xp_gained_for_next_rank.text = "0"
        
        account_pr_rank_current_week_number = ET.SubElement(account_pr_rank_root, 'Current_Week_Number')
        account_pr_rank_current_week_number.text = "1"
        
        account_pr_rank_current_week_match_count = ET.SubElement(account_pr_rank_root, 'Current_Week_Number_Match_Count')
        account_pr_rank_current_week_match_count.text = '0'
        
        # account_pr_rank_weekly_match_ids = ET.SubElement(account_pr_rank_root, 'Weekly_Match_IDs')
        account_pr_rank_pr_rank_history = ET.SubElement(account_pr_rank_root, 'PR_Rank_History')
        pr_rank_pr_rank_history_list = []
        for index in list(weekly_datestamps.keys()): #index = '1'
            week_index = ET.Element('Week', attrib = {"Index": index})
            week_start_datestamp = ET.SubElement(week_index, 'Week_Start_Datestamp')
            week_start_datestamp.text = str(weekly_datestamps[index])
            week_xp_gained = ET.SubElement(week_index, 'Weekly_XP_Gained')
            week_xp_gained.text = str(0)
            pr_rank_pr_rank_history_list.append(week_index)
        account_pr_rank_pr_rank_history.extend(pr_rank_pr_rank_history_list)

        with open(os.path.join(account_folder, 'pr_rank_info.xml'), 'w') as file:
            file.write(prettify(account_pr_rank_root))
        
        # #%% <username>/follow_path.xml
        # account_follow_path_root = ET.Element('Account_Follow_Path_Details')
        # account_follow_path_follow_path_list = get_follow_path_xml_object(path = follow_path[i], delimiter = "")
        # account_follow_path_root.extend(account_follow_path_follow_path_list)
        
        # with open(os.path.join(account_folder, 'follow_path.xml'), 'w') as file:
        #     file.write(prettify(account_follow_path_root))
        
        #%% <username>/match_history.xml
        account_match_history_root = ET.Element('Account_Match_History_Details')
        
        account_match_history_match_count = ET.SubElement(account_match_history_root, 'Match_Count')
        account_match_history_match_count.text = "0"
        
        account_match_history_matchIDs = ET.SubElement(account_match_history_root, 'MatchIDs')
        
        with open(os.path.join(account_folder, 'match_history.xml'), 'w') as file:
            file.write(prettify(account_match_history_root))
        
        #%% <username>/cooldown_info.xml
        account_cooldown_root = ET.Element('Account_Cooldown_Details')
        
        account_cooldown_last_cooldown_type = ET.SubElement(account_cooldown_root, 'Last_Cooldown_Type')
        account_cooldown_last_cooldown_type.text = "No Info"
        
        account_cooldown_last_cooldown_time = ET.SubElement(account_cooldown_root, 'Last_Cooldown_Time')
        account_cooldown_last_cooldown_time.text = str(datetime.now() - timedelta(days = 1)) #"No Info"
        
        account_cooldown_cooldown_type_history = ET.SubElement(account_cooldown_root, 'Cooldown_Type_History')
        
        account_cooldown_cooldown_time_history = ET.SubElement(account_cooldown_root, 'Cooldown_Time_History')
        
        account_cooldown_cooldown_matchID_history = ET.SubElement(account_cooldown_root, 'Cooldown_MatchID_History')
        
        with open(os.path.join(account_folder, 'cooldown_info.xml'), 'w') as file:
            file.write(prettify(account_cooldown_root))


        #%% <username>/weekly_info.xml
        account_weekly_root = ET.Element('Account_Weekly_Details')
        
        account_weekly_current_week_number = ET.SubElement(account_weekly_root, "Current_Week_Number")
        account_weekly_current_week_number.text = "1"# "No Info"
        account_weekly_current_week_number_match_count = ET.SubElement(account_weekly_root, "Current_Week_Number_Match_Count")
        account_weekly_current_week_number_match_count.text = "0"
        
        account_weekly_detailed_info = ET.SubElement(account_weekly_root, "Detailed_Info")
        weekly_weekly_history_list = []
        for index in list(weekly_datestamps.keys()): #index = '1'
            week_index = ET.Element('Week', attrib = {"Index": index})
            week_match_count_ = ET.SubElement(week_index, 'Week_Match_Count')
            week_match_count_.text = str(0)
            week_IDs_ = ET.SubElement(week_index, 'IDs')
            weekly_weekly_history_list.append(week_index)
        account_weekly_detailed_info.extend(weekly_weekly_history_list)
        
        with open(os.path.join(account_folder, 'weekly_info.xml'), 'w') as file:
            file.write(prettify(account_weekly_root))
        
        #%% <username>/error_info.xml
        account_error_root = ET.Element('Account_Error_Details')
        
        account_error_error_count = ET.SubElement(account_error_root, 'Error_Count')
        account_error_error_count.text = str(0)
        account_error_last_error_name = ET.SubElement(account_error_root, 'Last_Error_Name')
        account_error_last_error_name.text = 'No Info'
        account_error_last_error_timestamp = ET.SubElement(account_error_root, 'Last_Error_Timestamp')
        account_error_last_error_timestamp.text = 'No Info'
        account_error_error_name_history = ET.SubElement(account_error_root, 'Error_Name_History')
        account_error_error_timestamp_history = ET.SubElement(account_error_root, 'Error_Timestamp_History')
        
        with open(os.path.join(account_folder, 'error_info.xml'), 'w') as file:
            file.write(prettify(account_error_root))
        
        #%% <username>/mismatch_info.xml
        account_mismatch_root = ET.Element('Account_Mismatch_Details')
        
        account_error_mm_mismatch_count = ET.SubElement(account_mismatch_root, 'MM_Mismatch_Count')
        account_error_mm_mismatch_count.text = str(0)
        account_error_last_mm_mismatch_id = ET.SubElement(account_mismatch_root, 'Last_MM_Mismatch_ID')
        account_error_last_mm_mismatch_id.text = 'No Info'
        account_error_last_mm_mismatch_timestamp = ET.SubElement(account_mismatch_root, 'Last_MM_Mismatch_Timestamp')
        account_error_last_mm_mismatch_timestamp.text = 'No Info'
        
        account_error_mm_mismatch_history = ET.SubElement(account_mismatch_root, 'MM_Mismatch_History')
        
        with open(os.path.join(account_folder, 'mismatch_info.xml'), 'w') as file:
            file.write(prettify(account_mismatch_root))
        








