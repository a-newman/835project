from enum import Enum 

class DataSet: 
    """ 
    Multiple gesture sets with labels.
    """
    def __init__(self, name, filepath): 
        self.gestures = {} # maps gesture names to gsets
        self.name = name
        self.filepath = filepath

    def make_gesture_class(self, gesture_name): 
        if gesture_name in self.gestures: 
            return
        else: 
            self.gestures[gesture_name] = GestureSet(label=gesture_name)

    def store_gesture_example(self, gesture_name, sequence): 
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


class Frame:
    """
    A data structure to hold a frame of a gesture - (x,y,z) points
    """
    def __init__(self, frame):
        self.frame = frame

    def data_for(bodypart): 
        return self.frame[bodypart : bodypart + 3]

class BodyParts(Enum): 
    HIP_CENTER = 0
    SPINE = 1
    SHOULDER_CENTER = 2
    HEAD = 3
    SHOULDER_LEFT = 4
    ELBOW_LEFT = 5
    WRIST_LEFT = 6
    HAND_LEFT = 7
    SHOULDER_RIGHT = 8
    ELBOW_RIGHT = 9
    WRIST_RIGHT = 10
    HAND_RIGHT = 11
    HIP_LEFT = 12
    KNEE_LEFT = 13
    ANKLE_LEFT = 14
    FOOT_LEFT = 15
    HIP_RIGHT = 16
    KNEE_RIGHT = 17
    ANKLE_RIGHT = 18
    FOOT_RIGHT = 19