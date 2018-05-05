import numpy as np 

class DataSet: 
    """ 
    Multiple gesture sets with labels.
    """
    def __init__(self, name, filepath): 
        self.gestures = {} # maps gesture names to gsets
        self.translations = {} # maps gesture names to English translations 
        self.name = name
        self.filepath = filepath

    def make_gesture_class(self, gesture_name, translation): 
        if gesture_name in self.gestures: 
            return
        else: 
            self.gestures[gesture_name] = GestureSet(label=gesture_name)
            self.translations[gesture_name] = translation

    def store_gesture_example(self, gesture_name, sequence): 
        gesture_name = gesture_name[0]
        if gesture_name not in self.gestures: 
            raise RuntimeError("Not a valid gesture")

        self.gestures[gesture_name].sequences.append(sequence)

class GestureSet:
    """
    A set of the same gesture, repeated by different users
    """

    def __init__(self, label, sequences=[]):
        """
        :param sequences: List of Sequences
        :param label: Number associated with gesture
        """
        self.sequences = sequences
        self.label = label


class Sequence:
    """
    A sequence is a single gesture composed of ordered frames
    """

    def __init__(self, frames, timestamp):
        self.frames = frames
        self.timestamp = timestamp

    # def normalize(self): 
    #     # rn, will normalize by translating the whole skeleton so that the avg position of the center hip is 
    #     # in the same place 
    #     #print("normalizing")
    #     hipdata = np.array([f.data_for(BODYPARTS.HIP_CENTER) for f in self.frames])
    #     avgs = np.mean(hipdata, axis=0)
    #     framelen = len(self.frames[0].frame)
    #     #print("framelen", framelen)
    #     whole_frame_mean = np.hstack([avgs for _ in range(int(framelen/3))])
    #     newframes = [Frame(f.frame - whole_frame_mean) for f in self.frames]
    #     seq = Sequence(newframes, self.timestamp)
    #     return seq
    #     # print("newframes", len(newframes))
    #     # print(newframes)
    #     # return newframes

    def normalize(self): 
        mins = [10000, 100000, 10000]
        maxes = [-100000, -100000, -1000000]
        for frame in self.frames: 
            for i in range(0, len(frame.frame), 3): 
                elts = frame.frame[i:i+3]
                mins = np.minimum(mins, elts)
                maxes = np.maximum(maxes, elts)
        # we now have corners of a bounding box for the action. subtract the mins from all coords to get 
        # a corner on 0, 0
        framelen = len(self.frames[0].frame)
        whole_frame_mins = np.hstack([mins for _ in range(int(framelen/3))])
        newframes = [Frame(f.frame - whole_frame_mins) for f in self.frames]
        # now scale to put everything in the unit cube 
        inv_diffs = np.reciprocal(maxes - mins)
        whole_frame_factors = np.hstack([inv_diffs for _ in range(int(framelen/3))])
        newframes = [Frame(np.multiply(whole_frame_factors, f.frame)) for f in newframes]
        return Sequence(newframes, self.timestamp)


class Frame:
    """
    A data structure to hold a frame of a gesture - (x,y,z) points
    """
    def __init__(self, frame):
        self.frame = frame

    def data_for(self, bodypart): 
        return self.frame[bodypart : bodypart + 3]

class BodyParts(): 
    def __init__(self): 
        self.HEAD = 0
        self.SPINE = 1

        self.SHOULDER_CENTER = 2
        self.SHOULDER_LEFT = 3
        self.SHOULDER_RIGHT = 4

        self.ELBOW_LEFT = 5
        self.ELBOW_RIGHT = 6

        self.WRIST_LEFT = 7
        self.WRIST_RIGHT = 8

        self.HAND_LEFT = 9
        self.HAND_RIGHT = 10

        self.HIP_CENTER = 11
        self.HIP_LEFT = 12
        self.HIP_RIGHT = 13

        self.ANKLE_LEFT = 14
        self.ANKLE_RIGHT = 15

        self.FOOT_LEFT = 16
        self.FOOT_RIGHT = 17

        self.KNEE_LEFT = 18
        self.KNEE_RIGHT = 19

BODYPARTS = BodyParts()