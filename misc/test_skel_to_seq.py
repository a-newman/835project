from ui.data_utils import * 
import main

skel = Skeletal() 
skel.head = [1, 2, 3]
skel.spine = [1, 2, 3]
skel.shoulder_center= [1, 2, 3]
skel.shoulder_left = [1, 2, 3]
skel.shoulder_right = [1, 2, 3]
skel.elbow_left = [1, 2, 3]
skel.elbow_right = [1, 2, 3]
skel.wrist_left = [1, 2, 3]
skel.wrist_right = [1, 2, 3]
skel.hand_left = [1, 2, 3]
skel.hand_right = [1, 2, 3]
skel.hip_center = [1, 2, 3]
skel.hip_left = [1, 2, 3]
skel.hip_right = [1, 2, 3]
skel.ankle_left = [1, 2, 3]
skel.ankle_right = [1, 2, 3]
skel.foot_left = [1, 2, 3]
skel.foot_right = [1, 2, 3]
skel.knee_left = [1, 2, 3]
skel.knee_right = [1, 2, 3]

skel2 = Skeletal() 
skel.head = [0, 0, 0]
skel.spine = [0, 0, 0]
skel.shoulder_center= [0, 0, 0]
skel.shoulder_left = [0, 0, 0]
skel.shoulder_right = [0, 0, 0]
skel.elbow_left = [0, 0, 0]
skel.elbow_right = [0, 0, 0]
skel.wrist_left = [0, 0, 0]
skel.wrist_right = [0, 0, 0]
skel.hand_left = [0, 0, 0]
skel.hand_right = [0, 0, 0]
skel.hip_center = [0, 0, 0]
skel.hip_left = [0, 0, 0]
skel.hip_right = [0, 0, 0]
skel.ankle_left = [0, 0, 0]
skel.ankle_right = [0, 0, 0]
skel.foot_left = [0, 0, 0]
skel.foot_right = [0, 0, 0]
skel.knee_left = [0, 0, 0]
skel.knee_right = [0, 0, 0]

sf = ScanFrame([skel, skel2])

main._sf_to_sequence([sf])
