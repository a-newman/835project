from pythonreader import get_data
from data import dset_ops
from recognize import nn_classifier
from time import sleep
import pickle

DSET = "Practice"
CLASSIFIER_PATH = None
CLASSIFIER = None
GESTURES = ["wave", "run", "yawn"]

if not (dset_ops.exists(DSET)): 
	print("Making dset %s" % DSET)
	dset_ops.make_dset(DSET, False)
else: 
	print("Using dset %s" % DSET)

if (CLASSIFIER_PATH):
	with open(CLASSIFIER_PATH) as infile: 
		CLASSIFIER  = pickle.load(infile)
else: 
	CLASSIFIER = nn_classifier.NNClassifier(DSET)


def countdown(n): 
	for i in range(n): 
		print(n-i, "...")
		sleep(1)
	print("GO!!!!!!!!")

def record(): 
	print("STARTING")
	sleep(2)
	for g in GESTURES: 
		# make the gesture 
		dset_ops.make_gesture(DSET, g)
		print("RECORDING GESTURE: " + g)
		countdown(3)
		sleep(2)
		seq = get_data()
		print([f.frame for f in seq.frames])
		print("LENGTH", len(seq.frames))
		dset_ops.add_gesture_example(DSET, g, seq)
		print("GOOD JOB!")
		sleep(1)

def test(): 
	if not (CLASSIFIER): 
		print("no classifier specified") 
		return
	print("STARTING")
	sleep(2)
	for i in range(5): 
		countdown(3)
		sleep(2)
		seq = get_data()
		pred = CLASSIFIER.classify(seq)
		print("PREDICTION: %s" % pred)
		sleep(3)