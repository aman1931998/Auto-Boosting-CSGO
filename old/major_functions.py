import sys
import subprocess
import pickle
import shutil
import pyautogui as pg
import keyboard as kb
import time
import os
from functions import *
from positions import *
import psutil
import pyperclip as pc


CSGO_CANCEL_FRIEND_INVITE_X, CSGO_CANCEL_FRIEND_INVITE_Y = 629, 132

CSGO_LEADER_LEAVE_LOBBY_X, CSGO_LEADER_LEAVE_LOBBY_Y = 621, 43
CSGO_LEAVE_LOBBY_X, CSGO_LEAVE_LOBBY_Y = 621, 68   #update hoga yeh pixel

USERNAME_UPPER, PASSWORD_UPPER, STEAM_ID_UPPER, USERNAME_LOWER, PASSWORD_LOWER, STEAM_ID_LOWER = get_accounts()

with open(os.path.join('error_numpy_boxes', 'error_coordinates' + '.pkl'), 'rb') as file:
    error_coordinates = pickle.load(file)
with open(os.path.join('error_numpy_boxes', 'error_ok_button' + '.pkl'), 'rb') as file:
    error_ok_button = pickle.load(file)
with open(os.path.join('error_numpy_boxes', 'error_with_numpy_images' + '.pkl'), 'rb') as file:
    error_with_numpy_images = pickle.load(file)

with open(os.path.join('error_numpy_boxes', 'start_up', 'start_up_error_coordinates' + '.pkl'), 'rb') as file:
    start_up_error_coordinates = pickle.load(file)
with open(os.path.join('error_numpy_boxes', 'start_up', 'start_up_error_ok_button' + '.pkl'), 'rb') as file:
    start_up_error_ok_button = pickle.load(file)
with open(os.path.join('error_numpy_boxes', 'start_up', 'start_up_error_with_numpy_images' + '.pkl'), 'rb') as file:
    start_up_error_with_numpy_images = pickle.load(file)
del file



avast_popup_checker_image = np.load(os.path.join("warning_snippets", "avast_popup.npy"))

def play_next_match():
    with open('number_of_matches_to_play.txt', 'r') as file:
        number_of_matches_to_play = int(file.read())
    with open("number_of_matches_played.txt", 'r') as file:
        number_of_matches_played = int(file.read())
    if number_of_matches_played <= number_of_matches_to_play:
        return True
    else:
        return False
    
def update_next_match_play():
    with open("number_of_matches_played.txt", 'r') as file:
        number_of_matches_played = int(file.read())
    number_of_matches_played+=1
    with open("number_of_matches_played.txt", 'w') as file:
        file.write(str(number_of_matches_played))

def cleaner(PIDs = None): #TODO
    '''
    Cleans all instances of steam, steamwebhelper and csgo.
    '''
    if PIDs is None:
        os.system('taskkill /f /t /im csgo.exe /im steam.exe /im steamwebhelper.exe /im steamerrorreporter.exe')
        os.system('taskkill /f /t /im cmd.exe')
    else:
        for panel in PIDs.keys():
            subproc = PIDs[panel]
            subproc.terminate()
            PIDs[panel] = ""
    
    while True:
        try:
            userdata_list = os.listdir(os.path.join("C:\\", "Program Files (x86)", "Steam", "userdata"))
            for userdata in userdata_list:
                shutil.rmtree(os.path.join("C:\\", "Program Files (x86)", "Steam", "userdata", userdata))
            break
        except:
            pass

def clean_PIDs(PIDs):
    for panel in PIDs.keys():
        subproc = PIDs[panel]
        subproc.terminate()
        PIDs[panel] = ""
    cleaner()
    return PIDs


#%%
def get_panel_location(panel_location = 'u1'):
    '''
    Returns the panel location.
    '''
    batch = panel_location[0]
    place = int(panel_location[1]) - 1
    if batch == 'u':
        return CSGO_UPPER_POS_X[place], CSGO_UPPER_POS_Y[place]
    elif batch == 'l':
        return CSGO_LOWER_POS_X[place], CSGO_LOWER_POS_Y[place]

def launch_panel(username, password, steamid, panel_location, map_name = "anubis", trusted_mode = False):
    '''
    Launches a panel specified by arguments.
    '''
    print("Launching panel for %s at position %s"%(username, panel_location))
    while True:
        copy_userdata_output = copy_userdata(steamid, map_name = map_name)
        if copy_userdata_output:
            break

    x, y = get_panel_location(panel_location)
    
    base_command = 'C:\Program Files (x86)\Steam\steam.exe '
    steam_arguments = '-login %s %s -applaunch 730 -nobrowser -console -novid -nosound -window -w 640 -h 480 -x %d -y %d -low +exec afk -nohltv'%(username, password, x, y)
    if trusted_mode is False:
        steam_arguments+= ' -allow_third_party_software'
    
    subproc = subprocess.Popen(base_command + steam_arguments)
    
    return subproc
    
def get_panel_pids(username, password, steamid, panel_location, PIDs, launch_timeout = 35, trusted_mode = False, map_name = "anubis", clear_old_instance = False):
    '''
    Launches a panel and returns updated PIDs.
    '''
    # launching panel
    print(steamid)
    if clear_old_instance:
        kill_PIDs(subproc)
    PIDs[panel_location] = launch_panel(username, password, steamid, panel_location, map_name = map_name, trusted_mode = trusted_mode)
    # Checking panel 
    time.sleep(launch_timeout)
    return PIDs

def save_PIDs(PIDs, PIDs_dict = None):
    '''
    Save PIDs and PIDs_dict.
    '''
    with open(os.path.join('temp', 'PIDs.pkl'), 'wb') as file:
        pickle.dump(PIDs, file)
#%%
# def relaunch_panels(PIDs, PIDs_dict, panel_locations, map_name = "anubis", trusted_mode = False):
#     '''
#     Re-launches the panels provided and updates the PIDs and PIDs_dict.
#     '''
#     USERNAME_UPPER, PASSWORD_UPPER, STEAM_ID_UPPER, USERNAME_LOWER, PASSWORD_LOWER, STEAM_ID_LOWER = get_accounts()
#     for panel_location in panel_locations: #panel_location = panel_locations[0]
#         PIDs, PIDs_dict = kill_PIDs(PIDs, PIDs_dict, panel_location)
#         if panel_location[0] == 'u':
#             USERNAME, PASSWORD, STEAM_ID = USERNAME_UPPER.copy(), PASSWORD_UPPER.copy(), STEAM_ID_UPPER.copy()
#         if panel_location[0] == 'l':
#             USERNAME, PASSWORD, STEAM_ID = USERNAME_LOWER.copy(), PASSWORD_LOWER.copy(), STEAM_ID_LOWER.copy()
        
#         PIDs, PIDs_dict = get_panel_pids(USERNAME[int(panel_location[1]) - 1], 
#                                          PASSWORD[int(panel_location[1]) - 1], 
#                                          STEAM_ID[int(panel_location[1]) - 1], 
#                                          panel_location, PIDs, PIDs_dict, trusted_mode = trusted_mode, map_name = map_name)
#     return PIDs, PIDs_dict

def relaunch_panels_and_ready(PIDs, panel_locations, map_name = "anubis", trusted_mode = False, after_launch_timeout = 120):
    '''
    Re-launches the panels provided and updates the PIDs.
    '''
    if type(panel_locations) != list:
        panel_locations = [panel_locations]

    USERNAME_UPPER, PASSWORD_UPPER, STEAM_ID_UPPER, USERNAME_LOWER, PASSWORD_LOWER, STEAM_ID_LOWER = get_accounts()
    for panel_location in panel_locations: #panel_location = panel_locations[0]
        PIDs = kill_PIDs(PIDs, panel_location)
        if panel_location[0] == 'u':
            USERNAME, PASSWORD, STEAM_ID = USERNAME_UPPER.copy(), PASSWORD_UPPER.copy(), STEAM_ID_UPPER.copy()
        if panel_location[0] == 'l':
            USERNAME, PASSWORD, STEAM_ID = USERNAME_LOWER.copy(), PASSWORD_LOWER.copy(), STEAM_ID_LOWER.copy()
        
        PIDs = get_panel_pids(USERNAME[int(panel_location[1]) - 1], 
                                         PASSWORD[int(panel_location[1]) - 1], 
                                         STEAM_ID[int(panel_location[1]) - 1], 
                                         panel_location, PIDs, trusted_mode = trusted_mode, map_name = map_name)
    t_ = after_launch_timeout
    time.sleep(t_) 
    for panel_location in panel_locations:
        x, y = get_panel_location(panel_location)
        output = ready_panel(x, y, untrusted_check = trusted_mode)
        if output == True:
            PIDS = relaunch_panels_and_ready(PIDs, panel_locations, map_name, trusted_mode, after_launch_timeout)
    return PIDs

def kill_PIDs(PIDs, panel):                                                    # Kill Panels with given panel_ids
    if type(panel) != list:
        panel = [panel]
    for i in panel:
        print('Killing process %s'%(i))
        subproc = PIDs[i]
        subproc.terminate()
        PIDs[i] = ""
    time.sleep(10)
    print("Killing csgo.exe not responding PIDs after 10 seconds wait.")
    not_responding_pids = get_not_responding_csgo_pids()
    kill_not_responding_csgo_pids(not_responding_pids)
    return PIDs

def get_not_responding_csgo_pids():
    r = os.popen('tasklist /v /fi "imagename eq csgo.exe"').read().strip().split('\n')[2:]
    not_responding_panels = []
    for i in r:#i = r[0]
        if "Not Responding" in i: not_responding_panels.append(int(i.split()[1]))
    return not_responding_panels

def get_total_csgo_panels():
    r = os.popen('tasklist /v /fi "imagename eq csgo.exe"').read().strip().split('\n')[2:]
    accepted_pids = 0
    for pid in r:
        pid = pid.split()
        if int(pid[4].replace(",", "")) > 16384:
            accepted_pids+=1
    return accepted_pids

def kill_not_responding_csgo_pids(pids):
    os_command = "taskkill /f "
    for pid in pids:
        os_command += "/pid %d "%(pid)
    os.system(os_command)
    time.sleep(0.2)
    os.system("taskkill /im cmd.exe")


def get_top_left_position_from_panel_name(panel_name = "u1", include_account_details = False): # Get the top left coordinates of the panel using panel names
    USERNAME_UPPER, PASSWORD_UPPER, STEAM_ID_UPPER, USERNAME_LOWER, PASSWORD_LOWER, STEAM_ID_LOWER = get_accounts()
    batch = panel_name[0]
    number = int(panel_name[1]) - 1
    if batch == 'u':
        if include_account_details:
            return CSGO_UPPER_POS_X[number], CSGO_UPPER_POS_Y[number], [USERNAME_UPPER[number], PASSWORD_UPPER[number], STEAM_ID_UPPER[number]]
        else:
            return CSGO_UPPER_POS_X[number], CSGO_UPPER_POS_Y[number]
    elif batch == 'l':
        if include_account_details:
            return CSGO_LOWER_POS_X[number], CSGO_LOWER_POS_Y[number], [USERNAME_LOWER[number], PASSWORD_LOWER[number], STEAM_ID_LOWER[number]]
        else:
            return CSGO_LOWER_POS_X[number], CSGO_LOWER_POS_Y[number]
#%%

def check_launched_panel(test_image = None, checker_image = None, POS_X = None, POS_Y = None):
    after_launch_console_x_1, after_launch_console_y_1 = 271, 51
    after_launch_console_x_2, after_launch_console_y_2 = 410, 63
    if checker_image is None:
        checker_image = np.load(os.path.join('warning_snippets', 'after_launch_console.npy'))
    if test_image is None:
        time.sleep(0.05)
        test_image = ImageGrab.grab([POS_X + after_launch_console_x_1, 
                                     POS_Y + after_launch_console_y_1, 
                                     POS_X + after_launch_console_x_2, 
                                     POS_Y + after_launch_console_y_2])
    
    test_image = np.array(test_image)
    return np.all(test_image == checker_image)

def check_launched_panel_wrapper(checker_image = None):                        # Check launched panel.
    after_launch_console_x_1, after_launch_console_y_1 = 271, 51
    after_launch_console_x_2, after_launch_console_y_2 = 410, 63

    if checker_image is None:
        checker_image = np.load(os.path.join('warning_snippets', 'after_launch_console.npy'))

    test_image_outputs = []

    for i in range(5):
        click_only(CSGO_UPPER_POS_X[i] + CSGO_TITLE_BAR_X[i], CSGO_UPPER_POS_Y[i] + CSGO_TITLE_BAR_Y[i], 0.1)

        if not check_launched_panel(test_image = None, checker_image = checker_image, POS_X = CSGO_UPPER_POS_X[i], POS_Y = CSGO_UPPER_POS_Y[i]):
            test_image_outputs.append("u" + str(i+1))

        click_only(CSGO_LOWER_POS_X[i] + CSGO_TITLE_BAR_X[i], CSGO_LOWER_POS_Y[i] + CSGO_TITLE_BAR_Y[i], 0.1)

        if not check_launched_panel(test_image = None, checker_image = checker_image, POS_X = CSGO_LOWER_POS_X[i], POS_Y = CSGO_LOWER_POS_Y[i]):
            test_image_outputs.append("l" + str(i+1))
    
    return test_image_outputs
#%%

# def clear_panel_untrusted(POS_X, POS_Y, number_of_times = 1):  #check and update image comparision
#     '''
#     Clears the untrusted mode error for the panel.
#     '''


def ready_panel(POS_X, POS_Y, untrusted_check = True, untrusted_check_times = 3, panel_number = 0, do = True):
    '''
    Loads exec file and optionally clears untrusted check.
    '''
    if not do: return None
    print("Panel %s"%(panel_number))
    click_only(POS_X + CSGO_TITLE_BAR_X[CSGO_UPPER_POS_X.index(POS_X)], POS_Y + CSGO_TITLE_BAR_Y[CSGO_UPPER_POS_X.index(POS_X)], 0.1)
    write_and_execute('disconnect;exec afk;+left', 0.25, 0.5)
    write_and_execute('disconnect;exec afk;+left', 0.25, 0.5)
#    press_and_release('`', 0.1, 1)
    press_and_release('esc', 0.25, 4)
    if untrusted_check: untrusted_check_times += 1
    press_and_release('esc', 0.2, 2)
    if cd_check_wrapper(False, POS_X, POS_Y):
        runfile('driver_code.py')
        sys.exit(0)
    for i in range(untrusted_check_times):
        press_and_release('esc', 0.2, 2)
        click_only(POS_X + CSGO_PLAY_BUTTON_X, POS_Y + CSGO_PLAY_BUTTON_Y, 0.25, 3)
        time.sleep(0.3)
        hover_only(POS_X + CSGO_GO_SEARCH_BUTTON_X, POS_Y + CSGO_GO_SEARCH_BUTTON_Y, 0.2, 0.12)
        hover_only(POS_X + CSGO_GO_SEARCH_BUTTON_X, POS_Y + CSGO_GO_SEARCH_BUTTON_Y, 0.2, 0.12)
        time.sleep(0.1)
        click_only(None, None, 0.5, 1)
        time.sleep(0.6)
        error_name = identify_and_clear_errors(all_panels = False, 
                                               error_coordinates = error_coordinates, 
                                               error_with_numpy_images = error_with_numpy_images, 
                                               error_ok_button = error_ok_button, 
                                               POS_X = POS_X, 
                                               POS_Y = POS_Y, 
                                               return_error_name = True)
        # hover_only(POS_X + CSGO_UNTRUSTED_CONTINUE_X, POS_Y + CSGO_UNTRUSTED_CONTINUE_Y, 0.25, 0.1)
        # click_only(None, None, 0.25, 2)
        # time.sleep(0.3)
        hover_only(POS_X + CSGO_PROFILE_HOVER_X, POS_Y + CSGO_PROFILE_HOVER_Y, 0.2, 0.1)
        click_only(POS_X + CSGO_LEAVE_LOBBY_X, POS_Y + CSGO_LEAVE_LOBBY_Y, 0.3, 3)
        # hover_only(CSGO_UPPER_POS_X[i] + CSGO_GO_SEARCH_BUTTON_X, CSGO_UPPER_POS_Y[i] + CSGO_GO_SEARCH_BUTTON_Y, 0.1, 0.07)
        # click_only(None, None, 0.5, 1)
        time.sleep(0.3)
        if error_name in ['invalid_signature_vac_error', 'invalid_signature_vac_error_2', 'vac_was_unable_to_verify_your_game_session']:
            return True

def get_friend_code_from_panel(POS_X, POS_Y):
    '''
    Get friend code from panel.
    '''
    import pyperclip as pc
    index = CSGO_UPPER_POS_X.index(POS_X)
    click_only(POS_X + CSGO_TITLE_BAR_X[index], POS_Y + CSGO_TITLE_BAR_Y[index], 0.1)
    time.sleep(0.2)
    hover_only(POS_X + CSGO_PROFILE_HOVER_X, POS_Y + CSGO_PROFILE_HOVER_Y, 0.2, 0.1)
    time.sleep(0.25)
    click_only(POS_X + CSGO_CANCEL_FRIEND_INVITE_X, POS_Y + CSGO_CANCEL_FRIEND_INVITE_Y, 0.2, 10)
    click_only(POS_X + CSGO_FRIEND_REQUEST_X, POS_Y + CSGO_FRIEND_REQUEST_Y, 0.4, 2)
    click_only(POS_X + CSGO_ADD_FRIEND_X, POS_Y + CSGO_ADD_FRIEND_Y, 0.4, 2)
    click_only(POS_X + CSGO_COPY_YOUR_CODE_X, POS_Y + CSGO_COPY_YOUR_CODE_Y, 0.4, 2)

    friend_code = pc.paste()

    click_only(POS_X + CSGO_CANCEL_X, POS_Y + CSGO_CANCEL_Y, 0.2, 3)
    
    return friend_code

def invite_teammate_using_friend_code(POS_X, POS_Y, invite_code):
    '''
    Invite the teammate using friend code.
    '''
    index = CSGO_UPPER_POS_X.index(POS_X)
    click_only(POS_X + CSGO_TITLE_BAR_X[index], POS_Y + CSGO_TITLE_BAR_Y[index], 0.3, 1)
    
    if invite_code is None:
        return
    
    if type(invite_code) != list:
        invite_code = [invite_code]
    
    for code in invite_code:
        hover_only(POS_X + CSGO_PROFILE_HOVER_X, POS_Y + CSGO_PROFILE_HOVER_Y, 0.2, 0.1)
        click_only(POS_X + CSGO_FRIEND_REQUEST_X, POS_Y + CSGO_FRIEND_REQUEST_Y, 0.2, 2)
        click_only(POS_X + CSGO_ADD_FRIEND_X, POS_Y + CSGO_ADD_FRIEND_Y, 0.2, 2)
        click_only(POS_X + CSGO_ENTER_FRIEND_CODE_X, POS_Y + CSGO_ENTER_FRIEND_CODE_Y, 0.2, 3)

        write_only(code, 0.5)
        click_only(POS_X + CSGO_ACCEPT_FRIEND_CODE_X, POS_Y + CSGO_ACCEPT_FRIEND_CODE_Y, 0.4, 2)
    
        click_only(POS_X + CSGO_SELECT_TEAMMATE_PROFILE_X, POS_Y + CSGO_SELECT_TEAMMATE_PROFILE_Y, 0.4, 2)
        click_only(POS_X + CSGO_INVITE_TEAMMATE_X, POS_Y + CSGO_INVITE_TEAMMATE_Y, 0.4, 2)
        click_only(POS_X + CSGO_CANCEL2_X, POS_Y + CSGO_CANCEL2_Y, 0.2, 3)
    
def accept_invite_from_team_leader(POS_X, POS_Y, select_panel_needed = True):
    '''
    Accepts team leader invite.
    '''
    index = CSGO_UPPER_POS_X.index(POS_X)
    if select_panel_needed:
        click_only(POS_X + CSGO_TITLE_BAR_X[index], POS_Y + CSGO_TITLE_BAR_Y[index], 0.1)
    hover_only(POS_X + CSGO_PROFILE_HOVER_X, POS_Y + CSGO_PROFILE_HOVER_Y, 0.7, 0.12)
    click_only(POS_X + CSGO_ACCEPT_INVITE_X, POS_Y + CSGO_ACCEPT_INVITE_Y, 0.2, 5)

def check_friend_code_by_username(friend_code_dict, username):
    '''
    Checks for friend code using username from database.
    '''
    try:
        friend_code = friend_code_dict[username]
    except:
        friend_code = None
    
    return friend_code

def add_friend_code_by_username(friend_code_dict, username, friend_code):
    '''
    Creates new entry for friend code.
    '''
    friend_code_dict[username] = friend_code

def load_friend_code_dict_file(file_path = os.path.join('friend_codes.pkl')):
    '''
    Loads the friend codes database.
    '''
    # if os.path.isfile(file_path):
    #     mode = 'rb'
    #     with open(file_path, mode) as file:
    #         friend_code_dict = pickle.load(file)
    # else:
    #     friend_code_dict = {}
        
    # return friend_code_dict
    return {}

def save_friend_code_dict_file(friend_code_dict, file_path = os.path.join('friend_codes.pkl')):
    '''
    Saves the friend codes database.
    '''
    try:
        mode = 'wb'
        with open(file_path, mode) as file:
            pickle.dump(friend_code_dict, file)
        return True
    except:
        print("Error saving friend codes")
        with open(os.path.join('temp', 'friend_codes.pkl'), 'wb') as file:
            pickle.dump(friend_code_dict, file)
        return False

def create_lobby(BATCH_POS_X, BATCH_POS_Y, BATCH_USERNAME):
    friend_code_dict = load_friend_code_dict_file()
    FRIEND_CODES = []
    error_name = identify_and_clear_errors(all_panels = False, 
                                                   error_coordinates = error_coordinates, 
                                                   error_with_numpy_images = error_with_numpy_images, 
                                                   error_ok_button = error_ok_button, 
                                                   POS_X = BATCH_POS_X[0], 
                                                   POS_Y = BATCH_POS_Y[0], 
                                                   return_error_name = True)
    for i in range(4, 0, -1):
        friend_code = check_friend_code_by_username(friend_code_dict, BATCH_USERNAME[i])
        if friend_code is None:
            friend_code = get_friend_code_from_panel(BATCH_POS_X[i], BATCH_POS_Y[i])
            add_friend_code_by_username(friend_code_dict, BATCH_USERNAME[i], friend_code)
        FRIEND_CODES.append(friend_code)
    FRIEND_CODES.reverse()
    invite_teammate_using_friend_code(BATCH_POS_X[0], BATCH_POS_Y[0], FRIEND_CODES)
    
    for i in range(1, 5):
        error_name = identify_and_clear_errors(all_panels = False, 
                                                       error_coordinates = error_coordinates, 
                                                       error_with_numpy_images = error_with_numpy_images, 
                                                       error_ok_button = error_ok_button, 
                                                       POS_X = BATCH_POS_X[i], 
                                                       POS_Y = BATCH_POS_Y[i], 
                                                       return_error_name = True)
        accept_invite_from_team_leader(BATCH_POS_X[i], BATCH_POS_Y[i], select_panel_needed = True)
    
    save_friend_code_dict_file(friend_code_dict)

#%% LOBBY 5/5 GREEN CHECK
def check_green_mm_search(test_image = None, checker_image = None, POS_X = None, POS_Y = None):
    '''
    Checks for current panel to see if during search, it is showing 5/5.
    '''
    green_mm_check_x_1, green_mm_check_y_1 = 611, 61
    green_mm_check_x_2, green_mm_check_y_2 = 631, 77

    if checker_image is None:
        checker_image = np.load(os.path.join('warning_snippets', "lobby_5_by_5_green.npy"))
    
    if test_image is None:
        test_image = ImageGrab.grab([POS_X + green_mm_check_x_1, 
                                     POS_Y + green_mm_check_y_1, 
                                     POS_X + green_mm_check_x_2, 
                                     POS_Y + green_mm_check_y_2])
    
    test_image = np.array(test_image)
    
    return np.all(test_image == checker_image)

def check_green_mm_search_wrapper(arrangement_needed = False, checker_image = None):
    '''
    Checks all panels to se if during search, it's showing 5/5.
    '''
    green_mm_check_x_1, green_mm_check_y_1 = 611, 61
    green_mm_check_x_2, green_mm_check_y_2 = 631, 77

    if checker_image is None:
        checker_image = np.load(os.path.join('warning_snippets', "lobby_5_by_5_green.npy"))

    if arrangement_needed:
        for i in range(4, -1, -1):
            click_only(CSGO_UPPER_POS_X[i] + CSGO_TITLE_BAR_X[i], CSGO_UPPER_POS_Y[i] + CSGO_TITLE_BAR_Y[i], 0.1)
            click_only(CSGO_UPPER_POS_X[i] + CSGO_PLAY_BUTTON_X, CSGO_UPPER_POS_Y[i] + CSGO_PLAY_BUTTON_Y, 0.1, 4)
            click_only(CSGO_LOWER_POS_X[i] + CSGO_TITLE_BAR_X[i], CSGO_LOWER_POS_Y[i] + CSGO_TITLE_BAR_Y[i], 0.1)
            click_only(CSGO_LOWER_POS_X[i] + CSGO_PLAY_BUTTON_X, CSGO_LOWER_POS_Y[i] + CSGO_PLAY_BUTTON_Y, 0.1, 4)

    time.sleep(0.5)
    
    test_image = ImageGrab.grab()
    test_image_snippets_upper, test_image_snippets_lower = [], []
    for i in range(5):#i = 0
        test_snippet = test_image.crop([CSGO_UPPER_POS_X[i] + green_mm_check_x_1, 
                                        CSGO_UPPER_POS_Y[i] + green_mm_check_y_1, 
                                        CSGO_UPPER_POS_X[i] + green_mm_check_x_2, 
                                        CSGO_UPPER_POS_Y[i] + green_mm_check_y_2])        
        if not check_green_mm_search(test_image = test_snippet, checker_image = checker_image):
            test_image_snippets_upper.append(["u" + str(i+1)])

        test_snippet = test_image.crop([CSGO_LOWER_POS_X[i] + green_mm_check_x_1, 
                                        CSGO_LOWER_POS_Y[i] + green_mm_check_y_1, 
                                        CSGO_LOWER_POS_X[i] + green_mm_check_x_2, 
                                        CSGO_LOWER_POS_Y[i] + green_mm_check_y_2])        
        if not check_green_mm_search(test_image = test_snippet, checker_image = checker_image):
            test_image_snippets_lower.append(["l" + str(i+1)])
    print(*test_image_snippets_upper)
    print(*test_image_snippets_lower)
    if test_image_snippets_lower != []:
        leave_lobby("lower")
        create_lobby(CSGO_LOWER_POS_X, CSGO_LOWER_POS_Y, USERNAME_LOWER)
    if test_image_snippets_upper != []:
        leave_lobby("upper")
        create_lobby(CSGO_UPPER_POS_X, CSGO_UPPER_POS_Y, USERNAME_UPPER)
    
    if test_image_snippets_lower != [] or test_image_snippets_upper != []:
        return True
    else:
        return False

def leave_lobby(batch):
    '''
    Lobby is left by all panels of the given batch.
    '''
    if batch in ['upper', 'u']:
        POS_X, POS_Y = CSGO_UPPER_POS_X.copy(), CSGO_UPPER_POS_Y.copy()
    elif batch in ['lower', 'l']:
        POS_X, POS_Y = CSGO_LOWER_POS_X.copy(), CSGO_LOWER_POS_Y.copy()
        
    for i in [1, 2, 3, 0, 4]:
        click_only(POS_X[i] + CSGO_TITLE_BAR_X[i], POS_Y[i] + CSGO_TITLE_BAR_Y[i], 0.1)
        time.sleep(0.25)
        hover_only(POS_X[i] + CSGO_PROFILE_HOVER_X, POS_Y[i] + CSGO_PROFILE_HOVER_Y, 0.2, 0.1)
        time.sleep(0.25)
        click_only(POS_X[i] + CSGO_LEADER_LEAVE_LOBBY_X, POS_Y[i] + CSGO_LEADER_LEAVE_LOBBY_Y, 0.3, 3)
        time.sleep(0.15)
        click_only(POS_X[i] + CSGO_LEAVE_LOBBY_X, POS_Y[i] + CSGO_LEAVE_LOBBY_Y, 0.3, 3)
        time.sleep(0.15)
#%%

def map_loading_check(map_name = "anubis", method = "all", test_image = None, checker_image_array = None):
    '''
    Checks whether map is loaded or not.
    '''
    map_loading_check_x_1, map_loading_check_y_1 = 84, 93
    map_loading_check_x_2, map_loading_check_y_2 = 120, 127
    
    if checker_image_array is None:
        checker_image_array = np.load(os.path.join('warning_snippets', map_name + "_map_loading.npy"))
    
    if test_image is None:
        # test_image = Image.open(os.path.join("screenshots", "Screenshot (45).png")).convert("RGB")
        test_image = ImageGrab.grab()
    test_image_array = np.array(test_image)
    
    if method == 'all':
        test_image_snippets_upper = [i for i in range(5) if not np.all(test_image_array[CSGO_UPPER_POS_Y[i] + map_loading_check_y_1: CSGO_UPPER_POS_Y[i] + map_loading_check_y_2, 
                                                                                        CSGO_UPPER_POS_X[i] + map_loading_check_x_1: CSGO_UPPER_POS_X[i] + map_loading_check_x_2, 
                                                                                        :] == checker_image_array)]
        test_image_snippets_lower = [i for i in range(5) if not np.all(test_image_array[CSGO_LOWER_POS_Y[i] + map_loading_check_y_1: CSGO_LOWER_POS_Y[i] + map_loading_check_y_2, 
                                                                                        CSGO_LOWER_POS_X[i] + map_loading_check_x_1: CSGO_LOWER_POS_X[i] + map_loading_check_x_2, 
                                                                                        :] == checker_image_array)]
        return test_image_snippets_upper, test_image_snippets_lower
    elif method == 'upper':
        test_image_snippets_upper = [i for i in range(5) if not np.all(test_image_array[CSGO_UPPER_POS_Y[i] + map_loading_check_y_1: CSGO_UPPER_POS_Y[i] + map_loading_check_y_2, 
                                                                                        CSGO_UPPER_POS_X[i] + map_loading_check_x_1: CSGO_UPPER_POS_X[i] + map_loading_check_x_2, 
                                                                                        :] == checker_image_array)]
        return test_image_snippets_upper
    elif method == "lower":
        test_image_snippets_lower = [i for i in range(5) if not np.all(test_image_array[CSGO_LOWER_POS_Y[i] + map_loading_check_y_1: CSGO_LOWER_POS_Y[i] + map_loading_check_y_2, 
                                                                                        CSGO_LOWER_POS_X[i] + map_loading_check_x_1: CSGO_LOWER_POS_X[i] + map_loading_check_x_2, 
                                                                                        :] == checker_image_array)]
        return test_image_snippets_lower

def map_loading_check_wrapper(map_name = "anubis", method = "all", max_time = 15, checker_image_array = None):
    '''
    Map loading Wrapper.
    '''
    if checker_image_array is None:
        checker_image_array = np.load(os.path.join('warning_snippets', map_name + "_map_loading.npy"))
    
    timer = 0
    panels_connected = False
    
    if method == 'all':
        while not panels_connected and timer < max_time:
            #test_image = Image.open(os.path.join("screenshots", "Screenshot (45).png")).convert("RGB")            
            test_image = ImageGrab.grab()
            check_upper, check_lower = map_loading_check(map_name = map_name, method = method, test_image = test_image, checker_image_array = checker_image_array)
            
            if check_upper == check_lower == list(range(5)):
                panels_connected = True
            
            elif check_upper != [] or check_lower != []:
                timer+=1
            
            if check_upper == check_lower == []:
                print("Loading...")
            
            time.sleep(1)
        if timer == max_time:
            # TODO FUNCTION TO CANCEL MATCH
            #print(check_upper, check_lower)
            return check_upper, check_lower
        
    if method in ['u', 'upper']:
        while not panels_connected and timer < max_time:
            test_image = ImageGrab.grab()
            check_upper = map_loading_check(map_name = map_name, method = method, test_image = test_image, checker_image_array = checker_image_array)
            if check_upper == list(range(5)):
                panels_connected = True
            
            elif check_upper != []:
                timer+=1

            if check_upper == []:
                print("Loading...")
            
            time.sleep(1)
        if timer == max_time:
            # TODO FUNCTION TO CANCEL MATCH
            return check_upper

    if method in ['l', 'lower']:
        while not panels_connected and timer < max_time:
            test_image = ImageGrab.grab()
            check_lower = map_loading_check(map_name = map_name, method = method, test_image = test_image, checker_image_array = checker_image_array)
            
            if check_lower == list(range(5)):
                panels_connected = True
            
            elif check_lower != []:
                timer+=1

            if check_lower == []:
                print("Loading...")
            
            time.sleep(1)
        if timer == max_time:
            # TODO FUNCTION TO CANCEL MATCH
            return check_lower
    return True
#%%

def accept_match():
    '''
    Match Accept.
    '''
    upper_batch = [CSGO_UPPER_POS_X, CSGO_UPPER_POS_Y]
    lower_batch = [CSGO_LOWER_POS_X, CSGO_LOWER_POS_Y]
    
    for i in range(5): #i = 0
        for batch in [upper_batch, lower_batch]: #batch = lower_batch.copy()
            POS_X, POS_Y = batch
            click_only(POS_X[i] + CSGO_TITLE_BAR_X[i], 
                       POS_Y[i] + CSGO_TITLE_BAR_Y[i], 0.1)
            press_and_release('esc', 0.2, 1)
            click_only(POS_X[i] + CSGO_ACCEPT_BUTTON_X, 
                       POS_Y[i] + CSGO_ACCEPT_BUTTON_Y, 0.1, 2)
    click_only(0, 0, 0.1, 1)
            
def auto_accept_check(): #needs update as per long time
    '''
    Runs auto accept checker. Calls function accordingly to fix MM or run auto accept.
    '''
    max_time = 1800
    timer = 0
    count = 0
    while True:
        if accept_check(CSGO_UPPER_POS_X[4], CSGO_UPPER_POS_Y[4]) or accept_check(CSGO_LOWER_POS_X[4], CSGO_LOWER_POS_Y[4]):
            time.sleep(1)
        
        if accept_check(CSGO_UPPER_POS_X[4], CSGO_UPPER_POS_Y[4]) and accept_check(CSGO_LOWER_POS_X[4], CSGO_LOWER_POS_Y[4]):
                print("...Match found!...")
                accept_match()
                break
        
        #TODO scraping the optimized code to the bottom (comment), use later.
        elif accept_check(CSGO_UPPER_POS_X[4], CSGO_UPPER_POS_Y[4]):
            if accept_check(CSGO_UPPER_POS_X[4], CSGO_UPPER_POS_Y[4]) and accept_check(CSGO_LOWER_POS_X[4], CSGO_LOWER_POS_Y[4]):
                    print("...Match found!...")
                    accept_match()
                    break
    
            print("Match found for upper batch. USER Monitoring needed.")
            fix_mm_search(batch = "upper")
    
        elif accept_check(CSGO_LOWER_POS_X[4], CSGO_LOWER_POS_Y[4]):
            if accept_check(CSGO_UPPER_POS_X[4], CSGO_UPPER_POS_Y[4]) and accept_check(CSGO_LOWER_POS_X[4], CSGO_LOWER_POS_Y[4]):
                    print("...Match found!...")
                    accept_match()
                    break
    
            print("Match found for lower batch. USER Monitoring needed.")
            fix_mm_search(batch = "lower")

        if count%20 == 0:
            restart_if_panel_not_responding()
        count+=1
        timer+=1
        time.sleep(0.5)
        if count%60 == 0:
            error_check_during_search()

        print("Not found yet.")
        if timer >= max_time:
            with open("number_of_matches_played.txt", 'r') as file:
                matches_played = file.read()
            del file
            return matches_played
    # TODO launch auto dc rc from here or later?
    #auto_dc_rc_wrapper(match_output = 'tie', map_name = 'anubis')

def error_check_during_search():
    error_outputs = []
    for i in range(4, -1, -1):
        time.sleep(0.1)
        click_only(CSGO_UPPER_POS_X[i] + CSGO_TITLE_BAR_X[i], CSGO_UPPER_POS_Y[i] + CSGO_TITLE_BAR_Y[i], 0.1, 1)
        time.sleep(0.1)
        error_name = identify_and_clear_errors(all_panels = False, 
                                               error_coordinates = error_coordinates, 
                                               error_with_numpy_images = error_with_numpy_images, 
                                               error_ok_button = error_ok_button, 
                                               POS_X = CSGO_UPPER_POS_X[i], 
                                               POS_Y = CSGO_UPPER_POS_Y[i], 
                                               return_error_name = True)
        if error_name is not None:
            error_outputs.append(error_name)
        time.sleep(0.1)
        click_only(CSGO_LOWER_POS_X[i] + CSGO_TITLE_BAR_X[i], CSGO_LOWER_POS_Y[i] + CSGO_TITLE_BAR_Y[i], 0.1, 1)
        time.sleep(0.1)
        error_name = identify_and_clear_errors(all_panels = False, 
                                               error_coordinates = error_coordinates, 
                                               error_with_numpy_images = error_with_numpy_images, 
                                               error_ok_button = error_ok_button, 
                                               POS_X = CSGO_LOWER_POS_X[i], 
                                               POS_Y = CSGO_LOWER_POS_Y[i], 
                                               return_error_name = True)
        if error_name is not None:
            error_outputs.append(error_name)
        
    if error_outputs == []:
        return False
    else:
        leave_lobby("upper")
        leave_lobby("lower")
        
        restart_if_panel_not_responding()
        
        create_lobby(CSGO_UPPER_POS_X, CSGO_UPPER_POS_Y, USERNAME_UPPER)
        create_lobby(CSGO_LOWER_POS_X, CSGO_LOWER_POS_Y, USERNAME_LOWER)
        
        after_lobby_blue_check_wrapper(arrangement_needed = True, checker_image = None)
        
        start_mm_search(arrangement_needed = True)
        
        identify_and_clear_errors(all_panels = True, error_coordinates = error_coordinates, error_with_numpy_images = error_with_numpy_images, 
                                  error_ok_button = error_ok_button)
        return True


def auto_dc_rc_wrapper(match_output = 'tie', map_name = 'anubis', winner = 'upper', score = [16, 14], current_score = [0, 0]): # needs fix
    '''
    Match Wrapper. Decides the outcome of the match.
    '''
    match_output = match_output.lower()
    winner = winner.lower()
    map_name = map_name.lower()
    
    if match_output in ['tie', 't', 'equal', 'tied']:
        print("-----------------------")
        print("Match will be tied.")
        print("-----------------------")
        
    else:
        print("-----------------------")
        print("%s lobby will won the match with score %d-%d."%(winner, score[0], score[1]))
        print("-----------------------")
        score[0]-=2   #making winner score = 14
        if current_score != [0, 0]:
            #current 2 4 w r t winner
            #winner  16 14 w r t winner
            if current_score[0] > score[0] or current_score[1] > score[1]:
                print("Error. Not possible. Please check the arguments.")
                raise Exception
            score[0] -= current_score[0]
            score[1] -= current_score[1]
        
        # TODO launch auto dc rc winlose file/function
        
def fix_mm_search(batch = "upper"):
    '''
    Fixes MM on mismatch.
    '''
    UPPER_PANEL_1 = [CSGO_UPPER_POS_X[0], CSGO_UPPER_POS_Y[0]] ##TODO CORRECTION AND FIX PANEL 
    LOWER_PANEL_1 = [CSGO_LOWER_POS_X[0], CSGO_LOWER_POS_Y[0]]
    
    if batch == "upper":
        delay_stop_panel = [CSGO_UPPER_POS_X[0], CSGO_UPPER_POS_Y[0]]
        instant_stop_panel = [CSGO_LOWER_POS_X[0], CSGO_LOWER_POS_Y[0]]
    else: #if args.batch == "lower":
        delay_stop_panel = [CSGO_LOWER_POS_X[0], CSGO_LOWER_POS_Y[0]]
        instant_stop_panel = [CSGO_UPPER_POS_X[0], CSGO_UPPER_POS_Y[0]]
    
    # Stopping instant batch
    click_only(instant_stop_panel[0] + CSGO_TITLE_BAR_X[0], instant_stop_panel[1] + CSGO_TITLE_BAR_Y[0], 0.25)    
    press_and_release('esc', 0.5, 2)
    click_only(instant_stop_panel[0] + CSGO_PLAY_BUTTON_X, instant_stop_panel[1] + CSGO_PLAY_BUTTON_Y, 0.3, 3)
    hover_only(instant_stop_panel[0] + CSGO_PROFILE_HOVER_X, instant_stop_panel[1] + CSGO_PROFILE_HOVER_Y, 0.2, 0.1)
    time.sleep(0.4)
    hover_only(instant_stop_panel[0] + CSGO_CANCEL_SEARCH_X, instant_stop_panel[1] + CSGO_CANCEL_SEARCH_Y, 0.3, 0.1)
    click_only(None, None, 0.3, 3)
    time.sleep(0.8)
    
    # Closing developer mode on delay panel
    click_only(delay_stop_panel[0] + CSGO_TITLE_BAR_X[0], delay_stop_panel[1] + CSGO_TITLE_BAR_Y[0], 0.25)    
    press_and_release('esc', 0.5, 2)
    
    while accept_check(delay_stop_panel[0], delay_stop_panel[1]):
        time.sleep(0.5)
        continue
    
    # Stopping delay batch
    click_only(delay_stop_panel[0] + CSGO_TITLE_BAR_X[0], delay_stop_panel[1] + CSGO_TITLE_BAR_Y[0], 0.25)
    hover_only(delay_stop_panel[0] + CSGO_PROFILE_HOVER_X, delay_stop_panel[1] + CSGO_PROFILE_HOVER_Y, 0.2, 0.1)
    time.sleep(0.4)
    hover_only(delay_stop_panel[0] + CSGO_CANCEL_SEARCH_X, delay_stop_panel[1] + CSGO_CANCEL_SEARCH_Y, 0.3, 0.1)
    click_only(None, None, 0.3, 3)
    
    # # Cooldown time
    t2, t3 = 5, 50
    print("Waiting %d for possible time error"%t2)
    time.sleep(t2)
    print("Waiting %d for MM to reset search cooldown."%t3)
    time.sleep(t3)
    
    click_only(instant_stop_panel[0] + CSGO_TITLE_BAR_X[0], instant_stop_panel[1] + CSGO_TITLE_BAR_Y[0], 0.25)    
    click_only(instant_stop_panel[0] + CSGO_PLAY_BUTTON_X, instant_stop_panel[1] + CSGO_PLAY_BUTTON_Y, 0.5, 4)
    time.sleep(0.4)
    hover_only(instant_stop_panel[0] + CSGO_GO_SEARCH_BUTTON_X, instant_stop_panel[1] + CSGO_GO_SEARCH_BUTTON_Y, 0.5, 0.25)
    click_only(None, None, 0.5, 1)
    time.sleep(0.8)
    #press_and_release('`', 0.5, 1)
    
    # Re-Search
    click_only(delay_stop_panel[0] + CSGO_TITLE_BAR_X[0], delay_stop_panel[1] + CSGO_TITLE_BAR_Y[0], 0.25)    
    click_only(delay_stop_panel[0] + CSGO_PLAY_BUTTON_X, delay_stop_panel[1] + CSGO_PLAY_BUTTON_Y, 0.5, 4)
    time.sleep(0.4)
    hover_only(delay_stop_panel[0] + CSGO_GO_SEARCH_BUTTON_X, delay_stop_panel[1] + CSGO_GO_SEARCH_BUTTON_Y, 0.5, 0.25)
    click_only(None, None, 0.5, 1)
    time.sleep(0.8)
    #press_and_release('`', 0.5, 1)

#%%   temp_blue_lobby_error_check.
def after_lobby_blue_check(checker_image = None, POS_X = None, POS_Y = None, leader = True):
    blue_lobby_5_by_5_lobby_leader_x_1, blue_lobby_5_by_5_lobby_leader_y_1 = 611, 33
    blue_lobby_5_by_5_lobby_leader_x_2, blue_lobby_5_by_5_lobby_leader_y_2 = 631, 49

    blue_lobby_5_by_5_x_1, blue_lobby_5_by_5_y_1 = 611, 61
    blue_lobby_5_by_5_x_2, blue_lobby_5_by_5_y_2 = 631, 77

    if checker_image is None:
        checker_image = np.load(os.path.join("error_snippets", "blue_lobby_check.npy"))
    

    index = CSGO_UPPER_POS_X.index(POS_X)
    #click_only(POS_X + CSGO_TITLE_BAR_X[index], POS_Y + CSGO_TITLE_BAR_Y[index], 0.1, 1)
    if leader:
        test_image = ImageGrab.grab([POS_X + blue_lobby_5_by_5_lobby_leader_x_1, 
                                     POS_Y + blue_lobby_5_by_5_lobby_leader_y_1, 
                                     POS_X + blue_lobby_5_by_5_lobby_leader_x_2, 
                                     POS_Y + blue_lobby_5_by_5_lobby_leader_y_2])
    else:
        test_image = ImageGrab.grab([POS_X + blue_lobby_5_by_5_x_1, 
                                     POS_Y + blue_lobby_5_by_5_y_1, 
                                     POS_X + blue_lobby_5_by_5_x_2, 
                                     POS_Y + blue_lobby_5_by_5_y_2])
    test_image = np.array(test_image)
    return np.all(test_image == checker_image)


def after_lobby_blue_check_wrapper(arrangement_needed = True, checker_image = None):
    blue_lobby_mark_x_1, blue_lobby_mark_y_1 = 601, 37
    blue_lobby_mark_x_2, blue_lobby_mark_y_2 = 603, 232

    if checker_image is None:
        checker_image = np.load(os.path.join("warning_snippets", "blue_lobby_check.npy"))
    
    exit_count = 0
    
    while True:
        if arrangement_needed:
            for i in range(4, -1, -1):
                click_only(CSGO_UPPER_POS_X[i] + CSGO_TITLE_BAR_X[i], CSGO_UPPER_POS_Y[i] + CSGO_TITLE_BAR_Y[i], 0.1)
                click_only(CSGO_UPPER_POS_X[i] + CSGO_PLAY_BUTTON_X, CSGO_UPPER_POS_Y[i] + CSGO_PLAY_BUTTON_Y, 0.1, 4)
                click_only(CSGO_LOWER_POS_X[i] + CSGO_TITLE_BAR_X[i], CSGO_LOWER_POS_Y[i] + CSGO_TITLE_BAR_Y[i], 0.1)
                click_only(CSGO_LOWER_POS_X[i] + CSGO_PLAY_BUTTON_X, CSGO_LOWER_POS_Y[i] + CSGO_PLAY_BUTTON_Y, 0.1, 4)
        
        time.sleep(0.4)
        test_snippets_upper, test_snippets_lower = [], []
        for i in range(5):
            if i == 0: leader = True
            else: leader = False
            if not after_lobby_blue_check(checker_image = checker_image, POS_X = CSGO_UPPER_POS_X[i], POS_Y = CSGO_UPPER_POS_Y[i], leader = leader):
                test_snippets_upper.append(i)
            if not after_lobby_blue_check(checker_image = checker_image, POS_X = CSGO_LOWER_POS_X[i], POS_Y = CSGO_LOWER_POS_Y[i], leader = leader):
                test_snippets_lower.append(i)
        
        print(test_snippets_upper, test_snippets_lower)
        
        if test_snippets_upper != []:
            identify_and_clear_errors(all_panels = True, error_coordinates = error_coordinates, error_with_numpy_images = error_with_numpy_images, 
                          error_ok_button = error_ok_button)
            leave_lobby("upper")
            create_lobby(CSGO_UPPER_POS_X, CSGO_UPPER_POS_Y, USERNAME_UPPER)
        if test_snippets_lower != []:
            identify_and_clear_errors(all_panels = True, error_coordinates = error_coordinates, error_with_numpy_images = error_with_numpy_images, 
                          error_ok_button = error_ok_button)
            leave_lobby("lower")
            create_lobby(CSGO_LOWER_POS_X, CSGO_LOWER_POS_Y, USERNAME_LOWER)
        
        if test_snippets_lower == test_snippets_upper == []:
            break
        exit_count+=1
        if exit_count == 8:
            accept_args = get_accept_args()
            runfile("main_file.py", accept_args)
            sys.exit(0)                                                       #TODO

#%%
def start_mm_search(arrangement_needed = True):
    if arrangement_needed:
        for i in range(4, -1, -1):
            click_only(CSGO_UPPER_POS_X[i] + CSGO_TITLE_BAR_X[i], CSGO_UPPER_POS_Y[i] + CSGO_TITLE_BAR_Y[i], 0.1)
            click_only(CSGO_UPPER_POS_X[i] + CSGO_PLAY_BUTTON_X, CSGO_UPPER_POS_Y[i] + CSGO_PLAY_BUTTON_Y, 0.1, 4)
            click_only(CSGO_LOWER_POS_X[i] + CSGO_TITLE_BAR_X[i], CSGO_LOWER_POS_Y[i] + CSGO_TITLE_BAR_Y[i], 0.1)
            click_only(CSGO_LOWER_POS_X[i] + CSGO_PLAY_BUTTON_X, CSGO_LOWER_POS_Y[i] + CSGO_PLAY_BUTTON_Y, 0.1, 4)
    
    time.sleep(0.8)
    hover_only(CSGO_UPPER_POS_X[0] + CSGO_GO_SEARCH_BUTTON_X, CSGO_UPPER_POS_Y[0] + CSGO_GO_SEARCH_BUTTON_Y, 0.5, 0.25)
    click_only(None, None, 0.5, 1)
    time.sleep(0.8)
    hover_only(CSGO_LOWER_POS_X[0] + CSGO_GO_SEARCH_BUTTON_X, CSGO_LOWER_POS_Y[0] + CSGO_GO_SEARCH_BUTTON_Y, 0.5, 0.25)
    click_only(None, None, 0.5, 1)
    time.sleep(0.8)

def stop_mm_search(arrangement_needed = True):
    if arrangement_needed:
        for i in range(4, -1, -1):
            click_only(CSGO_UPPER_POS_X[i] + CSGO_TITLE_BAR_X[i], CSGO_UPPER_POS_Y[i] + CSGO_TITLE_BAR_Y[i], 0.1)
            click_only(CSGO_UPPER_POS_X[i] + CSGO_PLAY_BUTTON_X, CSGO_UPPER_POS_Y[i] + CSGO_PLAY_BUTTON_Y, 0.1, 4)
            click_only(CSGO_LOWER_POS_X[i] + CSGO_TITLE_BAR_X[i], CSGO_LOWER_POS_Y[i] + CSGO_TITLE_BAR_Y[i], 0.1)
            click_only(CSGO_LOWER_POS_X[i] + CSGO_PLAY_BUTTON_X, CSGO_LOWER_POS_Y[i] + CSGO_PLAY_BUTTON_Y, 0.1, 4)
    
    time.sleep(0.8)
    hover_only(CSGO_UPPER_POS_X[0] + CSGO_GO_SEARCH_BUTTON_X, CSGO_UPPER_POS_Y[0] + CSGO_GO_SEARCH_BUTTON_Y, 0.5, 0.25)
    click_only(None, None, 0.5, 1)
    time.sleep(0.8)
    hover_only(CSGO_LOWER_POS_X[0] + CSGO_GO_SEARCH_BUTTON_X, CSGO_LOWER_POS_Y[0] + CSGO_GO_SEARCH_BUTTON_Y, 0.5, 0.25)
    click_only(None, None, 0.5, 1)
    time.sleep(0.8)

#%%
def failed_to_reach_servers_check(test_image = None, checker_image = None, POS_X = None, POS_Y = None):
    failed_to_match_any_official_servers_x_1, failed_to_match_any_official_servers_y_1 = 612, 59
    failed_to_match_any_official_servers_x_2, failed_to_match_any_official_servers_y_2 = 631, 76

    if checker_image is None:
        checker_image = np.load(os.path.join('warning_snippets', 'failed_to_reach_any_official_servers.npy'))
    
    if test_image is None:
        test_image = ImageGrab.grab([POS_X + failed_to_match_any_official_servers_x_1, 
                                     POS_Y + failed_to_match_any_official_servers_y_1, 
                                     POS_X + failed_to_match_any_official_servers_x_2, 
                                     POS_Y + failed_to_match_any_official_servers_y_2])
    test_image = np.array(test_image)
    
    check_outputs, check_output_counts = np.unique(test_image == checker_image, return_counts = True)
    false_counts = 0
    true_counts = 0
    if check_outputs[0] == False:
        false_counts = check_output_counts[0]
        try:
            true_counts = check_output_counts[1]
        except:
            pass
    elif check_outputs[0] == True:
        true_counts = check_output_counts[0]
        try:
            false_counts = check_output_counts[1]
        except:
            pass
    
    return True if true_counts >= 750 else False

def failed_to_reach_servers_full_check(POS_X, POS_Y, checker_full_image = None):
    failed_to_match_any_official_servers_full_x_1, failed_to_match_any_official_servers_full_y_1 = 484, 59
    failed_to_match_any_official_servers_full_x_2, failed_to_match_any_official_servers_full_y_2 = 616, 76

    if checker_full_image is None:
        checker_full_image = np.load(os.path.join('warning_snippets', 'failed_to_reach_any_official_servers_full.npy'))
    
    hover_only(POS_X + CSGO_PROFILE_HOVER_X, POS_Y + CSGO_PROFILE_HOVER_Y, 0.75, 0.1)
    
    test_image = ImageGrab.grab([POS_X + failed_to_match_any_official_servers_full_x_1, 
                                 POS_Y + failed_to_match_any_official_servers_full_y_1, 
                                 POS_X + failed_to_match_any_official_servers_full_x_2, 
                                 POS_Y + failed_to_match_any_official_servers_full_y_2])
    test_image_array = np.array(test_image)

    check_outputs, check_output_counts = np.unique(test_image_array == checker_full_image, return_counts = True)

    false_counts = 0
    true_counts = 0
    if check_outputs[0] == False:
        false_counts = check_output_counts[0]
        true_counts = check_output_counts[1]
    elif check_outputs[0] == True:
        true_counts = check_output_counts[0]
        false_counts = check_output_counts[1]
    
    return True if true_counts >= 5000 else False
    
#    return np.all(test_image_array == checker_full_image)

def failed_to_reach_servers_check_wrapper(arrangement_needed = True, checker_image = None, checker_full_image = None):
    failed_to_match_any_official_servers_x_1, failed_to_match_any_official_servers_y_1 = 612, 59
    failed_to_match_any_official_servers_x_2, failed_to_match_any_official_servers_y_2 = 631, 76

    failed_to_match_any_official_servers_full_x_1, failed_to_match_any_official_servers_full_y_1 = 484, 59
    failed_to_match_any_official_servers_full_x_2, failed_to_match_any_official_servers_full_y_2 = 616, 76
    
    panels_with_failed_connection = []

    if checker_image is None:
        checker_image = np.load(os.path.join('warning_snippets', 'failed_to_reach_any_official_servers.npy'))
    if checker_full_image is None:
        checker_full_image = np.load(os.path.join('warning_snippets', 'failed_to_reach_any_official_servers_full.npy'))
    
    if arrangement_needed == True:
        for i in range(4, -1, -1):
            click_only(CSGO_UPPER_POS_X[i] + CSGO_TITLE_BAR_X[i], CSGO_UPPER_POS_Y[i] + CSGO_TITLE_BAR_Y[i], 0.1)
            click_only(CSGO_UPPER_POS_X[i] + CSGO_PLAY_BUTTON_X, CSGO_UPPER_POS_Y[i] + CSGO_PLAY_BUTTON_Y, 0.1, 4)
            click_only(CSGO_LOWER_POS_X[i] + CSGO_TITLE_BAR_X[i], CSGO_LOWER_POS_Y[i] + CSGO_TITLE_BAR_Y[i], 0.1)
            click_only(CSGO_LOWER_POS_X[i] + CSGO_PLAY_BUTTON_X, CSGO_LOWER_POS_Y[i] + CSGO_PLAY_BUTTON_Y, 0.1, 4)
    time.sleep(1)
    
    test_image = ImageGrab.grab()
    
    for i in range(5): #upper
        output1 = failed_to_reach_servers_check(test_image = None, checker_image = checker_image, POS_X = CSGO_UPPER_POS_X[i], POS_Y = CSGO_UPPER_POS_Y[i])
        print(output1)
        if output1: # caution symbol
            panels_with_failed_connection.append("u"+str(i+1))
            # if failed_to_reach_servers_full_check(CSGO_UPPER_POS_X[i], CSGO_UPPER_POS_Y[i], checker_full_image):
            #     panels_with_failed_connection.append("u"+str(i+1))
            # TODO RELAUNCH
            #relaunch_panel("u" + str(i+1))

    for i in range(5): #lower
        output1 = failed_to_reach_servers_check(test_image = None, checker_image = checker_image, POS_X = CSGO_LOWER_POS_X[i], POS_Y = CSGO_LOWER_POS_Y[i])
        print(output1)
        if output1: # caution symbol
            panels_with_failed_connection.append("l" + str(i+1))
            # if failed_to_reach_servers_full_check(CSGO_LOWER_POS_X[i], CSGO_LOWER_POS_Y[i], checker_full_image):
            #     panels_with_failed_connection.append("l" + str(i+1))
                # TODO RELAUNCH
    
    return panels_with_failed_connection
    
#%%
def disconnect_batch(batch = "lower", return_errors = True): #modify as per needs or to add a function
    '''
    Disconnects given batch.
    '''
    if batch == "lower":
        POS_X, POS_Y = CSGO_LOWER_POS_X.copy(), CSGO_LOWER_POS_Y.copy()
    elif batch == "upper":
        POS_X, POS_Y = CSGO_UPPER_POS_X.copy(), CSGO_UPPER_POS_Y.copy()
    
    error_outputs = []
    
    for i in range(4, -1, -1):
        click_only(POS_X[i] + CSGO_TITLE_BAR_X[i], 
                   POS_Y[i] + CSGO_TITLE_BAR_Y[i], 0.1)
        identified_error = identify_and_clear_errors(all_panels = False, 
                                                     error_coordinates = error_coordinates, 
                                                     error_with_numpy_images = error_with_numpy_images, 
                                                     error_ok_button = error_ok_button, 
                                                     POS_X = POS_X[i], 
                                                     POS_Y = POS_Y[i], 
                                                     return_error_name = True)
        # TODO add function here
        press_and_release('F7', 0.1, 2)
        # identified_error = identify_and_clear_errors(all_panels = False, 
        #                                              error_coordinates = error_coordinates, 
        #                                              error_with_numpy_images = error_with_numpy_images, 
        #                                              error_ok_button = error_ok_button, 
        #                                              POS_X = POS_X[i], POS_Y = POS_Y[i], 
        #                                              return_error_name = True)

        if identified_error is not None:
            error_outputs.append(identified_error)
    
    return error_outputs

def reconnect_batch(batch = "lower"): #modify as per needs or to add a function
    '''
    Reconnects given batch.
    '''
    if batch == "lower":
        POS_X, POS_Y = CSGO_LOWER_POS_X.copy(), CSGO_LOWER_POS_Y.copy()
    elif batch == "upper":
        POS_X, POS_Y = CSGO_UPPER_POS_X.copy(), CSGO_UPPER_POS_Y.copy()
    
    error_outputs = []
    for i in range(5):
        identified_error = identify_and_clear_errors(all_panels = False, 
                                             error_coordinates = error_coordinates, 
                                             error_with_numpy_images = error_with_numpy_images, 
                                             error_ok_button = error_ok_button, 
                                             POS_X = POS_X[i], 
                                             POS_Y = POS_Y[i], 
                                             return_error_name = True)
        hover_only(POS_X[i] + CSGO_RECONNECT_BUTTON_X, POS_Y[i] + CSGO_RECONNECT_BUTTON_Y, 0.2, 0)
        click_only(POS_X[i] + CSGO_RECONNECT_BUTTON_X, POS_Y[i] + CSGO_RECONNECT_BUTTON_Y, 0.4, 1)
        # TODO ADD FUNCTION HERE
        if identified_error is not None:
            error_outputs.append(identified_error)

    click_only(0, 0, 0.1, 1)
    return error_outputs    

def disconnect_reconnect_batch(batch = 'upper', after_dc_wait_time = 7, after_rc_wait_time = 21, after_dc_wait = True, map_name = "anubis"):
    '''
    DC/RC
    '''
    disconnect_batch(batch = batch)
    
    if after_dc_wait:
        time.sleep(7 + 15 - after_dc_wait_time)
    
    reconnect_batch(batch = batch)
    
    time.sleep(3)
    loading_screen_output = map_loading_check_wrapper(map_name = map_name, method = batch, max_time = 20, checker_image_array = None)
    # TODO FIX loading_screen_fix
    time.sleep(7 + 15)
#%%
def load_ingame_win_icons():
    icon_dict = {}
    icon_dict['ingame_ct_win_icon'] = np.load(os.path.join('warning_snippets', 'ingame_ct_win_icon.npy'))
    icon_dict['ingame_ct_win_icon_left'] = np.load(os.path.join('warning_snippets', 'ingame_ct_win_icon_left.npy'))
    icon_dict['ingame_ct_win_icon_right'] = np.load(os.path.join('warning_snippets', 'ingame_ct_win_icon_right.npy'))
    icon_dict['ingame_t_win_icon'] = np.load(os.path.join('warning_snippets', 'ingame_t_win_icon.npy'))
    icon_dict['ingame_t_win_icon_left'] = np.load(os.path.join('warning_snippets', 'ingame_t_win_icon_left.npy'))
    icon_dict['ingame_t_win_icon_right'] = np.load(os.path.join('warning_snippets', 'ingame_t_win_icon_right.npy'))
    return icon_dict

def ingame_identify_round_winner(icon_dict, batch = 'upper'): #icon_dict is the dict containing all icons
    ingame_left_icon_x_1, ingame_left_icon_y_1, ingame_left_icon_x_2, ingame_left_icon_y_2 = 310, 93, 320, 111
    ingame_right_icon_x_1, ingame_right_icon_y_1, ingame_right_icon_x_2, ingame_right_icon_y_2 = 325, 93, 336, 111
    ingame_icon_x_1, ingame_icon_y_1, ingame_icon_x_2, ingame_icon_y_2 = 310, 92, 336, 112
    
    if batch == 'upper':
        POS_X, POS_Y = CSGO_UPPER_POS_X, CSGO_UPPER_POS_Y
    elif batch == 'lower':
        POS_X, POS_Y = CSGO_LOWER_POS_X, CSGO_LOWER_POS_Y
    
    test_snippet_left = ImageGrab.grab([POS_X[0] + ingame_left_icon_x_1, 
                                        POS_Y[0] + ingame_left_icon_y_1, 
                                        POS_X[0] + ingame_left_icon_x_2, 
                                        POS_Y[0] + ingame_left_icon_y_2])
    
    test_snippet_right = ImageGrab.grab([POS_X[0] + ingame_right_icon_x_1, 
                                         POS_Y[0] + ingame_right_icon_y_1, 
                                         POS_X[0] + ingame_right_icon_x_2, 
                                         POS_Y[0] + ingame_right_icon_y_2])
    
    test_snippet_left = np.array(test_snippet_left)
    test_snippet_right = np.array(test_snippet_right)
    
    if np.all(test_snippet_left == icon_dict['ingame_t_win_icon_left']) and \
        np.all(test_snippet_right == icon_dict['ingame_t_win_icon_right']):
            return "t"
    elif np.all(test_snippet_left == icon_dict['ingame_ct_win_icon_left']) and \
        np.all(test_snippet_right == icon_dict['ingame_ct_win_icon_right']):
            return "ct"

#%%
def identify_error(test_image = None, error_coordinates = None, error_with_numpy_images = None, POS_X = None, POS_Y = None):
    if error_coordinates is None:
        with open(os.path.join('error_numpy_boxes', 'error_coordinates' + '.pkl'), 'rb') as file:
            error_coordinates = pickle.load(file)
    if error_with_numpy_images is None:
        with open(os.path.join('error_numpy_boxes', 'error_with_numpy_images' + '.pkl'), 'rb') as file:
            error_with_numpy_images = pickle.load(file)
    
    if test_image is None:
        test_image = ImageGrab.grab([POS_X, 
                                     POS_Y, 
                                     POS_X + 640, 
                                     POS_Y + 480 + 25])
    
    test_image_array = np.array(test_image)
    
    error_in_test_image = None
    
    for error_name in list(error_coordinates.keys()):
        x1, y1, x2, y2 = error_coordinates[error_name]
        if np.all(test_image_array[y1:y2, x1:x2, :] == error_with_numpy_images[error_name]):
            error_in_test_image = error_name
            break
    
    return error_in_test_image

def identify_error_wrapper(POS_X, POS_Y, error_coordinates = None, error_with_numpy_images = None, error_ok_button = None, return_error_name = False):
    if error_coordinates is None:
        with open(os.path.join('error_numpy_boxes', 'error_coordinates' + '.pkl'), 'rb') as file:
            error_coordinates = pickle.load(file)
    if error_with_numpy_images is None:
        with open(os.path.join('error_numpy_boxes', 'error_with_numpy_images' + '.pkl'), 'rb') as file:
            error_with_numpy_images = pickle.load(file)
    if error_ok_button is None:
        with open(os.path.join('error_numpy_boxes', 'error_ok_button' + '.pkl'), 'rb') as file:
            error_ok_button = pickle.load(file)

    
    test_image = ImageGrab.grab([POS_X, POS_Y, POS_X + 640, POS_Y + 480 + 25])
    
    output = identify_error(test_image = test_image, error_coordinates = error_coordinates, error_with_numpy_images = error_with_numpy_images)
    if output is None:
        if return_error_name:
            return (None, None)
        else:
            return None
    error_button = error_ok_button[output]
    
    print("Updating Log.")
    file = open('logging_error.txt', 'a')
    file.write(time.ctime(time.time()))
    file.write(", ")
    file.write(output)
    file.write("\n")
    file.close()
    if return_error_name:
        return error_button, output
    else:
        return error_button

def identify_and_clear_errors(all_panels = True, error_coordinates = None, error_with_numpy_images = None, error_ok_button = None, POS_X = None, POS_Y = None, return_error_name = False):
    if error_coordinates is None:
        with open(os.path.join('error_numpy_boxes', 'error_coordinates' + '.pkl'), 'rb') as file:
            error_coordinates = pickle.load(file)
    if error_with_numpy_images is None:
        with open(os.path.join('error_numpy_boxes', 'error_with_numpy_images' + '.pkl'), 'rb') as file:
            error_with_numpy_images = pickle.load(file)
    if error_ok_button is None:
        with open(os.path.join('error_numpy_boxes', 'error_ok_button' + '.pkl'), 'rb') as file:
            error_ok_button = pickle.load(file)
    
    if all_panels:
        for i in range(4, -1, -1): #i = 0
            click_only(CSGO_UPPER_POS_X[i] + CSGO_TITLE_BAR_X[i], CSGO_UPPER_POS_Y[i] + CSGO_TITLE_BAR_Y[i], 0.1, 1)
            error_button = identify_error_wrapper(CSGO_UPPER_POS_X[i], CSGO_UPPER_POS_Y[i], 
                                                  error_coordinates = error_coordinates, 
                                                  error_with_numpy_images = error_with_numpy_images, 
                                                  error_ok_button = error_ok_button)
            if error_button is not None:
                click_only(CSGO_UPPER_POS_X[i] + error_button[0], 
                           CSGO_UPPER_POS_Y[i] + error_button[1], 0.2, 5)
            
            click_only(CSGO_LOWER_POS_X[i] + CSGO_TITLE_BAR_X[i], CSGO_LOWER_POS_Y[i] + CSGO_TITLE_BAR_Y[i], 0.1, 1)
            error_button = identify_error_wrapper(CSGO_LOWER_POS_X[i], CSGO_LOWER_POS_Y[i], 
                                                  error_coordinates = error_coordinates, 
                                                  error_with_numpy_images = error_with_numpy_images, 
                                                  error_ok_button = error_ok_button)
            if error_button is not None:
                click_only(CSGO_LOWER_POS_X[i] + error_button[0], 
                           CSGO_LOWER_POS_Y[i] + error_button[1], 0.2, 5)
    else:
        i = CSGO_UPPER_POS_X.index(POS_X)
        #click_only(POS_X + CSGO_TITLE_BAR_X[i], POS_Y + CSGO_TITLE_BAR_Y[i], 0.1, 1)
        if return_error_name:
            error_button, error_name = identify_error_wrapper(POS_X, POS_Y, 
                                                              error_coordinates = error_coordinates, 
                                                              error_with_numpy_images = error_with_numpy_images, 
                                                              error_ok_button = error_ok_button, 
                                                              return_error_name = return_error_name)
            print(error_button)
            if error_button is not None:
                click_only(POS_X + error_button[0], 
                           POS_Y + error_button[1], 0.2, 3)
            return error_name
        else:
            error_button = identify_error_wrapper(POS_X, POS_Y, 
                                                  error_coordinates = error_coordinates, 
                                                  error_with_numpy_images = error_with_numpy_images, 
                                                  error_ok_button = error_ok_button)
            print(error_button)
            if error_button is not None:
                click_only(POS_X + error_button[0], 
                           POS_Y + error_button[1], 0.2, 3)


        
def temp_get_panel_ready_position(all_panels = True, POS_X = None, POS_Y = None):
    if all_panels:
        for i in range(5):
            click_only(CSGO_UPPER_POS_X[i] + CSGO_TITLE_BAR_X[i], CSGO_UPPER_POS_Y[i] + CSGO_TITLE_BAR_Y[i], 0.1, 1)
            press_and_release("esc", 0.2, 4)
            press_and_release("`", 0.2, 1)

            click_only(CSGO_LOWER_POS_X[i] + CSGO_TITLE_BAR_X[i], CSGO_LOWER_POS_Y[i] + CSGO_TITLE_BAR_Y[i], 0.1, 1)
            press_and_release("esc", 0.2, 4)
            press_and_release("`", 0.2, 1)
    else:
        i = CSGO_UPPER_POS_X.index(POS_X)
        click_only(POS_X + CSGO_TITLE_BAR_X[i], POS_Y + CSGO_TITLE_BAR_Y[i], 0.1, 1)
        press_and_release("esc", 0.2, 4)
        press_and_release("`", 0.2, 1)
        

def restart_if_panel_not_responding(clear_untrusted = True):
    not_responding_pids = get_not_responding_csgo_pids()
    number_of_active_panels = get_total_csgo_panels()
    if not_responding_pids != [] or number_of_active_panels != 10:
        print("CLEARING OFF ALL PANELS AND RE STARTING ALL PANELS in 10 seconds.")
        time.sleep(10)
        cleaner()
        accept_args = get_accept_args()
        runfile("main_file.py", accept_args)
        sys.exit(0)
    else:
        print("Number of Active panels: %d"%(int(number_of_active_panels)))
        print("Number of Not Responding panels: %d"%(len(not_responding_pids)))

def cancel_match():
    print("CANCELLING MATCH.")
    upper_batch = [CSGO_UPPER_POS_X, CSGO_UPPER_POS_Y]
    lower_batch = [CSGO_LOWER_POS_X, CSGO_LOWER_POS_Y]
    
    for batch in [lower_batch, upper_batch]: #batch = lower_batch.copy()
        POS_X, POS_Y = batch
        for i in range(5): #i = 0
            click_only(POS_X[i] + CSGO_TITLE_BAR_X[i], 
                       POS_Y[i] + CSGO_TITLE_BAR_Y[i], 0.1)


            ingame_error_check = identify_and_clear_errors(all_panels = False, 
                                                           error_coordinates = error_coordinates, 
                                                           error_with_numpy_images = error_with_numpy_images, 
                                                           error_ok_button = error_ok_button, 
                                                           POS_X = POS_X[i], 
                                                           POS_Y = POS_Y[i])
            press_and_release("F7", 0.2, 2)

            ingame_error_check = identify_and_clear_errors(all_panels = False, 
                                                           error_coordinates = error_coordinates, 
                                                           error_with_numpy_images = error_with_numpy_images, 
                                                           error_ok_button = error_ok_button, 
                                                           POS_X = POS_X[i], 
                                                           POS_Y = POS_Y[i])

            press_and_release("esc", 0.2, 2)

            ingame_error_check = identify_and_clear_errors(all_panels = False, 
                                                           error_coordinates = error_coordinates, 
                                                           error_with_numpy_images = error_with_numpy_images, 
                                                           error_ok_button = error_ok_button, 
                                                           POS_X = POS_X[i], 
                                                           POS_Y = POS_Y[i])
            

            # for pixel in ERROR_OK:#pixel = ERROR_OK[0]
            #     click_only(POS_X[i] + pixel[0], 
            #                POS_Y[i] + pixel[1], 0.1, 4)
            #     time.sleep(0.1)
            # click_only(POS_X[i] + CSGO_UNTRUSTED_CONTINUE_X, 
            #            POS_Y[i] + CSGO_UNTRUSTED_CONTINUE_Y, 0.1, 4)
    time.sleep(30)
    if clear_untrusted:
        clear_untrusted_issue(all_panels = True)
    sys.exit(0)
    # runfile('3_create_lobbies.py')

def write_stats_for_accounts_to_file():
    steamids = get_current_active_account_steamids()
    file_name = ".".join(steamids)
    with open(os.path.join('temp', 'account_log', file_name + '.txt'), 'w') as file:
        with open('active_accounts.txt', 'r') as file2:
            data = file2.read()
        file.write(str(file2))
        file.write("\n\n\n")
        with open("number_of_matches_played.txt", 'r') as file2:
            max_matches_played = str(file2.read())
        file.write(max_matches_played)


def avast_popup_base(test_image = None, checker_image = None, cancel_match_ = False):
    x1, y1, x2, y2 = 465, 210, 498, 239
    if checker_image is None:
        checker_image = np.load(os.path.join("warning_snippets", "avast_popup.npy"))
    
    if test_image is None:
        test_image = ImageGrab.grab([x1, y1, x2, y2])
    
    test_image = np.array(test_image)
    
    return np.all(test_image == checker_image)



def avast_popup(test_image = None, checker_image = None, cancel_match_ = False):
    xe, ye = 1444, 223
    failsafe = False
    if checker_image is None:
        checker_image = np.load(os.path.join("warning_snippets", "avast_popup.npy"))
    while True:
        output = avast_popup_base(test_image = test_image, checker_image = checker_image, cancel_match_ = cancel_match_)
        if output:
            failsafe = True
            hover_only(xe, ye, 0.5, 0.2)
            click_only(None, None, 0.1, 1)
            print("Updating Log.")
            file = open('logging_error.txt', 'a')
            file.write(time.ctime(time.time()))
            file.write(", ")
            file.write("Avast Popup.")
            file.write("\n")
            file.close()
            if cancel_match_:
                cancel_match()
        else:
            break
    return failsafe
'''
def update_account_statistics():
    USERNAME_UPPER, PASSWORD_UPPER, STEAM_ID_UPPER, USERNAME_LOWER, PASSWORD_LOWER, STEAM_ID_LOWER = get_accounts()
    if os.path.isfile(os.path.join('account_statistics')):
        pass

'''


def save_accept_args(accept_args, path = os.path.join("temp", "accept_args.txt")):
    with open(path, 'w') as file:
        file.write(accept_args)
    del file


def get_accept_args(path = os.path.join("temp", "accept_args.txt")):
    with open(path, 'r') as file:
        accept_args = file.read()
    
    return accept_args





def get_rank_snippets(all_panels = True, POS_X = None, POS_Y = None, batch = None):
    pr_rank_x_1, pr_rank_y_1 = 608, 70
    pr_rank_x_2, pr_rank_y_2 = 634, 94

    mm_rank_x_1, mm_rank_y_1 = 605, 102
    mm_rank_x_2, mm_rank_y_2 = 639, 114
    
    pr_count = len(os.listdir('pr_snippets'))
    mm_count = len(os.listdir('mm_snippets'))
    
    if all_panels == True:
        for i in range(5):
            image = ImageGrab.grab([CSGO_UPPER_POS_X[i] + pr_rank_x_1, 
                                    CSGO_UPPER_POS_Y[i] + pr_rank_y_1, 
                                    CSGO_UPPER_POS_X[i] + pr_rank_x_2, 
                                    CSGO_UPPER_POS_Y[i] + pr_rank_y_2])
            image.save(os.path.join('pr_snippets', str(pr_count+1) + '.png'))
            pr_count+=1
            image = ImageGrab.grab([CSGO_LOWER_POS_X[i] + pr_rank_x_1, 
                                    CSGO_LOWER_POS_Y[i] + pr_rank_y_1, 
                                    CSGO_LOWER_POS_X[i] + pr_rank_x_2, 
                                    CSGO_LOWER_POS_Y[i] + pr_rank_y_2])
            image.save(os.path.join('pr_snippets', str(pr_count+1) + '.png'))
            pr_count+=1
            
            image = ImageGrab.grab([CSGO_UPPER_POS_X[i] + mm_rank_x_1, 
                                    CSGO_UPPER_POS_Y[i] + mm_rank_y_1, 
                                    CSGO_UPPER_POS_X[i] + mm_rank_x_2, 
                                    CSGO_UPPER_POS_Y[i] + mm_rank_y_2])
            image.save(os.path.join('mm_snippets', str(mm_count+1) + '.png'))
            mm_count+=1
            image = ImageGrab.grab([CSGO_LOWER_POS_X[i] + mm_rank_x_1, 
                                    CSGO_LOWER_POS_Y[i] + mm_rank_y_1, 
                                    CSGO_LOWER_POS_X[i] + mm_rank_x_2, 
                                    CSGO_LOWER_POS_Y[i] + mm_rank_y_2])
            image.save(os.path.join('mm_snippets', str(mm_count+1) + '.png'))
            mm_count+=1
    else:
        if batch == None:
            image = ImageGrab.grab([POS_X + pr_rank_x_1, 
                                    POS_Y + pr_rank_y_1, 
                                    POS_X + pr_rank_x_2, 
                                    POS_Y + pr_rank_y_2])
            image.save(os.path.join('pr_snippets', str(pr_count+1) + '.png'))
            pr_count+=1

            image = ImageGrab.grab([POS_X + mm_rank_x_1, 
                                    POS_Y + mm_rank_y_1, 
                                    POS_X + mm_rank_x_2, 
                                    POS_Y + mm_rank_y_2])
            image.save(os.path.join('mm_snippets', str(mm_count+1) + '.png'))
            mm_count+=1

        elif batch in ['upper', 'u']:
            for i in range(5):
                image = ImageGrab.grab([CSGO_UPPER_POS_X[i] + pr_rank_x_1, 
                                        CSGO_UPPER_POS_Y[i] + pr_rank_y_1, 
                                        CSGO_UPPER_POS_X[i] + pr_rank_x_2, 
                                        CSGO_UPPER_POS_Y[i] + pr_rank_y_2])
                image.save(os.path.join('pr_snippets', str(pr_count+1) + '.png'))
                pr_count+=1

                image = ImageGrab.grab([CSGO_UPPER_POS_X[i] + mm_rank_x_1, 
                                        CSGO_UPPER_POS_Y[i] + mm_rank_y_1, 
                                        CSGO_UPPER_POS_X[i] + mm_rank_x_2, 
                                        CSGO_UPPER_POS_Y[i] + mm_rank_y_2])
                image.save(os.path.join('mm_snippets', str(mm_count+1) + '.png'))
                mm_count+=1
            
        elif batch in ['lower', 'l']:
            for i in range(5):
                image = ImageGrab.grab([CSGO_LOWER_POS_X[i] + pr_rank_x_1, 
                                        CSGO_LOWER_POS_Y[i] + pr_rank_y_1, 
                                        CSGO_LOWER_POS_X[i] + pr_rank_x_2, 
                                        CSGO_LOWER_POS_Y[i] + pr_rank_y_2])
                image.save(os.path.join('pr_snippets', str(pr_count+1) + '.png'))
                pr_count+=1
                
                image = ImageGrab.grab([CSGO_LOWER_POS_X[i] + mm_rank_x_1, 
                                        CSGO_LOWER_POS_Y[i] + mm_rank_y_1, 
                                        CSGO_LOWER_POS_X[i] + mm_rank_x_2, 
                                        CSGO_LOWER_POS_Y[i] + mm_rank_y_2])
                image.save(os.path.join('mm_snippets', str(mm_count+1) + '.png'))
                mm_count+=1
    print("Snippets Done")
    
    
def right_visible_arrangement(include_play_button = True):
    for i in range(4, -1, -1):
        click_only(CSGO_UPPER_POS_X[i] + CSGO_TITLE_BAR_X[i], CSGO_UPPER_POS_Y[i] + CSGO_TITLE_BAR_Y[i], 0.1)
        if include_play_button:
            click_only(CSGO_UPPER_POS_X[i] + CSGO_PLAY_BUTTON_X, CSGO_UPPER_POS_Y[i] + CSGO_PLAY_BUTTON_Y, 0.1, 4)
        click_only(CSGO_LOWER_POS_X[i] + CSGO_TITLE_BAR_X[i], CSGO_LOWER_POS_Y[i] + CSGO_TITLE_BAR_Y[i], 0.1)
        if include_play_button:
            click_only(CSGO_LOWER_POS_X[i] + CSGO_PLAY_BUTTON_X, CSGO_LOWER_POS_Y[i] + CSGO_PLAY_BUTTON_Y, 0.1, 4)

def left_visible_arrangement(include_play_button = True):
    for i in range(5):
        click_only(CSGO_UPPER_POS_X[i] + CSGO_TITLE_BAR_X[i], CSGO_UPPER_POS_Y[i] + CSGO_TITLE_BAR_Y[i], 0.1)
        if include_play_button:
            click_only(CSGO_UPPER_POS_X[i] + CSGO_PLAY_BUTTON_X, CSGO_UPPER_POS_Y[i] + CSGO_PLAY_BUTTON_Y, 0.1, 4)
        click_only(CSGO_LOWER_POS_X[i] + CSGO_TITLE_BAR_X[i], CSGO_LOWER_POS_Y[i] + CSGO_TITLE_BAR_Y[i], 0.1)
        if include_play_button:
            click_only(CSGO_LOWER_POS_X[i] + CSGO_PLAY_BUTTON_X, CSGO_LOWER_POS_Y[i] + CSGO_PLAY_BUTTON_Y, 0.1, 4)


def cd_check_wrapper(all_panels = True, POS_X = None, POS_Y = None):
    if all_panels:
        for i in range(5):
            cd_result = cd_check(CSGO_UPPER_POS_X[i], CSGO_UPPER_POS_Y[i])
            if cd_result in ["Y", "G"]:
                print("ERROR: Cooldown")
                #say_beep(2, 5)
                return True
            cd_result = cd_check(CSGO_LOWER_POS_X[i], CSGO_LOWER_POS_Y[i])
            if cd_result in ["Y", "G"]:
                print("ERROR: Cooldown")
                #say_beep(2, 5)
                return True
    else:
        cd_result = cd_check(POS_X, POS_Y)
        if cd_result in ["Y", "G"]:
            print("ERROR: Cooldown")
            return True
    return False
    
def add_account_to_vac_error_list(username):
    file = open('vac_error_accounts.txt', 'a')
    file.write(username)
    file.write('\n')
    file.close()
    
    
def check_round_completion(checker_images = None):
    ingame_ct_right_icon_x_1, ingame_ct_right_icon_y_1 = 325, 93
    ingame_ct_right_icon_x_2, ingame_ct_right_icon_y_2 = 336, 111
    
    if checker_images == None:
        ct_win_icon = np.load(os.path.join('warning_snippets', 'ingame_ct_win_icon_right.npy'))
        t_win_icon = np.load(os.path.join('warning_snippets', 'ingame_t_win_icon_right.npy'))
    else:
        ct_win_icon = checker_images[0]
        t_win_icon = checker_images[1]
    
    panel_top_left_xu, panel_top_left_yu = 1280, 54
    panel_top_left_xl, panel_top_left_yl = 1280, 534+54
    
    test_imageu = ImageGrab.grab([panel_top_left_xu + ingame_ct_right_icon_x_1, 
                                 panel_top_left_yu + ingame_ct_right_icon_y_1, 
                                 panel_top_left_xu + ingame_ct_right_icon_x_2, 
                                 panel_top_left_yu + ingame_ct_right_icon_y_2]).convert("RGB")
    
    test_imagel = ImageGrab.grab([panel_top_left_xl + ingame_ct_right_icon_x_1, 
                                 panel_top_left_yl + ingame_ct_right_icon_y_1, 
                                 panel_top_left_xl + ingame_ct_right_icon_x_2, 
                                 panel_top_left_yl + ingame_ct_right_icon_y_2]).convert("RGB")
    
    
    test_image_arrayu = np.array(test_imageu)
    test_image_arrayl = np.array(test_imagel)
    if np.all(test_image_arrayu == ct_win_icon) or np.all(test_image_arrayu == t_win_icon) or \
        np.all(test_image_arrayl == ct_win_icon) or np.all(test_image_arrayl == t_win_icon):
        return True
    else:
        return False

def check_round_completion_wrapper(checker_images = None):
    if checker_images == None:
        ct_win_icon = np.load(os.path.join('warning_snippets', 'ingame_ct_win_icon_right.npy'))
        t_win_icon = np.load(os.path.join('warning_snippets', 'ingame_t_win_icon_right.npy'))
    else:
        ct_win_icon = checker_images[0]
        t_win_icon = checker_images[1]
    
    max_time = 30
    while True:
        t1 = time.time()
        output = check_round_completion(checker_images = [ct_win_icon, t_win_icon])
        if output:
            return True
        t2 = time.time()
        max_time -= (t2-t1)
        if max_time < 1:
            return False
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    