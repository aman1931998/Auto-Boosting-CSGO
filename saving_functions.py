import cv2, pickle, secrets
from PIL import Image
import numpy as np, pandas as pd
import os
from datetime import datetime
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from tqdm import tqdm

def prettify(elem):
    """
    Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

#%% Save account xml objects. | used in saving_functions/update_account_data_completed
def save_account_info_xml_objects(username, objects):
    '''
    Saves the XML objects of the username.
    '''
    covered_xml_headers = set()
    header_to_file_name = {"Acccount_Details":"info.xml", 
                           "Account_Trade_Details":"trade_info.xml", 
                           "Account_MM_Rank_Details":"mm_rank_info.xml", 
                           "Account_PR_Rank_Details":"pr_rank_info.xml", 
                           "Account_Cooldown_Details":"cooldown_info.xml", 
                           "Account_Weekly_Details":"weekly_info.xml", 
                           "Account_Match_History_Details":"match_history.xml", 
                           "Account_Error_Details":"error_info.xml", 
                           "Account_Mismatch_Details":"mismatch_info.xml"}
    for obj in objects: #obj = objects[0]
        if obj.tag not in covered_xml_headers:
            covered_xml_headers.add(obj.tag)
        else: return False
    for obj in objects: #obj = objects[1]
        file_io = open(os.path.join('database', 'open_database', username, header_to_file_name[obj.tag]), 'w')
        file_io.write(prettify(obj))
        print(obj.tag)
        file_io.close()


#%%
