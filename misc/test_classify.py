from recognize.nn_classifier import * 
from data.Gesture import * 
from random import random

s = Sequence([Frame([random()*2 for _ in range(60)]) for _ in range(30)], 0)

c = NNClassifier("Practice")

print(c.classify(s))

