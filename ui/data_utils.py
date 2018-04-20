import numpy as np;
class Skeletal:
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
  def is_empty(self):
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
    if total>0.0:
      print "total";total
      print "data", data
    return total>0.0


class ScanFrame:
  def __init__(self, skeletons):
    self.skeletons = skeletons;