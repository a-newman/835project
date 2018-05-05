import json
import os
import re
from data.Gesture import DataSet, GestureSet, Sequence, Frame

BASE_PATH = 'data/sets/'
INDEX_PATH = BASE_PATH + 'index.json'
ALLOW_DELETE = set(['train', 'test', 'eval'])

def make_dset(name, safe=True): 
    # creates a new empty data set
    # registers it in the index and creates a file for it
    index = _load_index()

    if (name in index) and safe: 
        raise RuntimeError("This name is already being used by another vocabulary set")

    id_ = len(index)
    slug = re.sub('[^\w\s-]', '', name).strip().lower()
    slug = re.sub('[-\s]+', '-', slug)
    filename = slug + '_' + str(id_) + '.json'

    index[name] = filename

    file_path = BASE_PATH + filename
    if safe and (os.path.exists(file_path)): 
        raise RuntimeError("you're about to overrwrite")
    with open(file_path, 'w') as outfile: 
        dset = DataSet(name=name, filepath=file_path)
        json.dump(_json_serialize_dset(dset), outfile)

    _save_index(index)

    return dset

def delete_dset(name): 
    if name not in ALLOW_DELETE: # extra check to make sure you mean it 
        raise RuntimeError("Delete is not enabled for this set.")

    index = _load_index()
    try: 
        name = index.pop(name)
    except KeyError: 
        raise RuntimeError("Dataset does not exist")

    os.remove(BASE_PATH + name);

    _save_index(index)

def refresh_dset(name): 
    if name not in ALLOW_DELETE: 
        raise RuntimeError("Refresh is not enabled for this set")
    dset = _load_dset(name)
    new_gestures = {} 
    for gname, g in dset.gestures.items(): 
        new_gestures[gname] = GestureSet(gname) 
    dset.gestures = new_gestures
    _save_dset(dset)
    

def exists(name): 
    index = _load_index()
    return name in index 

def get_defined_gestures(name): 
    dset = _load_dset(name)
    print(dset)
    print(dset.translations)
    return [(key, val) for key, val in dset.translations.items()]

def _load_dset(name): 
    index = _load_index()

    if name not in index: 
        raise RuntimeError(name + " is not a known dataset")

    file_path = index[name]
    with open(BASE_PATH + file_path, 'r') as infile: 
        dset = json.load(infile)
        return _json_recover_dset(dset)

def _save_dset(dset): 
    filepath = dset.filepath 
    with open(filepath, 'w') as outfile: 
        dset_json = _json_serialize_dset(dset)
        json.dump(dset_json, outfile)


def make_gesture(dset_name, gesture_name, translation):
    dset=_load_dset(dset_name)
    dset.make_gesture_class(gesture_name, translation)
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

def _save_index(index): 
    with open(INDEX_PATH, 'w') as outfile: 
        json.dump(index, outfile)


def _json_recover_dset(j): 
    dset = DataSet(name=j['name'], filepath=j['filepath'])
    dset.translations = j['translations']
    for gname, g in j['gestures'].items(): 
        dset.gestures[gname] = _json_recover_gesture(g)
    return dset

def _json_recover_gesture(j): 
    sequences = [_json_recover_seq(s) for s in j['sequences']]
    return GestureSet(label = j['label'], sequences=sequences)

def _json_recover_seq(j): 
    return Sequence([_json_recover_frame(f) for f in j['frames']], j['timestamp'])

def _json_recover_frame(j): 
    return Frame(j)

def _json_serialize_dset(dset): 
    dd = {'name': dset.name, 'filepath': dset.filepath, 'gestures': {}, 'translations': dset.translations}
    for gname, g in dset.gestures.items(): 
        dd['gestures'][gname] = _json_serialize_gesture(g)
    return dd  

def _json_serialize_gesture(g): 
    gd = {
        'sequences': [_json_serialize_seq(s) for s in g.sequences],
        'label': g.label,
    }
    return gd

def _json_serialize_seq(s): 
    sd = {
        'frames': [_json_serialize_frame(f) for f in s.frames],
        'timestamp': s.timestamp
    }
    return sd

def _json_serialize_frame(f): 
    return f.frame
