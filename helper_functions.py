from PIL import ImageGrab, Image
import math
import os, pickle
from datetime import datetime, timedelta
import secrets
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import time
import numpy as np
from project_path import steam_path

from loading_functions import load_usernames, get_account_info_xml_objects
from saving_functions import save_account_info_xml_objects

# Clean Network DNS and other data. | Called in driver_code.py
def clean_network_dns_data():
    os.system("ipconfig /release")
    time.sleep(0.1)
    os.system("ipconfig /flushdns")
    time.sleep(0.1)
    os.system("ipconfig /renew")
    time.sleep(0.1)

#%% Check whether unranked batches can be created at the given threshold.
def unranked_mm_batches_available(account_data, threshold = 10):
    l = []
    for username in account_data.keys(): #username = list(account_data.keys())[0]
        if account_data[username]['MM_Rank'] == 'unranked' or 'unknown' in account_data[username]['MM_Rank']:
            l.append(username)
    return True if len(l) >= threshold else False

#%% Check whether ranked batches can be created at the given threshold.
def ranked_mm_batches_available(account_data, threshold = 150):
    l = []
    for username in account_data.keys(): #username = list(account_data.keys())[0]
        if account_data[username]['MM_Rank'] != 'unranked' and 'unknown' not in account_data[username]['MM_Rank']:
            l.append(username)
    return True if len(l) >= threshold else False

#%% Weekly datestamps
def get_new_week_datestamps():
    d = {"%d"%(i+1):None for i in range(40)}
    base_datestamp = datetime(year = 2021, month = 1, day = 6, hour = 2, minute = 44, second = 5)
    for i in range(40):
        d[str(i+1)] = base_datestamp + timedelta(days = 7 * i)
    return d

def save_new_week_datestamps(weekly_datestamps, path = os.path.join('dynamic', 'weekly_datestamps.pkl')):
    try:
        with open(path, 'wb') as file:
            pickle.dump(weekly_datestamps, file)
        return True
    except:
        return False

def load_new_week_datestamps(path = os.path.join('dynamic', 'weekly_datestamps.pkl')):
    try:
        with open(path, 'rb') as file:
            weekly_datestamps = pickle.load(file)
        return weekly_datestamps
    except:
        return False


def get_current_week_details(weekly_datestamps = None, include_datetime_obj = True):
    if weekly_datestamps == None:
        weekly_datestamps = load_new_week_datestamps()
    current_datestamp = datetime.now()
    for week_index in list(weekly_datestamps.keys()): #week_index = list(weekly_datestamps.keys())[0]
        if (current_datestamp - weekly_datestamps[week_index]).days in range(0, 7):
            if include_datetime_obj:
                return week_index, weekly_datestamps[week_index]
            else:
                return week_index
    return False


def generate_unique_matchID(include_prefix = True):
    matchID = str(secrets.token_hex(16))
    if include_prefix:
        matchID = "match_" + matchID
    return matchID
def generate_unique_mismatchID(include_prefix = True):
    mismatchID = str(secrets.token_hex(8))
    if include_prefix: 
        mismatchID = "mismatch_" + mismatchID
    return mismatchID

#%% Prettifies the XML Object.
def prettify(elem):
    """
    Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

#%% XP_Calculator. # remove "current_xp +"
def calculate_xp_gained(current_xp = 0, rounds_won = 16):
    current_xp = float(current_xp)
    if current_xp == 0:
        return str(current_xp + rounds_won * 30 + (rounds_won * 30) * 3)
    if current_xp > 0 and current_xp < 4500:
        base_xp_won = rounds_won * 30
        if current_xp + base_xp_won + base_xp_won * 3 <= 4500:
            return str(current_xp + base_xp_won + base_xp_won * 3)
        else:
            boost_xp_winnable = 4500 - current_xp
            rounds_for_3x = math.floor((boost_xp_winnable / (base_xp_won * 3)) * rounds_won)
#            rounds_for_3x = round((boost_xp_winnable / (base_xp_won * 3)) * rounds_won)
            rounds_for_1x = rounds_won - rounds_for_3x
            return str(current_xp + base_xp_won + (30 * rounds_for_3x * 3) + (30 * rounds_for_1x * 1)) ##### TODO if current_xp + new boost is greater than 4500.
    elif current_xp >= 4500 and current_xp < 7500:
        base_xp_won = rounds_won * 30
        if current_xp + base_xp_won + base_xp_won * 1 <= 7500:
            return str(current_xp + base_xp_won + base_xp_won * 1)
        else:
            boost_xp_winnable = 7500 - current_xp
            rounds_for_1x = math.floor((boost_xp_winnable / (base_xp_won * 1)) * rounds_won)
            rounds_for_0x = rounds_won - rounds_for_1x
            return str(current_xp + base_xp_won + (30 * rounds_for_1x * 1) + (30 * rounds_for_0x * 0)) ##### TODO if current_xp + new boost is greater than 7500
    elif current_xp >= 7500 and current_xp < 11167:
        base_xp_won = rounds_won * 30
        if current_xp + base_xp_won + base_xp_won * 0 <= 11167:
            return str(current_xp + base_xp_won + base_xp_won * 0)
        else:
            xp_winnable_normal = 11167 - current_xp
            rounds_for_0x = math.floor((xp_winnable_normal / (base_xp_won * 1)) * rounds_won) 
            return str(current_xp + 30 * rounds_for_0x + 30 * (rounds_won - rounds_for_0x) * 0.175)  ##### TODO if current_xp + new boost is greater than 11167
    elif current_xp >= 11167:
        return str(current_xp + rounds_won * 30 * 0.175)


def calculate_matches_to_play(current_xp = 0, match_sequence = [16, 0], target_xp = 5000):
    count = 0
    index = 0
    while float(current_xp) <= float(target_xp) or index:
        count += 1
        current_xp = calculate_xp_gained(current_xp = current_xp, rounds_won = match_sequence[index])
        #print(current_xp)
        index = int(not index)
    return count        

def get_number_of_matches_to_play(usernames, account_data, return_type = 'dict', sub_categories_mm_ranks = True, match_sequence = [16, 0]):
    if type(usernames) == str:
        usernames = [usernames]
    if return_type == 'dict':
        match_count_oriented_usernames_dict = {}
        if sub_categories_mm_ranks:
            mm_rank_names = ['s1', 's2', 's3', 's4', 'se', 'sem', 'gn1', 'gn2', 'gn3', 'gnm', 'mg1', 'mg2', 'mge', 'dmg', 'le', 'lem', 'smfc', 'ge', 'expired', 'unranked']
            #mm_rank_names = ['s1', 's2', 's3', 's4', 'se', 'sem', 'gn1', 'gn2', 'gn3', 'gnm', 'mg1', 'mg2', 'mge', 'dmg', 'le', 'lem', 'smfc', 'ge']
            for username in usernames:
                # match_count = calculate_matches_to_play(account_data[username]['XP_Gained_For_Next_Rank'], match_sequence = match_sequence)
                match_count = 6
                if match_count not in match_count_oriented_usernames_dict.keys():
                    match_count_oriented_usernames_dict[match_count] = {rank:[] for rank in mm_rank_names}
                account_rank = account_data[username]['MM_Rank']
                if 'unknown' in account_rank: 
                    account_rank = 'unknown'
                if account_rank not in match_count_oriented_usernames_dict[match_count].keys():
                    match_count_oriented_usernames_dict[match_count][account_rank] = []
                match_count_oriented_usernames_dict[match_count][account_rank].append(username)
            return match_count_oriented_usernames_dict


def new_week_check():
    try:
        with open(os.path.join('dynamic', 'current_week.pkl'), 'rb') as file:
            current_week = pickle.load(file)
        check_new_week = get_current_week_details(include_datetime_obj = False)
        current_week = int(current_week)
        check_new_week = int(check_new_week)
        if current_week == check_new_week:
            return False
        else:
            with open(os.path.join('dynamic', 'week_check_trigger.pkl'), 'wb') as file:
                pickle.dump(True, file)
            return True
    except:
        print("Week Check Failed.")
        return True

def update_new_week_triggers():
    try:
        with open(os.path.join('dynamic', 'current_week.pkl'), 'wb') as file:
            pickle.dump(get_current_week_details(include_datetime_obj = False), file)
        print("Week index updated.")
        
        with open(os.path.join('dynamic', 'week_check_trigger.pkl'), 'wb') as file:
            pickle.dump(False, file)
    except:
        return False

def check_week_trigger():
    try:
        with open(os.path.join('dynamic', 'week_check_trigger.pkl'), 'rb') as file:
            trigger = pickle.load(file)
        return trigger
    except:
        return False



def update_account_stats_after_week_change():
    usernames = load_usernames()
    for username in usernames: #username = 'aggressive58dispensable18'
        file_io = get_account_info_xml_objects(username, file_order = ['weekly_info'])[0]
        current_week_number = file_io.find('Current_Week_Number').text
        file_io.find('Current_Week_Number').text = str(get_current_week_details(include_datetime_obj = False))
        current_week_number_match_count = file_io.find('Current_Week_Number_Match_Count').text
        file_io.find('Current_Week_Number_Match_Count').text = str(0)
        file_io.find(".Detailed_Info/Week[@Index='%s']"%(str(current_week_number))).find('Week_Match_Count').text = str(current_week_number_match_count)
        save_account_info_xml_objects(username, [file_io])
    
    print("WEEK DATA UPDATED")
    return True
    
    


def copy_error_image(image, name, path = os.path.join('rough_data', 'failed_images')):
    try:
        final_saving_path = os.path.join(path, name)
        if not os.path.isdir(final_saving_path):
            os.mkdir(final_saving_path)
        count = len(os.listdir(final_saving_path)) + 1
        np.save(os.path.join(final_saving_path, name + "_" + str(count) + '.npy'), np.array(image)[:, :, :3])
    except:
        print("Error in copy_error_function", name)






#%% Steam URL Converter
class Convert(object): #TO transfer
    """
    Class for converting SteamID between different versions of it
    """
    def __init__(self, steamid):
        """Init"""
        self.sid = steamid
        self.change_val = 76561197960265728
        self.alert()

    def set_steam_id(self, steamid):
        """Sets new steam ID"""
        self.sid = steamid
        self.recognize_sid()
        self.alert()

    def get_steam_id(self):
        """
        Returns given Steam ID
        """
        return self.sid

    def recognize_sid(self, choice=0):
        """
        Recognized inputted steamID
        SteamID code = 1
        SteamID3 code = 2
        SteamID32 code = 3
        SteamID64 code = 4
        Not found = 0
        Choice int 1 or 0
        1- prints recognized steam ID and returns code
        0- Returns only code
        """
        if choice not in [0, 1]:
            print('Assuming choice is 1')
            choice = 1
        if self.sid[0] == 'S':  # SteamID
            if choice == 1:
                print('Recognized ', self.sid, ' as SteamID')
            return 1
        elif self.sid[0] in ['U', 'I', 'M', 'G', 'A', 'P', 'C', 'g', 'T', 'L', 'C', 'a']:  # SteamID3
            if choice == 1:
                print('Recognized ', self.sid, ' as SteamID3')
            return 2
        elif self.sid[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] and len(self.sid) < 17:  # SteamID32
            if choice == 1:
                print('Recognized ', self.sid, ' as SteamID32')
            return 3
        elif self.sid[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] and len(self.sid) == 17:  # SteamID64
            if choice == 1:
                print('Recognized ', self.sid, ' as SteamID64')
            return 4
        else:
            if choice == 1:
                print(self.sid, 'is not recognized as any SteamID')
            return 0

    def alert(self):
        """
        Prints alert when user tries to convert one of special accounts
        """
        recognized = self.recognize_sid(0)
        if recognized == 1:
            if self.sid[6] != '0':
                print('Result of converting:', self.sid, 'steam ID may not be correct')
        elif recognized == 2:
            if self.sid[0] != 'U':
                print('Result of converting:', self.sid, 'steam ID may not be correct')

    def steam_id_converter(self):
        """
        Converts other SteamID versions to steamID
        """
        recognized = self.recognize_sid(0)
        if recognized == 1:  # Returns steamID
            return self.sid
        elif recognized == 2:  # Converts SteamID3 to SteamID
            steam3 = int(self.sid[4:])
            return 'STEAM_0:' + str(self.oddity(steam3)) + ':' + str(steam3 // 2)
        elif recognized == 3:  # Converts SteamID32 to SteamID
            steam3 = int(self.sid)
            return 'STEAM_0:' + str(self.oddity(steam3)) + ':' + str(steam3 // 2)
        elif recognized == 4:  # Converts SteamID64 SteamID64
            steam3 = int(self.steam_id32_converter())
            return 'STEAM_0:' + str(self.oddity(steam3)) + ':' + str(steam3 // 2)

    @staticmethod
    def oddity(number):
        """Checks oddity of given number"""
        if number % 2 == 0:
            return 0
        else:
            return 1

    def steam_id3_converter(self):
        """Converts other SteamID versions to SteamID3"""
        recognized = self.recognize_sid(0)
        if recognized == 1:  # Converts SteamID to SteamID3
            return 'U:1:' + str(self.steam_id32_converter())
        elif recognized == 2:  # returns SteamID3
            return self.sid
        elif recognized == 3:  # Converts SteamID32 to SteamID3
            return 'U:1:' + str(self.sid)
        elif recognized == 4:  # Converts SteamID64 to SteamID3
            return 'U:1:' + str(int(self.sid) - self.change_val)

    def steam_id32_converter(self):
        """Converts other steamID versions to steamID32"""
        recognized = self.recognize_sid(0)
        if recognized == 1:  # Converts from steamID to SteamID32
            y = self.sid[8:9]  # STEAM_0:y:zzzzzz
            z = self.sid[10:]  # STEAM_0:y:zzzzzz
            return int(z) * int(2) + int(y)
        elif recognized == 2:  # Converts from steamID3 to SteamID32
            return int(self.sid[4:])
        elif recognized == 3:  # Returns steamID32
            return int(self.sid)
        elif recognized == 4:  # Converts from steamID64 to SteamID32
            return int(self.sid) - self.change_val

    def steam_id64_converter(self):
        """Converts other SteamID versions to SteamID64"""
        recognized = self.recognize_sid(0)
        if recognized == 1:  # Converts from steamID to SteamID64
            y = self.sid[8:9]  # STEAM_0:y:zzzzzz
            z = self.sid[10:]  # STEAM_0:y:zzzzzz
            return int(z) * int(2) + int(y) + self.change_val
        elif recognized == 2:  # Converts steamID3 to SteamID64
            return int(self.sid[4:]) + self.change_val
        elif recognized == 3:  # Converts steamID32 to SteamID64
            return int(self.sid) + self.change_val
        elif recognized == 4:  # Returns steamID64
            return int(self.sid)
        


