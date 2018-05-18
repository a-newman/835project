from data import dset_ops
import json
import sys

if __name__ == "__main__": 
    args = sys.argv
    if len(args) > 1: 
        # load mubarik's dset
        with open('config.json', 'r') as infile: 
            config = json.load(infile) 

        config['dataset'] = 'test_mubarik'

        with open('config.json', 'w') as outfile: 
                json.dump(config, outfile)


    else: 
        # load the index 
        dset_index = len(dset_ops._load_index())
        NAME = str(dset_index)
        dset_ops.make_dset(NAME, safe=False)

        GESTURES = [
                ("adiga", "you"),
                ("aniga", "me"),
                ("dhamaan", "all"),
                ("tuko", "pray"),
                ("duub", "push across"),
                ("deji", "calm it down"),
                ("qooraanso", "glance"),
                ("tuur", "throw"),
                ("wadhfi", "swing"), 
                ("qoqo", "scratch your stomach")
        ]

        for g in GESTURES: 
            dset_ops.make_gesture(NAME, g[0], g[1])

        # load in the new dset
        with open('config.json', 'r') as infile: 
            config = json.load(infile) 

        config['dataset'] = NAME

        with open('config.json', 'w') as outfile: 
                json.dump(config, outfile)

        print("DONE!")
