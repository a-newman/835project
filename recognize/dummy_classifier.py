from recognize.classifier import Classifier
from data import dset_ops
import random 

class DummyClassifier(Classifier): 
    def __init__(self, dset_name, k=1, num_frames=30): 
        self.dset_name = dset_name

    def prep(self): 
        """
        Do any pre-processing that needs to happen before it's ready to use
        Will be called on start-up. 
        """
        self._reload()

    def update(self, label, sample): 
        """
        Take in a new sample of someone (either teacher or student) performing the action
        Update/improve the model based on this example
        """
        # just add a seq to the model 
        pass

    def classify(self, sample): #test_sequence=sample, training_gesture_sets=list of gsets 
        """
        Given a sample, run the model on it and returns label of highest-scoring gesture
        """
        if not (self.cached_dset): 
            self._reload()
        options = list(self.cached_dset.gestures.keys())
        #random.shuffle(options)
        return options[0]

    def train(self): 
        """
        Train the model
        """
        # no training required. All computation happens at sample time 
        pass 

    def _reload(self): 
        print("reloading")
        self.cached_dset = dset_ops._load_dset(self.dset_name)