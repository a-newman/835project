import json
import os
import pickle
import re
from Gesture import DataSet

BASE_PATH = 'sets/'
INDEX_PATH = BASE_PATH + 'index.json'

def make_dset(name, safe=True): 
    # creates a new empty data set
    # registers it in the index and creates a file for it
    index = _load_index()

    if (name in index) and safe: 
        raise RuntimeError("This name is already being used by another vocabulary set")

    id_ = len(index)
    slug = re.sub('[^\w\s-]', '', name).strip().lower()
    slug = re.sub('[-\s]+', '-', slug)
    filename = slug + '_' + str(id_) + '.pkl'

    index[name] = filename

    file_path = BASE_PATH + filename
    if safe and (os.path.exists(file_path)): 
        raise RuntimeError("you're about to overrwrite")
    with open(file_path, 'wb') as outfile: 
        dset = DataSet(name=name, filepath=file_path)
        pickle.dump(dset, outfile)

    # save index
    with open(INDEX_PATH, 'w') as outfile: 
        json.dump(index, outfile)

def _load_dset(name): 
    index = _load_index()

    if name not in index: 
        raise RuntimeError(name + " is not a known dataset")

    file_path = index[name]
    with open(BASE_PATH + file_path, 'rb') as infile: 
        dset = pickle.load(infile)
        return dset

def _save_dset(dset): 
    filepath = dset.filepath 
    with open(filepath, 'wb') as outfile: 
        pickle.dump(dset, outfile)


def make_gesture(dset_name, gesture_name):
    dset=_load_dset(dset_name)
    dset.make_gesture_class(gesture_name)
    _save_dset(dset)
    return dset

def add_gesture_example(dset_name, gesture_name, sequence): 
    dset = _load_dset(dset_name)
    dset.store_gesture_example(gesture_name, sequence)
    _save_dset(dset)
    return dset

def _load_index(): 
    with open(INDEX_PATH, 'r') as infile: 
        index = json.load(infile)
        return index