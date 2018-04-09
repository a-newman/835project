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
        try: 
            g_id = self.gesture_names_to_ids[gesture_name]
        except KeyError: 
            raise RuntimeError("Not a valid gesture")

        self.gestures[g_id].sequences.append(sequence)

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

    def __init__(self, frames, label):
        self.frames = frames
        self.label = label


class Frame:
    """
    A data structure to hold a frame of a gesture - (x,y,z) points
    """

    def __init__(self, frame):
        self.frame = frame

    def head(self):
        return self.frame[0:3]

    def neck(self):
        return self.frame[3:6]

    def left_shoulder(self):
        return self.frame[6:9]

    def left_elbow(self):
        return self.frame[9:12]

    def left_hand(self):
        return self.frame[12:15]

    def right_shoulder(self):
        return self.frame[15:18]

    def right_elbow(self):
        return self.frame[18:21]

    def right_hand(self):
        return self.frame[21:24]

    def torso(self):
        return self.frame[24:27]

    def left_hip(self):
        return self.frame[27:30]

    def right_hip(self):
        return self.frame[30:]


# Main Script to load Gestures.MAT into python objects
# Gestures = scipy.io.loadmat('gesture_dataset.mat')
# gestures = Gestures['gestures']
# gesture_sets = [GestureSet(g) for g in gestures[0]]
