#from functions import *
from tqdm import tqdm
from datetime import datetime
import pandas as pd
import os
import numpy as np
import xml.dom as minidom
import xml.etree.ElementTree as ET
from driver_functions import *

database_path = os.path.join('database')
open_database_path = os.path.join('database', 'open_database')
raw_data_sheet = pd.read_excel(os.path.join(database_path, 'batch_2_main_sheet.xlsx'))

steam_profile_link = raw_data_sheet['community link'].to_list()
username = raw_data_sheet['Username'].to_list()
password = raw_data_sheet['Password'].to_list()
email_address = raw_data_sheet['Email Address'].to_list()
email_password = raw_data_sheet['Email Password'].to_list()

mm_rank = ['unranked'] * len(raw_data_sheet)
mm_wins = [0] * len(raw_data_sheet)
pr_rank = [2.0] * len(raw_data_sheet)


follow_path = [""] * len(raw_data_sheet)
history = [""] * len(raw_data_sheet)
earned_xp = [0] * len(raw_data_sheet)

mm_rank_history = [""] * len(raw_data_sheet)
mm_rank_history_time = [""]  * len(raw_data_sheet)

mm_rank_last_updated_on = [""] * len(raw_data_sheet)

last_cooldown_time = [""] * len(raw_data_sheet)
last_cooldown_type = [""] * len(raw_data_sheet)
cooldown_type_history = [""] * len(raw_data_sheet)
cooldown_time_history = [""] * len(raw_data_sheet)

steam_trade_url = [""] * len(raw_data_sheet)

for i in tqdm(range(len(username))): #i=1
    account = username[i]
    account_folder = os.path.join(open_database_path, account)
    if not os.path.isdir(account_folder): os.mkdir(account_folder)
    # if os.path.isfile(os.path.join(account_folder, 'info.xml')): pass
    # else:
    if True:
        account_root = ET.Element('Details')
        
        account_steam_profile_link = ET.SubElement(account_root, 'Steam_Profile_Link')
        account_steam_profile_link.text = str(steam_profile_link[i])
        account_steam_id = ET.SubElement(account_root, 'SteamID')
        account_steam_id.text = str(Convert(str(steam_profile_link[i][steam_profile_link[i].find('les/')+4:steam_profile_link[i].find('les/')+4 + 17])).steam_id32_converter())
        account_username = ET.SubElement(account_root, 'Username')
        account_username.text = str(account)
        account_password = ET.SubElement(account_root, 'Password')
        account_password.text = str(password[i])
        account_email_address = ET.SubElement(account_root, 'Email_Address')
        account_email_address.text = str(email_address[i])
        account_email_password = ET.SubElement(account_root, 'Email_Password')
        account_email_password.text = str(email_password[i])
        account_steam_trade_url = ET.SubElement(account_root, 'Steam_Trade_Url')
        account_mm_rank = ET.SubElement(account_root, 'MM_Rank')
        account_mm_rank.text = str(mm_rank[i])
        account_mm_wins = ET.SubElement(account_root, 'MM_Wins')
        account_mm_wins.text = str(mm_wins[i])
        account_pr_rank = ET.SubElement(account_root, 'PR_Rank')
        account_pr_rank.text = str(pr_rank[i])
        
        # account_follow_path = ET.SubElement(account_root, "Follow_Path")
        # account_follow_path_children = []
        # for j in range(10):
        #     account_follow_path_node = ET.Element('Match_%d'%(j+1), num = str(j))
        #     account_follow_path_node.text = 'w'
        #     account_follow_path_children.append(account_follow_path_node)
        # account_follow_path.extend(account_follow_path_children)
        
        #account_history = ET.SubElement(account_root, 'History')
        
        account_earned_xp = ET.SubElement(account_root, 'Earned_XP')
        account_earned_xp.text = '0'
        
        # account_mm_rank_history = ET.SubElement(account_root, 'MM_Rank_History')
        # account_mm_rank_history_last_rank = ET.Element('Rank_1', num = '0'); account_mm_rank_history_last_rank.text = str(mm_rank[i])
        # account_mm_rank_history.extend([account_mm_rank_history_last_rank])

        account_mm_rank_latest_timestamp_dt = datetime.now()
        account_mm_rank_latest_timestamp = get_timestamp_xml_object(index = 0, now = account_mm_rank_latest_timestamp_dt)
        # account_mm_rank_history_time = ET.SubElement(account_root, 'MM_Rank_History_Time')
        # account_mm_rank_history_time.extend([account_mm_rank_latest_timestamp])
        
        account_mm_rank_last_update = ET.SubElement(account_root, 'MM_Rank_Last_Updated_On')
        account_mm_rank_last_update.text = str(account_mm_rank_latest_timestamp_dt)
        
        account_last_cooldown_type = ET.SubElement(account_root, 'Last_Cooldown_Type')
        
        account_last_cooldown_time = ET.SubElement(account_root, 'Last_Cooldown_Time')
        
        # account_cooldown_type_history = ET.SubElement(account_root, 'Cooldown_Type_History')
        
        # account_cooldown_time_history = ET.SubElement(account_root, 'Cooldown_Time_History')
        
        # account_steam_trade_time_history = ET.SubElement(account_root, 'Steam_Trade_Time_History')
        
        account_inventory_count= ET.SubElement(account_root, 'Inventory_Count')

        # account_inventory_history = ET.SubElement(account_root, 'Steam_Trade_Inventory_History')
        
        with open(os.path.join(account_folder, 'info.xml'), 'w') as file:
            file.write(prettify(account_root))















