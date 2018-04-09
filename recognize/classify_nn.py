import operator
import math
import numpy as np
import heapq


def classify_nn(test_sequence, training_gesture_sets, k=1):
    """
    Classify test_sequence using nearest neighbors
    :param test_gesture: Sequence to classify
    :param training_gesture_sets: training set of labeled gestures
    :return: a classification label (an integer between 0 and 8)
    """
    # min heap to hold the best k tuples 
    h = []
    heapq.heapify(h)
    test_feat = _get_feat_vec(test_sequence)
    for gset in training_gesture_sets: 
        label = gset.label
        for seq in gset.sequences: 
            train_feat = _get_feat_vec(seq)
            dist = np.linalg.norm(test_feat - train_feat)
            item = (-dist, label)
            # add to heap 
            if len(h) < k: 
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
    #print("maxelt", maxelt)
    return maxelt


def _get_feat_vec(seq): 
    vec = np.hstack([np.array(f.frame) for f in seq.frames])
    return vec