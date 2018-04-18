from data import dset_ops 
from data.Gesture import * 
from recognize.nn_classifier import NNClassifier
from recognize.dt_classifier import DTClassifier
from recognize.dummy_classifier import DummyClassifier
from recognize.net_classifier import NetClassifier
import random

dset_to_test = "Practice"
num_gestures = 1

# for each gesture, we wanna select num_gestures examples of each gesture as a "train" set 
# the rest is a test set 

ds = dset_ops._load_dset(dset_to_test)

# make temp train and test dsets 
dset_ops.make_dset("train", safe=False)
dset_ops.make_dset("test", safe=False)

for label, g in ds.gestures.items(): 
    dset_ops.make_gesture("train", label)
    dset_ops.make_gesture("test", label)

    sequences = g.sequences
    random.shuffle(sequences)
    trainseq = sequences[:num_gestures]
    testseq = sequences[num_gestures:]

    for trainelt in trainseq: 
        dset_ops.add_gesture_example("train", label, trainelt)

    for testelt in testseq: 
        dset_ops.add_gesture_example("test", label, testelt)

classifiers = [] 
classifiers.append(DummyClassifier(dset_to_test))

log = ""
accuracies = {} 
for i, c in enumerate(classifiers): 
    n = 0 
    correct = 0
    log += "Testing classifier %d\n" % i
    c.prep()
    c.train()
    testset = dset_ops._load_dset("test")
    for label, g in testset.gestures.items(): 
        log += "Testing gesture %s\n" % label
        for seq in g.sequences:
            n += 1
            prediction = c.classify(seq)
            log += "Predicted %s\n" % prediction
            if prediction == label: 
                correct += 1 
    acc = float(correct)/n
    accuracies[i] = acc
    log +=  "Accuracy for classifier %d: %f\n\n" % (i, acc)
    print("PRINTING LOG")
    print(log)
    print("ACCURACIES")
    print(accuracies)

# delete temp databases
dset_ops.delete_dset("test")
dset_ops.delete_dset("train")
