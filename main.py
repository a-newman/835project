import json 
import pkl

CLASSIFIERS_BASE_PATH = "recognize/classifiers/"

CLASSIFIERS = {
	'dtree': None # should map to a pickle file 
}

def grab_data(): 
	with open('SkeletonBasics-D2D/tmpfifo', 'r') as infile: 
        lines = infile.readlines()
    # TODO: parse, pick frames, put into a proper Gesture or something

if __name__ == "__main__": 
	# load the config file 
	with open('config.json', 'r') as infile: 
		config = json.load(infile)

	with open(CLASSIFIERS_BASE_PATH + config['classifier_file']) as infile: 
		classifier = pkl.load(infile) # trained classifier 

	classifier.prep(); # does any required preprocessing

	# classifier.update(label, sample)

	# classifier.classify(sample)