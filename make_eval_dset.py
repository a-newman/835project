from data.dset_ops import * 
NAME = "test_mb_2"

#delete_dset("eval")
make_dset(NAME, safe=False)

#gestures = ["run", "wave", "bat", "cook", "surf", "dance", "telephone", "eat", "box", "dab"]

gestures = [
	("adiga", "you"),
	("aniga", "me"),
	("dhamaan", "all"),
	("tuko", "pray"),
	("duub", "push across"),
	("deji", "calm it down"),
	("qooraanso", "glance"),
	("tuur", "throw"),
	("wadhfi", "swing"), 
	("qoqo", "scratch your stomach")
]

for g in gestures: 
    make_gesture(NAME, g[0], g[1])

print("DONE!")
