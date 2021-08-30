import pickle, os


#%% Saves the current session's MM batches.
def save_mm_batches(mm_batches, save_path = os.path.join('dynamic', 'mm_batches.pkl')):
    try:
        with open(save_path, 'wb') as file:
            pickle.dump(mm_batches, file)
        return True
    except:
        return False

#%% Loads the current session's MM batches.
def load_mm_batches(load_path = os.path.join('dynamic', 'mm_batches.pkl')):
    try:
        with open(load_path, 'rb') as file:
            mm_batches = pickle.load(file)
            return mm_batches
    except:
        return False

#%% Saves the Index of MM batch in current session/
def save_mm_batches_index(mm_batches_index, save_path = os.path.join('dynamic', 'mm_batches_index.pkl')):
    try:
        with open(save_path, 'wb') as file:
            pickle.dump(mm_batches_index, file)
        return True
    except:
        return False

#%% Loads the Index of MM batch in current session/
def load_mm_batches_index(load_path = os.path.join('dynamic', 'mm_batches_index.pkl')):
    try:
        with open(load_path, 'rb') as file:
            mm_batches_index = pickle.load(file)
            return mm_batches_index
    except:
        return False

#%% Saves the Account datbase of the current Session to be continued later.
def save_old_account_database(account_data, save_path = os.path.join('dynamic', 'account_database.pkl')):
    try:
        with open(save_path, 'wb') as file:
            pickle.dump(account_data, file)
        return True
    except:
        return False


#%% Loads the Account database of the current Session saved to be contined later.
def load_old_account_database(load_path = os.path.join('dynamic', 'account_database.pkl')):
    try:
        with open(load_path, 'rb') as file:
            account_data = pickle.load(file)
            return account_data
    except:
        return False

#%% Saves the current mm_batch.
def save_current_mm_batch(mm_batch, save_path = os.path.join('dynamic', 'mm_batch.pkl')):
    try:
        with open(save_path, 'wb') as file:
            pickle.dump(mm_batch, file)
        return True
    except:
        return False


#%% Loads the current mm_batch.
def load_current_mm_batch(load_path = os.path.join('dynamic', 'mm_batch.pkl')):
    try:
        with open(load_path, 'rb') as file:
            mm_batch = pickle.load(file)
            return mm_batch
    except:
        return False

#%%
#load_winner_index
#%% Saves the current mm_batch.
def save_winner_index(winner_index, save_path = os.path.join('dynamic', 'winner_index.pkl')):
    try:
        with open(save_path, 'wb') as file:
            pickle.dump(winner_index, file)
        return True
    except:
        return False


#%% Loads the current mm_batch.
def load_winner_index(load_path = os.path.join('dynamic', 'winner_index.pkl')):
    try:
        with open(load_path, 'rb') as file:
            winner_index = pickle.load(file)
            return winner_index
    except:
        return False


#%%
def reset_match_verification(path = os.path.join('dynamic', 'ingame_verification.pkl')):
    with open(path, 'wb') as file:
        pickle.dump(False, file)

def verify_match_completion(path = os.path.join('dynamic', 'ingame_verification.pkl')):
    try:
        with open(path, 'rb') as file:
            status = pickle.load(file)
        return status
    except:
        return False

def toggle_match_completion(path = os.path.join('dynamic', 'ingame_verification.pkl')):
    with open(path, 'wb') as file:
        pickle.dump(True, file)

#%%
def reset_main_verification(path = os.path.join('dynamic', 'main_verification.pkl')):
    with open(path, 'wb') as file:
        pickle.dump(False, file)

def verify_main_completion(path = os.path.join('dynamic', 'main_verification.pkl')):
    try:
        with open(path, 'rb') as file:
            status = pickle.load(file)
        return status
    except:
        return False
def toggle_main_completion(path = os.path.join('dynamic', 'main_verification.pkl')):
    with open(path, 'wb') as file:
        pickle.dump(True, file)

#%%