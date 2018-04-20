from recognize.net_classifier import NetClassifier
from data import dset_ops

nc = NetClassifier("Practice")

print("prepping")
nc.prep()

print("training")
nc.train()

#nc.save(savepath="recognize/classifiers/PracticeNet.pkl")

# grab a seq from the dset and try to classify it 
ds = dset_ops._load_dset("Practice")
for label, g in ds.gestures.items(): 
    print("label", label)
    seq = g.sequences[0] 
    break 

print(nc.classify(seq))

