from data import Gesture, dset_ops
import time 

def _flatten(L): 
    return [dimension for point in L for dimension in point]

def get_data(): 
    with open('SkeletonBasics-D2D/tmpfifo', 'r') as infile: 
        lines = infile.readlines()

    frames = [] 
    for line in lines: 
        line = line.strip()
        # throw out empty lines
        if len(line) == 0: 
            continue
        # break down by point
        body_points = line.split(",")[:-1]
        if len(body_points) != 20:
            continue
        body_points = [point.strip().split(" ") for point in body_points]
        coords = [float(point) for point in _flatten(body_points)]
        frame = Gesture.Frame(coords)
        frames.append(frame)
    timestamp = time.time() 
    seq = Gesture.Sequence(frames, timestamp)
    return seq