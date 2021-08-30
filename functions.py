import time
import beepy 
import shutil, os
import pyautogui as pg
import keyboard as kb
from time import sleep
import numpy as np
from PIL import Image, ImageGrab, ImageOps
import pickle, cv2
# from major_functions import *
from positions import *
from project_path import steam_path
pg.FAILSAFE = False

# with open(os.path.join('error_numpy_boxes', 'error_list_with_numpy_images.pkl'), 'rb') as file:
#     error_list = pickle.load(file)
# del file

# with open(os.path.join('error_numpy_boxes', 'error_list.pkl'), 'rb') as file:
#     error_data_list = pickle.load(file)
# del file

def click_only(pos1x, pos1y, sleep_timer = 1, clicks = 1):
    pg.click(x = pos1x, y = pos1y, clicks = clicks, interval = 0.08)
    sleep(sleep_timer)

def right_and_left_click(pos1x, pos1y, pos2x, pos2y, sleep_timer1 = 1, sleep_timer2 = 1):
    pg.click(x = pos1x, y = pos1y, button = 'right')
    sleep(sleep_timer1)
    pg.click(x = pos2x, y = pos2y)
    sleep(sleep_timer2)

def click_and_drag(pos1x, pos1y, pos2x, pos2y, sleep_timer = 1):
    pg.moveTo(x = pos1x, y = pos1y)
    sleep(0.1)
    pg.dragTo(x = pos2x, y = pos2y, duration = 0.25)
    sleep(sleep_timer)

def write_only(text = '', sleep_timer = 1, select_text = 0):
    if select_text != 0:
        click_only(None, None, 0.1, 3)
    kb.write(text)
    sleep(sleep_timer)

def write_and_execute(text = '', sleep_timer1 = 1, sleep_timer2 = 1, select_text = 0):
    write_only(text, sleep_timer1, select_text)
    kb.press_and_release('enter')
    sleep(sleep_timer2)

def hover_only(pos1x, pos1y, sleep_timer = 1, duration = 1):
    pg.moveTo(x = pos1x, y = pos1y, duration = duration)
    sleep(sleep_timer)
    
# Approved | Used in main_file
def get_accounts(file_path = 'active_accounts.txt'):
    file = open(file_path, 'r')
    data = list(map(lambda x:x.split(), file.readlines()))
    file.close()
    u_upper, p_upper, i_upper, u_lower, p_lower, i_lower = [], [], [], [], [], []
    for i in data[:5]: i_upper.append(i[0]); u_upper.append(i[1]); p_upper.append(i[2])
    for i in data[5:10]: i_lower.append(i[0]); u_lower.append(i[1]); p_lower.append(i[2])
    return u_upper, p_upper, i_upper, u_lower, p_lower, i_lower

def press_and_release(command, sleep_timer = 1, number_of_presses = 1):
    for i in range(number_of_presses):
        kb.press_and_release(hotkey = command)
        sleep(sleep_timer)


def copy_userdata(steam32id = 0, map_name = "anubis", base_path = os.path.join('userdata')):
    try:
        if os.path.isdir(os.path.join(steam_path, "userdata", steam32id)):
            shutil.rmtree(os.path.join(steam_path, "userdata", steam32id))#, ignore_errors = True)
        shutil.copytree(os.path.join(base_path, map_name), 
                        os.path.join(steam_path, "userdata", steam32id))
        return True
    except:
        return False

def cd_check(panel_top_left_x, panel_top_left_y, select_panel = False, consider_blue = True):
    yellow_cd = np.array([225, 193,  17], dtype='uint8')
    green_cd_min = np.array([131, 150, 61], dtype = 'uint8')
    green_cd_max = np.array([164, 195, 85], dtype = 'uint8')
    green_cd = np.array([145, 175, 73], dtype = 'uint8')                       #TODO
    blue_network_problem_min = np.array([50, 178, 216], 'uint8')
    blue_network_problem_max = np.array([73, 183, 217], 'uint8')

    index = CSGO_UPPER_POS_X.index(panel_top_left_x)
    if select_panel:
        click_only(panel_top_left_x + CSGO_TITLE_BAR_X[index], panel_top_left_y + CSGO_TITLE_BAR_Y[index], 0.2, 2)
    
    test_image = np.array(ImageGrab.grab([panel_top_left_x + 81, 
                                          panel_top_left_y + 34, 
                                          panel_top_left_x + 82, 
                                          panel_top_left_y + 35, 
                                          ])).squeeze()
    if consider_blue:
        if np.all(test_image >= blue_network_problem_min) and \
            np.all(test_image <= blue_network_problem_max):
                return "Blue"
    if np.all(test_image == yellow_cd) or \
        np.all(test_image[::-1] == yellow_cd):
            return "Yellow"
    elif np.all(test_image == green_cd) or \
        np.all(test_image[::-1] == green_cd) or \
            (np.all(test_image >= green_cd_min) and np.all(test_image <= green_cd_max)):
            return "Green"

    else:
        return None

def say_beep(sleep_timer = 1, repeat = 1):
    if repeat == -1: #infinite
        while True:
            beepy.beep(5)
            sleep(sleep_timer)
    else:
        for i in range(repeat):
            beepy.beep(5)
            sleep(sleep_timer)

def lost_connection_check(panel_top_left_x, panel_top_left_y):
    lost_connection_pixel = np.array([44], 'uint8')
    #time.sleep(5) 1543, 347 +3, +3
    panel_connection_status = np.unique(np.array(ImageGrab.grab([panel_top_left_x + 263, 
                                                                 panel_top_left_y + 293, 
                                                                 panel_top_left_x + 266, 
                                                                 panel_top_left_y + 296])))
    if len(panel_connection_status) == 1 and \
        np.all(panel_connection_status == lost_connection_pixel):
            print("Connection Error")
            return True
    return False


def panel_reposition(panel_upper, panel_lower = -1):
    if panel_lower == -1:
        panel_lower = panel_upper

    click_only(CSGO_UPPER_POS_X[panel_upper - 1] + CSGO_TITLE_BAR_X[panel_upper - 1], 
               CSGO_UPPER_POS_Y[panel_upper - 1] + CSGO_TITLE_BAR_Y[panel_upper - 1], 
               0.2, 2)
    
    click_only(CSGO_LOWER_POS_X[panel_lower - 1] + CSGO_TITLE_BAR_X[panel_lower - 1], 
               CSGO_LOWER_POS_Y[panel_lower - 1] + CSGO_TITLE_BAR_Y[panel_lower - 1], 
               0.2, 2)
    sleep(0.4)
    click_and_drag(CSGO_LOWER_POS_X[panel_lower - 1] + CSGO_TITLE_BAR_X[panel_upper - 1], 
                   CSGO_LOWER_POS_Y[panel_lower - 1] + CSGO_TITLE_BAR_Y[panel_upper - 1], 
                   CSGO_UPPER_POS_X[panel_upper - 1] + CSGO_TITLE_BAR_X[panel_upper - 1], 
                   CSGO_UPPER_POS_Y[panel_upper - 1] + CSGO_TITLE_BAR_Y[panel_upper - 1] + 27, 
                   1)
    sleep(0.4)
    
    click_and_drag(CSGO_UPPER_POS_X[panel_upper - 1] + CSGO_TITLE_BAR_X[panel_lower - 1], 
                   CSGO_UPPER_POS_Y[panel_upper - 1] + CSGO_TITLE_BAR_Y[panel_lower - 1], 
                   CSGO_LOWER_POS_X[panel_lower - 1] + CSGO_TITLE_BAR_X[panel_lower - 1], 
                   CSGO_LOWER_POS_Y[panel_lower - 1] + CSGO_TITLE_BAR_Y[panel_lower - 1], 
                   1)
    sleep(0.4)
    
    click_and_drag(CSGO_UPPER_POS_X[panel_upper - 1] + CSGO_TITLE_BAR_X[panel_upper - 1], 
                   CSGO_UPPER_POS_Y[panel_upper - 1] + CSGO_TITLE_BAR_Y[panel_upper - 1] + 27, 
                   CSGO_UPPER_POS_X[panel_upper - 1] + CSGO_TITLE_BAR_X[panel_upper - 1], 
                   CSGO_UPPER_POS_Y[panel_upper - 1] + CSGO_TITLE_BAR_Y[panel_upper - 1], 
                   1)
    
def accept_check(panel_top_left_x, panel_top_left_y):
    identification_box = [330, 278, 369, 314]
    threshold = 155
    green_layer = 1
    button_image = np.array(ImageGrab.grab([panel_top_left_x, 
                                       panel_top_left_y, 
                                       panel_top_left_x + 640, 
                                       panel_top_left_y + 480 + 27]).crop(identification_box))[:, :, green_layer]
    return np.sum(button_image)/np.multiply(button_image.shape[0], button_image.shape[1]) > threshold

def update_winner_batch(filename = "winner_lobby.txt"):
    file = open(filename)
    data = file.read()
    file.close()
    file = open(filename, 'w')
    if data == 'upper':
        file.write('lower')
    else:
        file.write('upper')
    file.close()

def get_winner_lobby(filename = "winner_lobby.txt"):
    file = open(filename)
    data = file.read()
    file.close()
    return data

def after_match_cleanup(sleep_timer = 10):
    sleep(sleep_timer)
    
    upper_batch = [CSGO_UPPER_POS_X, CSGO_UPPER_POS_Y]
    lower_batch = [CSGO_LOWER_POS_X, CSGO_LOWER_POS_Y]
    
    for batch in [upper_batch, lower_batch]: #batch = lower_batch.copy()
        POS_X, POS_Y = batch
        for i in range(5): #i = 0
            click_only(POS_X[i] + CSGO_TITLE_BAR_X[i], 
                       POS_Y[i] + CSGO_TITLE_BAR_Y[i], 0.1)
            press_and_release('f7', 0.2, 1)



# def identify_error(test_image, error_list):

#     test_image_array = np.array(test_image)
#     for error_name, error_image_array in error_list.items():
#         error_image_array_mask = error_image_array[:, :, 3:4]//255
#         error_image_array = error_image_array[:, :, :3]
        
#         if np.all(error_image_array == np.multiply(test_image_array, error_image_array_mask)):
#             print(error_name)
#             return error_name
#     return None

# def identify_error_wrapper(POS_X, POS_Y, error_list, error_data_list):
#     test_image = ImageGrab.grab([POS_X, POS_Y, POS_X + 640, POS_Y + 480])
#     output = identify_error(test_image, error_list)
#     if output is None:
#         return None
#     error_ok_button = error_data_list[output][2]
#     file = open('logging_error.txt', 'a')
#     file.write(str(time.time()))
#     file.write(", ")
#     file.write(output)
#     file.write("\n")
#     file.close()
#     return error_ok_button


def clear_untrusted_issue(all_panels = True, POS_X = 0, POS_Y = 54):
    if all_panels == False:
        clear_untrusted(POS_X, POS_Y)
    else:
        for i in range(5):
            clear_untrusted(CSGO_UPPER_POS_X[i], CSGO_UPPER_POS_Y[i])
            clear_untrusted(CSGO_LOWER_POS_X[i], CSGO_LOWER_POS_Y[i])

def clear_untrusted(POS_X, POS_Y):
    for j in range(1):
        index = CSGO_UPPER_POS_X.index(POS_X)
        click_only(POS_X + CSGO_TITLE_BAR_X[index], POS_Y + CSGO_TITLE_BAR_Y[index], 0.2, 1)
        click_only(POS_X + CSGO_PLAY_BUTTON_X, POS_Y + CSGO_PLAY_BUTTON_Y, 0.25, 3)
        time.sleep(0.3)
        hover_only(POS_X + CSGO_GO_SEARCH_BUTTON_X, POS_Y + CSGO_GO_SEARCH_BUTTON_Y, 0.5, 0.25)
        click_only(None, None, 0.5, 1)
        time.sleep(0.6)
        click_only(POS_X + CSGO_UNTRUSTED_CONTINUE_X, POS_Y + CSGO_UNTRUSTED_CONTINUE_Y, 0.25, 2)
        time.sleep(0.3)
        hover_only(POS_X + CSGO_PROFILE_HOVER_X, POS_Y + CSGO_PROFILE_HOVER_Y, 0.2, 0.1)
        click_only(POS_X + CSGO_LEAVE_LOBBY_X, POS_Y + CSGO_LEAVE_LOBBY_Y, 0.3, 3)
        # hover_only(POS_X[i] + CSGO_GO_SEARCH_BUTTON_X, POS_Y[i] + CSGO_GO_SEARCH_BUTTON_Y, 0.1, 0.07)
        # click_only(None, None, 0.5, 1)
        time.sleep(0.3)

def get_score_snippet(POS_X, POS_Y):
    save_path = os.path.join('score_images')
    score_1_x_1, score_1_y_1 = 307, 41
    score_1_x_2, score_1_y_2 = 321, 52
    
    score_2_x_1, score_2_y_1 = 325, 41
    score_2_x_2, score_2_y_2 = 339, 52
    
    image_1 = ImageGrab.grab([POS_X + score_1_x_1, 
                              POS_Y + score_1_y_1, 
                              POS_X + score_1_x_2, 
                              POS_Y + score_1_y_2, 
                              ])
    image_2 = ImageGrab.grab([POS_X + score_2_x_1, 
                              POS_Y + score_2_y_1, 
                              POS_X + score_2_x_2, 
                              POS_Y + score_2_y_2, 
                              ])
    item_number = len(os.listdir(save_path)) + 5000
    image_1.save(os.path.join(save_path, str(item_number) + '.png'))
    image_2.save(os.path.join(save_path, str(item_number + 1) + '.png'))

def get_gun_snippet(POS_X, POS_Y):
    save_path = os.path.join('gun_images')
    image_1 = ImageGrab.grab([POS_X, 
                              POS_Y, 
                              POS_X + 640, 
                              POS_Y + 480, 
                              ])
    item_number = len(os.listdir(save_path))
    image_1.save(os.path.join(save_path, str(item_number) + '.png'))

class Convert(object):
    """Class for converting SteamID between different versions of it"""

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
        """Returns given Steam ID"""
        return self.sid

    def recognize_sid(self, choice=0):
        """Recognized inputted steamID
        SteamID code = 1
        SteamID3 code = 2
        SteamID32 code = 3
        SteamID64 code = 4
        Not found = 0
        Choice int 1 or 0
        1- prints recognized steam ID and returns code
        0- Returns only code"""
        if choice is not 0 and choice is not 1:
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
        """Prints alert when user tries to convert one of special accounts"""
        recognized = self.recognize_sid(0)
        if recognized == 1:
            if self.sid[6] != '0':
                print('Result of converting:', self.sid, 'steam ID may not be correct')
        elif recognized == 2:
            if self.sid[0] != 'U':
                print('Result of converting:', self.sid, 'steam ID may not be correct')

    def steam_id_converter(self):
        """Converts other SteamID versions to steamID"""
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












