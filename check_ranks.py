"""
Script to check rank snippets of MM and PR
Needs the databsae folder path, rank_type and other parameters
INDEPENDENT
"""


from tqdm import tqdm
import pickle
import shutil
import os
import cv2
from PIL import Image, ImageGrab
import numpy as np
import sys

# from rank_update_functions import backup_rank_database
#%% Select rank type [mm or pr]
rank_type = 'mm'

assert rank_type in ['pr', 'mm']

print("Selected Rank Type: %s"%(rank_type))
base_path = os.path.join('images', rank_type + '_ranks')
print("Selected Path: %s"%(base_path))
#%% Backup existing database
# print("Backing up database")
# backup_rank_database(base_path)
print("Loading earlier comparision indexes.")
rank_replace_path = os.path.join('images', 'replace_dict')
try:
    with open(os.path.join(rank_replace_path, rank_type + '_conversion_table.pkl'), 'rb') as file:
        conversion_table = pickle.load(file)
except:
    conversion_table = {}
# try:
#     with open(os.path.join(rank_replace_path, rank_type + '_to_ignore.pkl'), 'rb') as file:
#         to_ignore = pickle.load(file)
# except:
#     to_ignore = []

#%% Getting the list of snippets
print("Getting List of images for %s rank type"%(rank_type))
image_name_list = os.listdir(base_path)
# Removing the numpy_objects folder
try:
    image_name_list.remove('numpy_objects')
except:
    pass
try:
    image_name_list.remove('Thumbs.db')
except:
    pass

print("Found %d images"%(len(image_name_list)))

#%% filtering ranked_images and error_images
print("Filtering useless/invalid images")
image_name_error = []
image_name_ranked = []

for image_name in tqdm(image_name_list): #image_name = image_name_list[0]
    if "unknown" not in image_name:
        image_name_ranked.append(image_name)
    elif not os.path.isfile(os.path.join(base_path, "numpy_objects", image_name.split('.')[0] + ".npy")):
        image_name_error.append(image_name)
    else:
        try:
            image = Image.open(os.path.join(base_path, image_name))
            image_array = np.load(os.path.join(base_path, "numpy_objects", image_name.split('.')[0] + ".npy"))
            if not np.all(np.array(image) == image_array):
                image_name_error.append(image_name)
        except:
            image_name_error.append(image_name)

print("Found %d Ranked Images and %d error images"%(len(image_name_ranked), len(image_name_error)))

for image_name in image_name_error + image_name_ranked:
    image_name_list.remove(image_name)

# del image, image_array

#%% 
print("") #####???? USED??
info_rank_dict = {}
for image_name in tqdm(image_name_ranked): #image_name = image_name_ranked[0]
    rank_name = image_name.split(".")[0].split("_")[0]
    if rank_name not in info_rank_dict.keys():
        info_rank_dict[rank_name] = {"images": []}
    image_array = np.array(Image.open(os.path.join(base_path, image_name)).convert('RGB')) # .convert('LA'))
    info_rank_dict[rank_name]['images'].append(image_array)

# del image_name, image_array, rank_name


#%% loading all images in temporary dict
print("Loading all images into a temporary dictionary. It will be used to filter out similar images.")
info_dict_temp = {}
for image_name in tqdm(image_name_list):
    info_dict_temp[image_name] = np.array(Image.open(os.path.join(base_path, image_name)).convert('RGB')) #.convert('LA'))

# del image_name
print("Images loaded successfully.")

#%% filtering out repeated images
info_dict = {}
similarity_count = 0
for image_name in tqdm(image_name_list): #image_name = image_name_list[1]
    current_image = info_dict_temp[image_name]
    is_similar = False
    for test_image_name in info_dict.keys(): #test_image_name = list(info_dict.keys())[0]
        if np.all(info_dict[test_image_name]['image'] == current_image):
            similarity_count += 1
            is_similar = True
            break
    if is_similar:
        info_dict[test_image_name]['names_of_similar_image'].append(image_name)
    else:
        info_dict[image_name] = {"image": current_image, 
                                 "names_of_similar_image": [], 
                                 "comparision_array": {i:None for i in info_rank_dict.keys()}}
    
print("Found %d Similarities in new images."%(similarity_count))

#%% getting closest rank for each snippet.
print("Getting closest rank match for each snippet.")
for image_name in tqdm(info_dict.keys()): #image_name = list(info_dict.keys())[0]
    for rank in info_rank_dict.keys(): #rank = 'dmg'
        rank_snippets = info_rank_dict[rank]['images']
        comparision_snippets = [np.sum(np.where(rank_snippet == info_dict[image_name]['image'], 0, 1)) for rank_snippet in rank_snippets]
        info_dict[image_name]['comparision_array'][rank] = min(comparision_snippets)

#%%
comparision_array = []

for image_name in info_dict.keys(): #image_name = list(info_dict.keys())[0]
    # info_dict[image_name]['comparision_array'] = info_dict[image_name]['comparision_array']
    comparision_array.append(info_dict[image_name]['comparision_array'][min(info_dict[image_name]['comparision_array'], key = info_dict[image_name]['comparision_array'].get)])
    # display(Image.fromarray(info_dict[image_name]['image']))
    # print(info_dict[image_name]['comparision_array'][min(info_dict[image_name]['comparision_array'], key = info_dict[image_name]['comparision_array'].get)])
    # input()
    info_dict[image_name]['comparision_score'] = info_dict[image_name]['comparision_array'][min(info_dict[image_name]['comparision_array'], key = info_dict[image_name]['comparision_array'].get)]
    info_dict[image_name]['comparision_array'] = min(info_dict[image_name]['comparision_array'], key = info_dict[image_name]['comparision_array'].get)

print("Comparisions done, and image with lease score defined.")

#%%
# for i in sorted(range(len(info_dict.keys())), key = lambda x: comparision_array[x]):
#     image_name = list(info_dict.keys())[i]
#     display(Image.fromarray(info_dict[image_name]['image']))
#     print(comparision_array[i])
#     input()


# to_ignore = [] #TODO
# conversion_table = {} #TODO
print("Showingg high score snippets.")
print("Type: \n0 -> to ignore the snippet.\n1 -> to select the expected rank of snippet.\nOtherwise, enter the rank input.")
for image_name in info_dict.keys(): #image_name = list(info_dict.keys())[0]
    # if image_name in to_ignore or image_name in conversion_table.keys():
    #     print("Skipping %s, already in database."%(image_name))
    #     continue
    print("Index: %d of %d"%(list(info_dict.keys()).index(image_name), len(info_dict.keys())))
    display(Image.fromarray(info_dict[image_name]['image']))
    expected_rank = info_dict[image_name]['comparision_array']
    print("Expected Rank for this snippet: %s"%(expected_rank))
    input_taken = input("Enter the rank for this snippet: ")
    print("\n\n\n\n\n")
    if input_taken in ["0", 0, ""]:
        # to_ignore += [image_name] + info_dict[image_name]['names_of_similar_image']
        continue
    if input_taken in ['1', 1, 'yes', 'Yes', 'YES', 'YEs']:
        accepted_rank = expected_rank
    else:    
        accepted_rank = input_taken
    conversion_table[image_name] = accepted_rank
    for similar_image in info_dict[image_name]['names_of_similar_image']:
        conversion_table[similar_image] = accepted_rank


print("Please press enter 5 times.")
for i in range(5):
    input()

#%%

print("Mention error indexes [Leave blank for No Errors. ")
missing_indexes = list(map(int, input("Please mention the missing and error indexes: ").split()))
for index in missing_indexes:# index = missing_indexes[0]
    print("Index: %d of %d"%(index, len(missing_indexes)))
    image_name = list(info_dict.keys())[index]
    display(Image.fromarray(info_dict[image_name]['image']))
    expected_rank = info_dict[image_name]['comparision_array']
    print("Expected Rank for this snippet: %s"%(expected_rank))
    input_taken = input("Enter the rank for this snippet: ")
    print("\n\n\n\n\n")
    if input_taken in ["0", 0, ""]:
        # to_ignore += [image_name] + info_dict[image_name]['names_of_similar_image']
        try:
            del conversion_table[image_name]
        except:
            pass
        for similar_image in info_dict[image_name]['names_of_similar_image']:
            try:
                del conversion_table[similar_image]
            except:
                pass
        continue
    if input_taken in ['1', 1, 'yes', 'Yes', 'YES', 'YEs']:
        accepted_rank = expected_rank
    else:    
        accepted_rank = input_taken
    conversion_table[image_name] = accepted_rank
    for similar_image in info_dict[image_name]['names_of_similar_image']:
        conversion_table[similar_image] = accepted_rank
    



with open(os.path.join('images', 'replace_dict', rank_type + '_conversion_table.pkl'), 'wb') as file:
    pickle.dump(conversion_table, file)

# with open(os.path.join('images', 'replace_dict', rank_type + '_to_ignore.pkl'), 'wb') as file:
#     pickle.dump(list(sorted(to_ignore)), file)






#%%
# if os.path.isfile(os.path.join('images', 'replace_dict', rank_type + '_replace_dict_interim.pkl')):
#     x = input("Overwrite existing conversion status: ")
#     if x.lower() in ["yes", 'y', "1"]:
#         with open(os.path.join('images', 'replace_dict', rank_type + '_replace_dict_interim.pkl'), 'wb') as file:
#             pickle.dump(conversion_table, file)
#     else:
#         sys.exit(0)
# else:
#     with open(os.path.join('images', 'replace_dict', rank_type + '_replace_dict_interim.pkl'), 'wb') as file:
#         pickle.dump(conversion_table, file)











#%%
# for image_name in sorted(info_dict, key = lambda x: info_dict[x]['comparision_score']):
#     if image_name in to_ignore: continue
#     display(Image.fromarray(info_dict[image_name]['image']))
#     print("Closest comparision: %s"%(info_dict[image_name]['comparision_array']))
#     new_name = input()
#     if new_name == "":
#         new_name = info_dict[image_name]['comparision_array']
#         conversion_table[image_name] = new_name
#     elif new_name == "-1":
#         to_ignore.add(image_name)
#     else:
#         conversion_table[image_name] = new_name


#%%
# #%%
# analysis_ranked = {}
# for rank in list(info_rank_dict.keys()): #rank = 'dmg'
#     if len(info_rank_dict[rank]['images']) == 1:
#         analysis_ranked[rank] = info_rank_dict[rank]
#     else:
#         for i in range(len(info_rank_dict[rank]['images'])): #i = 0
#             current_image = info_rank_dict[rank]['images'][i]
#             for j in range(len(info_rank_dict[rank]['images'])): #j = 1
#                 if i == j:
#                     info_rank_dict[rank]['comparision_array'][i].append(0)
#                 else:
#                     to_check_image = info_rank_dict[rank]['images'][j]
#                     difference_mapping = np.sum(np.where(to_check_image == current_image, 0, 1))
#                     info_rank_dict[rank]['comparision_array'][i].append(difference_mapping)









