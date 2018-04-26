from data import dset_ops 
from load_gestures import load_gestures
import time 

gestures = load_gestures() 

d = dset_ops.make_dset("mp2", safe=False)

for i, elt in enumerate(gestures): 
	d.make_gesture_class(str(i))
	for s in elt.sequences: 
		s.timestamp = time.time()
		d.store_gesture_example(str(i), s)

dset_ops._save_dset(d)