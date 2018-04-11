from recognize.classifier import Classifier
from data import dset_ops
from recognize.normalize_frames import resize_seq
import heapq
import numpy as np

class NNClassifier(Classifier): 
    def __init__(self, dset_name, k=3, num_frames=30): 
        super().__init__()
        self.dset_name = dset_name
        self.k = k
        self.cached_dset = None
        self.num_frames = num_frames

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
        self.cached_dset.store_gesture_example(label, sample)

    def classify(self, sample): #test_sequence=sample, training_gesture_sets=list of gsets 
        """
        Given a sample, run the model on it and returns label of highest-scoring gesture
        """
        if not (self.cached_dset): 
            self._reload()
        h = []
        heapq.heapify(h)
        test_feat = self._get_feat_vec(sample)
        for label, gset in self.cached_dset.gestures.items():
            for seq in gset.sequences: 
                train_feat = self._get_feat_vec(seq)
                print("test_feat", test_feat)
                print("train_feat", train_feat)
                dist = np.linalg.norm(test_feat - train_feat)
                item = (-dist, label)
                # add to heap 
                if len(h) < self.k: 
                    heapq.heappush(h, item)
                else: 
                    heapq.heappushpop(h, item)

        # now we have our size-k min heap; time to tally the votes 
        votes = {}
        for elt in h: 
            vote = elt[1]
            # print("vote", vote)
            votes[vote] = votes.get(vote, 0) + 1
        maxelt = max([(count, vote) for vote, count in votes.items()])[1]
        return maxelt

    def train(): 
        """
        Train the model
        """
        # no training required. All computation happens at sample time 
        pass 

    def save(self, savepath=None): 
        self.cached_dset = None
        super(Classifier, self).save();

    def _get_feat_vec(self, seq): 
        # reduce to the right number of frames 
        frames = resize_seq(seq.frames, self.num_frames)
        vec = np.hstack([np.array(f.frame) for f in frames])
        return vec

    def _reload(self): 
        self.cached_dset = dset_ops._load_dset(self.dset_name)