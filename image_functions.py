import numpy as np
import cv2
from PIL import Image, ImageGrab
from panel_functions import get_top_left_position_from_panel_name
from loading_functions import load_mm_rank_database, load_pr_rank_database

from capture_functions import get_pr_rank_snippet, get_mm_rank_snippet

#%%
# [Internal Function] Identifies MM Rank of snippet. 
def identify_mm_rank_internal(mm_rank_database, rank_snippet):
    '''
    [Internal Function] Identifies MM Rank of snippet. 
    If found:
        return mm_rank
    else:
        return False # in which case, it'll create a new snippet for review by wrapper.
    '''
    rank_snippet = np.array(rank_snippet)
    for mm_rank in mm_rank_database.keys(): #mm_rank = 'unranked' # mm_rank = 'le''
        for snippet in mm_rank_database[mm_rank]: #snippet = mm_rank_database[mm_rank][0]
            if np.all(snippet == rank_snippet):
                return mm_rank
    return False
    
# Identifies MM Rank of snippet. 
def identify_mm_rank(rank_snippet = None, panel = None, mm_rank_database = None):
    if mm_rank_database == None: mm_rank_database = load_mm_rank_database()
    assert type(rank_snippet) != None or panel != None
    if type(rank_snippet) != None: rank_snippet = np.array(rank_snippet)[:,:,:3]
    if panel != None:
        if type(panel) == str:
            panel_top_left_x, panel_top_left_y = get_top_left_position_from_panel_name(panel)
            rank_snippet = get_mm_rank_snippet(panel_top_left_x, panel_top_left_y)
        elif type(panel) in (list, tuple): rank_snippet = get_mm_rank_snippet(panel[0], panel[1])
    assert type(rank_snippet) != None
    identified_rank = identify_mm_rank_internal(mm_rank_database, rank_snippet)
    if identified_rank != False:
        print(identified_rank)
        return identified_rank
    else:
        unknown_count = get_number_of_saved_snippets_of_rank(rank_type = 'mm', rank_name = 'unknown')
        image = Image.fromarray(rank_snippet)
        image.save(os.path.join('images', 'mm_ranks', 'unknown_' + str(unknown_count + 1) + '.png'))
        np.save(os.path.join('images', 'mm_ranks', 'numpy_objects', 'unknown_' + str(unknown_count + 1) + '.npy'), np.array(image))
    print('unknown_' + str(unknown_count + 1))
    return 'unknown_' + str(unknown_count + 1)

#%%
def identify_pr_rank_internal(pr_rank_database, rank_snippet):
    '''
    [Internal Function] Identifies PR Rank of snippet.
    If found: 
        return pr_rank
    else:
        return False # in which case, it'll create a new snippet for review by wrapper.
    '''
    rank_snippet = np.array(rank_snippet)
    for pr_rank in pr_rank_database.keys(): #pr_rank = list(pr_rank_database.keys())[0]
        for snippet in pr_rank_database[pr_rank]:
            if np.all(snippet == rank_snippet):
                return pr_rank
    return False

# Identifies PR Rank of snippet. 
def identify_pr_rank(rank_snippet = None, panel = None, pr_rank_database = None):
    if pr_rank_database == None: pr_rank_database = load_pr_rank_database()
    assert type(rank_snippet) != None or panel != None
    if type(rank_snippet) != None: rank_snippet = np.array(rank_snippet)[:,:,:3]
    if panel != None:
        if type(panel) == str:
            panel_top_left_x, panel_top_left_y = get_top_left_position_from_panel_name(panel)
            rank_snippet = get_pr_rank_snippet(panel_top_left_x, panel_top_left_y)
        elif type(panel) in (list, tuple): rank_snippet = get_pr_rank_snippet(panel[0], panel[1])
    assert type(rank_snippet) != None
    identified_rank = identify_pr_rank_internal(pr_rank_database, rank_snippet)
    if identified_rank != False:
        print(identified_rank)
        return identified_rank
    else:
        unknown_count = get_number_of_saved_snippets_of_rank(rank_type = 'pr', rank_name = 'unknown')
        image = Image.fromarray(rank_snippet)
        image.save(os.path.join('images', 'pr_ranks', 'unknown_' + str(unknown_count + 1) + '.png'))
        np.save(os.path.join('images', 'pr_ranks', 'numpy_objects', 'unknown_' + str(unknown_count + 1) + '.npy'), np.array(image))
    print('unknown_' + str(unknown_count + 1))
    return 'unknown_' + str(unknown_count + 1)



import os
def get_number_of_saved_snippets_of_rank(rank_type, rank_name):
    list_files = os.listdir(os.path.join('images', rank_type + '_ranks'))
    count = 0
    for file in list_files:
        if rank_name in file:
            count += 1
    return count
