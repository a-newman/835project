from data import dset_ops 
from data.Gesture import * 
from recognize.nn_classifier import NNClassifier
from recognize.dt_classifier import DTClassifier
from recognize.dummy_classifier import DummyClassifier
#from recognize.net_classifier import NetClassifier
from recognize.mm_classifier import MMClassifier
import random

dset_to_test = "Practice2"
num_gestures = 3

trainname = "train3"
testname = "test3"

# for each gesture, we wanna select num_gestures examples of each gesture as a "train" set 
# the rest is a test set 

def make_dsets(): 
    ds = dset_ops._load_dset(dset_to_test)

    # make temp train and test dsets 
    dset_ops.make_dset(trainname, safe=False)
    dset_ops.make_dset(testname, safe=False)

    for label, g in ds.gestures.items(): 
        train_dset = dset_ops.make_gesture(trainname, label)
        test_dset = dset_ops.make_gesture(testname, label)

        sequences = g.sequences
        random.shuffle(sequences)
        trainseq = sequences[:num_gestures]
        testseq = sequences[num_gestures:]

        for trainelt in trainseq: 
            print("adding example train")
            train_dset.store_gesture_example(label, trainelt)
            #dset_ops.add_gesture_example("train", label, trainelt, save=False)

        for testelt in testseq: 
            print("adding example test")
            test_dset.store_gesture_example(label, testelt)
            #dset_ops.add_gesture_example("test", label, testelt, save=False)

    dset_ops._save_dset(train_dset)
    dset_ops._save_dset(test_dset)


def test(): 
    classifiers = [] 
    classifiers.append(MMClassifier(trainname))

    log = ""
    accuracies = {} 
    for i, c in enumerate(classifiers): 
        n = 0 
        correct = 0
        log += "Testing classifier %d\n" % i
        c.prep()
        print("training") 
        c.train()
        print("evaluating")
        testset = dset_ops._load_dset(testname)
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
        with open('log.txt', 'w') as outfile: 
            outfile.write(log)

# # delete temp databases
# dset_ops.delete_dset("test")
# dset_ops.delete_dset("train")

if __name__ == "__main__": 
    make_dsets()
    test()