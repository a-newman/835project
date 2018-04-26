from data.Gesture import Sequence, GestureSet
import math

# def normalize_frames(gesture_sets, num_frames):
#     """
#     Normalizes the number of Frames in each Sequence in each GestureSet
#     :param gesture_sets: the list of GesturesSets
#     :param num_frames: the number of frames to normalize to
#     :return: a list of GestureSets where all Sequences have the same number of Frames
#     """
#     new_sets = []
#     for gset in gesture_sets: 
#         label = gset.label 
#         sequences = gset.sequences
#         new_sequences = []
#         for seq in sequences: 
#             frames = seq.frames

#             # for now, assume this is positive 
#             new_frames = resize(frames, num_frames)

#             new_seq = Sequence(new_frames, label)
#             new_sequences.append(new_seq)
#         new_gesture = GestureSet(new_sequences, label)
#         new_sets.append(new_gesture)
#     return new_sets 

def resize_seq(frames, n): 
    #print("frames", frames)
    if len(frames) == 0: 
        raise RuntimeError("must provide at least one frame")
    delta = n - len(frames)

    #base case 
    if delta==0: return frames

    # reduce problem 
    interval = math.ceil(float(len(frames))/abs(delta))
    new_frames = []
    subtract_frames = delta < 0
    for i in range(len(frames)): 
        hit_interval = i%interval == interval-1
        if (hit_interval):
            if not subtract_frames: 
                # we need to add frames; add the same frame twice
                new_frames.append(frames[i])
                new_frames.append(frames[i])
        else: 
            new_frames.append(frames[i]) 
    
    # recurse 
    return resize_seq(new_frames, n)