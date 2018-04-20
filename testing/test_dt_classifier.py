from recognize.dt_classifier import DTClassifier 
from data import dset_ops

dtc = DTClassifier("Practice")

print("prepping")
dtc.prep()

print("training")
dtc.train()

# grab a seq from the dset and try to classify it 
ds = dset_ops._load_dset("Practice")
for label, g in ds.gestures.items(): 
    print("label", label)
    seq = g.sequences[0] 
    break 

print(dtc.classify(seq))
