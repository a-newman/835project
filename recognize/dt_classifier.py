import pickle
from recognize.classifier import Classifier
from recognize.normalize_frames import resize_seq
from data import dset_ops

import numpy as np 
from sklearn.tree import DecisionTreeClassifier

class DTClassifier(Classifier): 
    """
    Classifies using a decision tree 
    """
    def __init__(self, dset_name, num_frames=30, test_ratio=.8): 
        super().__init__()
        self.last_savepath = None
        self.dset_name = dset_name
        self.num_frames = num_frames
        self.test_ratio = test_ratio
        self.cached_dset = None

        self.g_id_count = 0
        self.g_ids_to_names = {} 
        self.X = None
        self.Y = None
        self.clf = None

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
        raise NotImplementedError()

    def classify(self, seq): 
        """
        Given a sample, run the model on it and returns label of highest-scoring gesture
        """
        # resize the seq 
        print("seq", seq)
        frames = resize_seq(seq.frames, self.num_frames)
        sample = np.array([np.concatenate(list(map(lambda x: x.frame, frames)))])
        print("sample shape", sample.shape)

        prediction_id = self.clf.predict(sample)[0]
        return self.g_ids_to_names[prediction_id]

    def train(self): 
        """
        Train the model
        """
        self.clf = DecisionTreeClassifier(criterion='gini')
        self.clf.fit(self.X, self.Y)

    def _get_new_gid(self): 
        self.g_id_count += 1
        return self.g_id_count - 1 

    def _reload(self): 
        print("reloading")
        self.cached_dset = dset_ops._load_dset(self.dset_name)

        # Convert the dataset into a form that is usable by this classifier 
        samples, labels = [], []
        self.g_ids_to_names = {}
        self.g_id_count = 0 

        for g_name, g in self.cached_dset.gestures.items(): 
            g_id = self._get_new_gid()
            self.g_ids_to_names[g_id] = g_name 

            for seq in g.sequences: 
                frames = resize_seq(seq.frames, self.num_frames)
                sample = np.concatenate(list(map(lambda x: x.frame, frames))) # a sample is the concatenation of all the frames in a single seq
                samples.append(sample)
                labels.append(int(g_id))

        self.X, self.Y = np.vstack(samples), np.array(labels)
        print("self.X shape", self.X.shape)
        print("self.Y shape", self.Y.shape)