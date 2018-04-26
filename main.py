import json 
import pickle
import pythonreader
import numpy as np
from time import sleep, time
from data import dset_ops
from data.Gesture import GestureSet, Sequence, Frame
from ui import integration
from recognize import nn_classifier

CLASSIFIERS_BASE_PATH = "recognize/classifiers/"
CONFIG = None
CLASSIFIER = None
DATASET_NAME = None

tmp_testing_gesture = None # buffer a gesture in testing mode here; wait for feedback
					       # on whether we guessed right to write it to the db 

def process_gesture_test(ui_object): 
	#sleep(2)
	seq = _sf_to_sequence(ui_object.backend_data)
	if (seq): 
		tmp_testing_gesture = seq
		pred_gesture = CLASSIFIER.classify(seq)
		ui_object.word = pred_gesture 
	else: 
		ui_object.word = None
	ui_object.backend_wait = False
	return 

def process_gesture_train(ui_object): 
	data = ui_object.backend_data
	gesture_name = ui_object.test_word
	seq = _sf_to_sequence(data)
	if (seq): 
		dset_ops.add_gesture_example(DATASET_NAME, gesture_name, seq)
	ui_object.backend_wait = False

def process_gesture_practice(gesture_name): 
	seq = pythonreader.get_data()
	if CONFIG.save_data: 
		dset_ops.add_gesture_example(DATASET_NAME, gesture_name, seq)
	if CONFIG.mutate_classifier: 
		CLASSIFIER.update(gesture_name, seq)
		CLASSIFIER.save()
	return seq

def _sf_to_sequence(scan_frame_list): 
	timestamp = time() 
	frames = [] 
	for sf in scan_frame_list: 
		if len(sf.skeletons) == 0: 
			continue
		best_skel = _get_closest_skel(sf.skeletons)
		frame = [] 
		frame.extend(best_skel.head)
		frame.extend(best_skel.spine)
		frame.extend(best_skel.should_center)
		frame.extend(best_skel.shoulder_left)
		frame.extend(best_skel.shoulder_right)
		frame.extend(best_skel.elbow_left)
		frame.extend(best_skel.elbow_right)
		frame.extend(best_skel.wrist_left)
		frame.extend(best_skel.wrist_right)
		frame.extend(best_skel.hand_left)
		frame.extend(best_skel.hand_right)
		frame.extend(best_skel.hip_center)
		frame.extend(best_skel.hip_left)
		frame.extend(best_skel.hip_right)
		frame.extend(best_skel.ankle_left)
		frame.extend(best_skel.ankle_right)
		frame.extend(best_skel.foot_left)
		frame.extend(best_skel.foot_right)
		frame.extend(best_skel.knee_left)
		frame.extend(best_skel.knee_right)
		if not sum(frame) == 0: 
			frames.append(Frame(frame))
	if len(frames) == 0: 
		print("No valid data was collected")
		return None
	else: 
		return Sequence(frames, timestamp)

def _get_closest_skel(skeletons): 
	# metric = lambda skel: sum([elt**2 for elt in skel.hip_center])**.5 
	# metrics = [metric(skel) for skel in skeletons]
	# idx = np.argmin(metrics)
	# return skeletons[idx]
	return skeletons[0]

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
		'save_sequence': process_gesture_train,
		'record_delay': 2
	}

	# UI

	
	# game = PykinectInt()
	#  WordGameUI(backend_map=backend)
	# game.display_logic()
	integration.runUI(backend)