import os
import xml.etree.ElementTree as ET
from datetime import datetime

from project_path import steam_path
#%% Get PR Rank History Object. | not used anywhere yet.
def get_pr_rank_history_object(week_number, datetime_object): ###CHECK!#???
    '''
    Returns a PR Rank History node object.
    '''
    assert type(datetime_object) == datetime
    assert type(week_number) == int
    element = ET.Element('Index_%d'%(str(week_number)))
    number = ET.SubElement(element, "Week_Number")
    number.text = str(week_number)
    datetime_ = ET.SubElement(element, "TimeStamp")
    datetime_.text = str(datetime_object)
    return element

#%% Get MM Rank History Objects (Rank and Time) | mm_rank_info.xml/MM_Rank_History and MM_Rank_Time_History
def get_mm_rank_history_objects(mm_rank_update, datetime_object = datetime.now(), mm_rank_history_updated_index = 0):
    '''
    Returns MM_Rank and MM_Rank_time node objects for open database
    '''
    mm_rank_obj = ET.Element('Rank', attrib = {"Index":str(mm_rank_history_updated_index)})
    mm_rank_obj.text = str(mm_rank_update)
    
    datetime_obj = ET.Element('Time', attrib = {"Index":str(mm_rank_history_updated_index)})
    datetime_obj.text = str(datetime_object)
    
    return mm_rank_obj, datetime_obj

#%% Get Cooldown History Objects (Cooldown Type, Time, MatchID) | cooldown_info.xml/Cooldown_Type_History, 
                                                                                  # Cooldown_Time_History, 
                                                                                  # Cooldown_MatchID_History
def get_new_cooldown_history_objects(cooldown_type = "green", cooldown_time = datetime.now(), cooldown_history_updated_index = 0, matchID = "match_"):
    '''
    Returns Cooldown Type and Time nodes for History.
    '''
    cooldown_type_obj = ET.Element('Type', attrib = {"Index":str(cooldown_history_updated_index)})
    cooldown_type_obj.text = str(cooldown_type)
    
    cooldown_time_obj = ET.Element('Time', attrib = {"Index":str(cooldown_history_updated_index)})
    cooldown_time_obj.text = str(cooldown_time)
    
    cooldown_matchID_obj = ET.Element('MatchID', attrib = {"Index":str(cooldown_history_updated_index)})
    cooldown_matchID_obj.text = str(matchID)    

    return cooldown_type_obj, cooldown_time_obj, cooldown_matchID_obj

#%% Gets Match ID XML Object. | match_history.xml/MatchIDs
def get_match_ID_xml_object(match_id, datestamp = None, output = 'w', matchID_updated_count = 0):
    if datestamp == None:
        datestamp = datetime.now()
    if  output in ['w', 'W', 'winner', 'Winner', 'Win', 'win', 'Victory', 1, '1', True]:
        output = 'w'
    elif output in ['l', 'L', 'loser', 'Loser', 'Lose', 'lose', 'Defeat', -1, '-1', False]:
        output = 'l'
    elif output in ['t', 'tie', 'Tie', 'T', '0', 0]:
        output = 't'
    assert type(datestamp) == datetime
    matchID_object = ET.Element('Match', attrib = {"Index":str(matchID_updated_count)})
    matchID_matchID_object = ET.SubElement(matchID_object, 'MatchID')
    matchID_matchID_object.text = str(match_id)
    matchID_datetime_object = ET.SubElement(matchID_object, 'Datestamp')
    matchID_datetime_object.text = str(datestamp)
    matchID_output_object = ET.SubElement(matchID_object, 'Output')
    matchID_output_object.text = str(output)
    return matchID_object

#%% Gets Search_Error XML Object | used while logging match details | mismatch_details/Mismatch History
def get_mm_mismatch_Mismatch_history_xml_object(mismatch_data):
    '''
    OUTPUT: mm_mismatch_data/mismatchID.xml/Mismatch[1.2.3.4....]
    Gets MM Mismatch History XML Object | used while logging mismatch details | 

    mismatch_data: dict of n mismatches
        '1': dict of 2
            "Match_Found_For": "team1" or "team2"
            "Timestamp_Recorded": datetime object        .
        '2':...
        .
        .
        .
    '''
    assert type(mismatch_data) == dict
    log_mismatch_history = ET.Element('History')
    if len(mismatch_data.keys()) == 0:
        log_mismatch_history.text = "No Error"
    else:
        log_mismatch_history_list = []
        for key in mismatch_data.keys(): #key = list(mismatch_data.keys())[0]
            mismatch_history_node_obj = ET.Element('Mismatch', attrib = {"Index":str(key)})
            mismatch_history_node_match_found_for_obj = ET.SubElement(mismatch_history_node_obj, 'Match_Found_For')
            mismatch_history_node_match_found_for_obj.text = str(mismatch_data[key]['Match_Found_For'])
            mismatch_history_node_match_timestamp_recorded_obj = ET.SubElement(mismatch_history_node_obj, 'Timestamp_Recorded')
            mismatch_history_node_match_timestamp_recorded_obj.text = str(mismatch_data[key]['Timestamp_Recorded'])
            log_mismatch_history_list.append(mismatch_history_node_obj)
        log_mismatch_history.extend(log_mismatch_history_list)
    return log_mismatch_history

#%% Gets Error_History_Node Object.  # WIP
def get_error_history_xml_object(error_name, timestamp, error_updated_count):
    if type(timestamp) != datetime:
        timestamp = datetime.now()
    error_obj = ET.Element('Error', attrib = {"Index":str(error_updated_count)})
    error_error_name = ET.SubElement(error_obj, 'Error_Name')
    error_error_name.text = str(error_name)
    error_error_timestamp = ET.SubElement(error_obj, 'Error_Timestamp')
    error_error_timestamp.text = str(timestamp)
    return error_obj

#%% Gets MM_Mismatch_History_Node Object.  # WIP
def get_mm_mismatch_xml_object(mismatchID, timestamp = datetime.now(), mm_mismatch_updated_index = 0):
    if type(timestamp) != datetime:
        timestamp = datetime.now()
    mismatch_history_obj = ET.Element('Mismatch', attrib = {"Index": str(mm_mismatch_updated_index)})
    mismatch_id_obj = ET.SubElement(mismatch_history_obj, 'Mismatch_ID')
    mismatch_id_obj.text = str(mismatchID)
    mismatch_timestamp_obj = ET.SubElement(mismatch_history_obj, 'Timestamp')
    mismatch_timestamp_obj.text = str(timestamp)
    return mismatch_history_obj



#%% Get TimeStamp Object. <was used in logging match details: changed to str()
# def get_timestamp_xml_object(index = None, now = True, year = None, month = None, date = None, hours = None, minutes = None, seconds = None):
#     if now == True or type(now) == datetime:
#         if type(now) == datetime:
#             timestamp = now
#         else:
#             timestamp = datetime.now()
#         year = str(timestamp.year)
#         month = str(timestamp.month)
#         date = str(timestamp.day)
#         hours = str(timestamp.hour)
#         minutes = str(timestamp.minute)
#         seconds = str(timestamp.second)
#     else:
#         assert year != None and month != None and date != None and hours != None and minutes != None and seconds != None
#     if index == None:
#         timestamp_xml_element = ET.Element('TimeStamp')
#     elif type(index) == int or index.isdigit():
#         timestamp_xml_element = ET.Element('TimeStamp', attrib = {"Index": index})
#     timestamp_xml_year = ET.SubElement(timestamp_xml_element, 'Timestamp_Year')
#     timestamp_xml_year.text = year
#     timestamp_xml_month = ET.SubElement(timestamp_xml_element, 'Timestamp_Month')
#     timestamp_xml_month.text = month
#     timestamp_xml_date = ET.SubElement(timestamp_xml_element, 'Timestamp_Date')
#     timestamp_xml_date.text = date
#     timestamp_xml_hours = ET.SubElement(timestamp_xml_element, 'Timestamp_Hours')
#     timestamp_xml_hours.text = hours
#     timestamp_xml_minutes = ET.SubElement(timestamp_xml_element, 'Timestamp_Minutes')
#     timestamp_xml_minutes.text = minutes
#     timestamp_xml_seconds = ET.SubElement(timestamp_xml_element, 'Timestamp_Seconds')
#     timestamp_xml_seconds.text = seconds
        
#     return timestamp_xml_element



















# def get_follow_path_xml_object(path = "", delimiter = ""):
#     '''
#     Gets Follow Path from /<username>/
#     '''
#     if delimiter == "": path = list(path)
#     elif type(path) == list: path = list(map(str, path))
#     else: path = [i.strip() for i in path.split()]
    
#     l = []
#     for index in range(len(path)):
#         e = ET.Element("Match", attrib = {"Index": index + 1})
#         e.text = path[index]
#         l.append(e)
    
#     return l
