import os, shutil
from project_path import steam_path
# kill csgo processes
os.system('taskkill /f /im csgo.exe /im steam.exe /im steamwebhelper.exe /im steamservice.exe /im steamerrorreporting.exe')

# # kill steam processes
# os.system('taskkill /f ')

# # kill steamwebhelper processes
# os.system('taskkill /f ')


#kill open cmd process
os.system('taskkill /f /im cmd.exe')

userdata_list = os.listdir(os.path.join(steam_path, "userdata"))

for userdata in userdata_list:
    #os.system('rmdir /s ' + os.path.join("C:\\", "Program Files (x86)", "Steam", "userdata", userdata))
    shutil.rmtree(os.path.join(steam_path, "userdata", userdata))

