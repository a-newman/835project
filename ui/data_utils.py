import numpy as np;
class Skeletal:
  '''
  A class that defines a skeleton as a list of joint positins

  parameters
  - head, spine, shoulders, etc: each as a single 3d position.
  methods:
  - is_not_empty: true if not all coordinates are zero.
  '''
  def __init__(self,data = 0):
    self.head = []
    self.spine = [] 
    
    self.should_center = [];
    self.shoulder_left = [];
    self.shoulder_right = [];

    self.elbow_left = [];
    self.elbow_right = [];

    self.wrist_left = [];
    self.wrist_right = [];

    self.hand_left = [];
    self.hand_right = [];

    self.hip_center = [];
    self.hip_left = [];
    self.hip_right = [];

    self.ankle_left = [];
    self.ankle_right = [];

    self.foot_left = [];
    self.foot_right = [];

    self.knee_left = [];
    self.knee_right = [];
  def is_not_empty(self):
    attr = [
    self.head,self.spine,self.should_center,
    self.shoulder_left,self.shoulder_right,
    self.elbow_left,self.elbow_right,self.wrist_left,
    self.wrist_right,self.hand_left,self.hand_right,
    self.hip_center,self.hip_left,self.hip_right,
    self.ankle_left,self.ankle_right,self.foot_left,
    self.foot_right,self.knee_left,self.knee_right
    ]
    total = np.sum(attr)
    return total>0.0


class ScanFrame:
  '''
  A class that defines a frame, list of skeletons detected by the Kinect at once.
  parameters
  - skeletons: The list of skeletal objects
  '''
  def __init__(self, skeletons):
    self.skeletons = skeletons;