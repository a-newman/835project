from load_gestures import load_gestures
import dset_ops

DSET_NAME = 'MiniProject 2'
gsets = load_gestures()

dset_ops.make_dset('MiniProject 2', safe=False)

for i, gs in enumerate(gsets): 
	g_name = 'gesture_' + str(i)
	print("making dset with name " + g_name)
	dset_ops.make_gesture(DSET_NAME, g_name)
	# for each example, add it to the gesture 
	for seq in gs.sequences: 
		print("adding a seq")
		dset_ops.add_gesture_example(DSET_NAME, g_name, seq)