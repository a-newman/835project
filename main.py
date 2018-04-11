import json 
import pickle
import pythonreader
from time import sleep
from data import Gesture, dset_ops
from ui.gameUI import WordGameUI
from recognize import nn_classifier

CLASSIFIERS_BASE_PATH = "recognize/classifiers/"
CONFIG = None
CLASSIFIER = None
DATASET_NAME = None

tmp_testing_gesture = None # buffer a gesture in testing mode here; wait for feedback
					       # on whether we guessed right to write it to the db 

def process_gesture_test(ui_object): 
	#sleep(2)
	seq = pythonreader.get_data()
	tmp_testing_gesture = seq
	pred_gesture = CLASSIFIER.classify(seq)
	ui_object.word = pred_gesture 
	return 

def process_gesture_practice(gesture_name): 
	seq = pythonreader.get_data()
	if CONFIG.save_data: 
		dset_ops.add_gesture_example(DATASET_NAME, gesture_name, seq)
	if CONFIG.mutate_classifier: 
		CLASSIFIER.update(gesture_name, seq)
		CLASSIFIER.save()
	return seq

if __name__ == "__main__": 
	# load the config file 
	with open('config.json', 'r') as infile: 
		CONFIG = json.load(infile)

	DATASET_NAME = CONFIG['dataset']

	wordlist = dset_ops.get_defined_gestures(DATASET_NAME)

	# with open(CLASSIFIERS_BASE_PATH + config['classifier_file']) as infile: 
	# 	CLASSIFIER = pkl.load(infile) # trained classifier 

	# classifier.prep(); # does any required preprocessing

	CLASSIFIER = nn_classifier.NNClassifier(DATASET_NAME)

	backend = {
		'words': wordlist,
		'get_classification': process_gesture_test,
		'record_delay': 2
	}

	# UI 
	game = WordGameUI(backend)
	game.display_logic()