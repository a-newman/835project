import json 
import pkl
import pythonreader
from data import Gesture, dset_ops

CLASSIFIERS_BASE_PATH = "recognize/classifiers/"
CONFIG = None
CLASSIFIER = None
DATASET_NAME = None

tmp_testing_gesture = None # buffer a gesture in testing mode here; wait for feedback
					       # on whether we guessed right to write it to the db 

def process_gesture_test(): 
	seq = pythonreader.get_data()
	tmp_testing_gesture = seq
	pred_gesture = CLASSIFIER.classify(seq)

def process_gesture_practice(gesture_name): 
	seq = pythonreader.get_data()
	if CONFIG.save_data: 
		dset_ops.add_gesture_example(DATASET_NAME, gesture_name, seq)
	if CONFIG.mutate_classifier: 
		CLASSIFIER.update(gesture_name, seq)
		CLASSIFIER.save()

if __name__ == "__main__": 
	# load the config file 
	with open('config.json', 'r') as infile: 
		CONFIG = json.load(infile)

	DATASET_NAME = CONFIG.dataset

	with open(CLASSIFIERS_BASE_PATH + config['classifier_file']) as infile: 
		CLASSIFIER = pkl.load(infile) # trained classifier 

	classifier.prep(); # does any required preprocessing

	# START UP THE UI