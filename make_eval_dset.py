from data.dset_ops import * 
NAME = "eval4"

#delete_dset("eval")
make_dset(NAME)

#gestures = ["run", "wave", "bat", "cook", "surf", "dance", "telephone", "eat", "box", "dab"]

gestures = ["wave", "dab", "telephone", "bat", "yawn"]

for g in gestures: 
    make_gesture(NAME, g)

print("DONE!")