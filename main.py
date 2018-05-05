import json 
import pickle
import pythonreader
import numpy as np
from time import sleep, time
from data import dset_ops
from data.Gesture import GestureSet, Sequence, Frame

from ui import integration2
#from pycallgraph import PyCallGraph
#from pycallgraph.output import GraphvizOutput
from ui import integration
from recognize.nn_classifier import NNClassifier
from recognize.dt_classifier import DTClassifier

tmp_testing_gesture = None # buffer a gesture in testing mode here; wait for feedback
					       # on whether we guessed right to write it to the db 

class MainObj(): 

	def __init__(self): 
		self.CLASSIFIERS_BASE_PATH = "recognize/classifiers/"
		self.CONFIG = None
		self.CLASSIFIER = None
		self.DATASET_NAME = None

		with open('config.json', 'r') as infile: 
			self.CONFIG = json.load(infile)

		self.DATASET_NAME = self.CONFIG['dataset']
		print("DATASET_NAME", self.DATASET_NAME)

		self.wordlist = dset_ops.get_defined_gestures(self.DATASET_NAME)

		self.CLASSIFIER = NNClassifier(self.DATASET_NAME)
		self.CLASSIFIER.prep()
		self.CLASSIFIER.train()

	def process_gesture_test(self, ui_object): 
		#sleep(2)
		seq = self._sf_to_sequence(ui_object.backend_data)
		print "length of the seq: ", len(seq.frames);
		print "length of the data: ", len(ui_object.backend_data)
		if (seq): 
			tmp_testing_gesture = seq
			pred_gesture = self.CLASSIFIER.classify(seq)
			ui_object.word = pred_gesture 
		else: 
			ui_object.word = None
		ui_object.backend_wait = False
		return 

	def process_gesture_train(self, ui_object): 
		data = ui_object.backend_data
		gesture_name = ui_object.test_word
		print "word", gesture_name
		seq = self._sf_to_sequence(data)

		if (seq): 
			print("DATASET NAME at add time", self.DATASET_NAME)
			dset_ops.add_gesture_example(self.DATASET_NAME, gesture_name, seq)
		ui_object.backend_wait = False

	def process_gesture_practice(self, gesture_name): 
		seq = pythonreader.get_data()
		if self.CONFIG.save_data: 
			dset_ops.add_gesture_example(self.DATASET_NAME, gesture_name, seq)
		if self.CONFIG.mutate_classifier: 
			self.CLASSIFIER.update(gesture_name, seq)
			self.CLASSIFIER.save()
		return seq

	def _sf_to_sequence(self, scan_frame_list): 
		timestamp = time() 
		frames = [] 
		for sf in scan_frame_list: 
			if len(sf.skeletons) == 0: 
				continue
			best_skel = self._get_closest_skel(sf.skeletons)
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

	def _get_closest_skel(self, skeletons): 
		# metric = lambda skel: sum([elt**2 for elt in skel.hip_center])**.5 
		# metrics = [metric(skel) for skel in skeletons]
		# idx = np.argmin(metrics)
		# return skeletons[idx]
		return skeletons[0]

def main(): 
	mainobj = MainObj()

	backend = {
		'words': mainobj.wordlist,
		'get_classification': mainobj.process_gesture_test,
		'save_sequence': mainobj.process_gesture_train,
		'record_delay': 2
	}

	# UI

	
	# game = PykinectInt()
	#  WordGameUI(backend_map=backend)
	# game.display_logic()
	integration.runUI(backend)
if __name__ == "__main__":
  #with PyCallGraph(output=GraphvizOutput()): 
  main()
