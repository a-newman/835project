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

    def normalize(self): 
        # rn, will normalize by translating the whole skeleton so that the avg position of the center hip is 
        # in the same place 
        hipdata = np.array([f.data_for(BODYPARTS.HIP_CENTER) for f in self.frames])
        print("hipdata", hipdata.shape)
        avgs = np.mean(hipdata)
        print("avgs", hipdata.shape)
        whole_frame_mean = "blah"


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