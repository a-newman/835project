# PyKinect
# Copyright(c) Microsoft Corporation
# All rights reserved.
# 
# Licensed under the Apache License, Version 2.0 (the License); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0
# 
# THIS CODE IS PROVIDED ON AN  *AS IS* BASIS, WITHOUT WARRANTIES OR CONDITIONS
# OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY
# IMPLIED WARRANTIES OR CONDITIONS OF TITLE, FITNESS FOR A PARTICULAR PURPOSE,
# MERCHANTABLITY OR NON-INFRINGEMENT.
# 
# See the Apache Version 2.0 License for specific language governing
# permissions and limitations under the License.
from data_utils import *
import thread
import itertools
import ctypes
from ui_utils import TextRender

import pykinect
from pykinect import nui
from pykinect.nui import JointId

import pygame
from pygame.color import THECOLORS
from pygame.locals import *
skeletal_map = []

KINECTEVENT = pygame.USEREVENT
RECORDEVENT = pygame+1
DEPTH_WINSIZE = 320,240
VIDEO_WINSIZE = 640,480
pygame.init()

SKELETON_COLORS = [THECOLORS["red"], 
                   THECOLORS["blue"], 
                   THECOLORS["green"], 
                   THECOLORS["orange"], 
                   THECOLORS["purple"], 
                   THECOLORS["yellow"], 
                   THECOLORS["violet"]]

LEFT_ARM = (JointId.ShoulderCenter, 
            JointId.ShoulderLeft, 
            JointId.ElbowLeft, 
            JointId.WristLeft, 
            JointId.HandLeft)
RIGHT_ARM = (JointId.ShoulderCenter, 
             JointId.ShoulderRight, 
             JointId.ElbowRight, 
             JointId.WristRight, 
             JointId.HandRight)
LEFT_LEG = (JointId.HipCenter, 
            JointId.HipLeft, 
            JointId.KneeLeft, 
            JointId.AnkleLeft, 
            JointId.FootLeft)
RIGHT_LEG = (JointId.HipCenter, 
             JointId.HipRight, 
             JointId.KneeRight, 
             JointId.AnkleRight, 
             JointId.FootRight)
SPINE = (JointId.HipCenter, 
         JointId.Spine, 
         JointId.ShoulderCenter, 
         JointId.Head)

skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image

def pos_to_array(joint):
  return [joint.x,joint.y,joint.z]

def map_skeleton(skeleton):
  skltl = Skeletal();
  skltl.head = pos_to_array(skeleton.SkeletonPositions[JointId.Head]);
    
  skltl.should_center = pos_to_array(skeleton.SkeletonPositions[JointId.ShoulderCenter]);
  skltl.shoulder_left = pos_to_array(skeleton.SkeletonPositions[JointId.ShoulderLeft]);
  skltl.shoulder_right = pos_to_array(skeleton.SkeletonPositions[JointId.ShoulderRight]);

  skltl.elbow_left = pos_to_array(skeleton.SkeletonPositions[JointId.ElbowLeft]);
  skltl.elbow_right = pos_to_array(skeleton.SkeletonPositions[JointId.ElbowRight]);

  skltl.wrist_left = pos_to_array(skeleton.SkeletonPositions[JointId.WristLeft]);
  skltl.wrist_right = pos_to_array(skeleton.SkeletonPositions[JointId.WristRight]);

  skltl.hand_left = pos_to_array(skeleton.SkeletonPositions[JointId.HandLeft]);
  skltl.hand_right = pos_to_array(skeleton.SkeletonPositions[JointId.HandRight]);

  skltl.hip_center = pos_to_array(skeleton.SkeletonPositions[JointId.HipCenter]);
  skltl.hip_left = pos_to_array(skeleton.SkeletonPositions[JointId.HipLeft]);
  skltl.hip_right = pos_to_array(skeleton.SkeletonPositions[JointId.HandRight]);

  skltl.ankle_left = pos_to_array(skeleton.SkeletonPositions[JointId.AnkleLeft]);
  skltl.ankle_right = pos_to_array(skeleton.SkeletonPositions[JointId.AnkleRight]);

  skltl.foot_left = pos_to_array(skeleton.SkeletonPositions[JointId.FootLeft]);
  skltl.foot_right = pos_to_array(skeleton.SkeletonPositions[JointId.FootRight]);

  skltl.knee_left = pos_to_array(skeleton.SkeletonPositions[JointId.KneeLeft]);
  skltl.knee_right = pos_to_array(skeleton.SkeletonPositions[JointId.KneeRight]);
  return skltl;

def collect(skeletons):
  sf = [];
  for index, skeleton in enumerate(skeletons):
    sk = map_skeleton(skeleton)
    sf.append(sk);
  skeletal_map.append(ScanFrame(sf));




def draw_skeleton_data(pSkelton, index, positions, width = 4):
    start = pSkelton.SkeletonPositions[positions[0]]
       
    for position in itertools.islice(positions, 1, None):
        next = pSkelton.SkeletonPositions[position.value]
        
        curstart = skeleton_to_depth_image(start, dispInfo.current_w, dispInfo.current_h) 
        curend = skeleton_to_depth_image(next, dispInfo.current_w, dispInfo.current_h)

        pygame.draw.line(screen, SKELETON_COLORS[index], curstart, curend, width)
        
        start = next

# recipe to get address of surface: http://archives.seul.org/pygame/users/Apr-2008/msg00218.html
if hasattr(ctypes.pythonapi, 'Py_InitModule4'):
   Py_ssize_t = ctypes.c_int
elif hasattr(ctypes.pythonapi, 'Py_InitModule4_64'):
   Py_ssize_t = ctypes.c_int64
else:
   raise TypeError("Cannot determine type of Py_ssize_t")

_PyObject_AsWriteBuffer = ctypes.pythonapi.PyObject_AsWriteBuffer
_PyObject_AsWriteBuffer.restype = ctypes.c_int
_PyObject_AsWriteBuffer.argtypes = [ctypes.py_object,
                                  ctypes.POINTER(ctypes.c_void_p),
                                  ctypes.POINTER(Py_ssize_t)]

def surface_to_array(surface):
   buffer_interface = surface.get_buffer()
   address = ctypes.c_void_p()
   size = Py_ssize_t()
   _PyObject_AsWriteBuffer(buffer_interface,
                          ctypes.byref(address), ctypes.byref(size))
   bytes = (ctypes.c_byte * size.value).from_address(address.value)
   bytes.object = buffer_interface
   return bytes

def draw_skeletons(skeletons):
    for index, data in enumerate(skeletons):
        # draw the Head
        HeadPos = skeleton_to_depth_image(data.SkeletonPositions[JointId.Head], dispInfo.current_w, dispInfo.current_h) 
        draw_skeleton_data(data, index, SPINE, 10)
        pygame.draw.circle(screen, SKELETON_COLORS[index], (int(HeadPos[0]), int(HeadPos[1])), 20, 0)
    
        # drawing the limbs
        draw_skeleton_data(data, index, LEFT_ARM)
        draw_skeleton_data(data, index, RIGHT_ARM)
        draw_skeleton_data(data, index, LEFT_LEG)
        draw_skeleton_data(data, index, RIGHT_LEG)


def depth_frame_ready(frame):
    if video_display:
        return

    with screen_lock:
        address = surface_to_array(screen)
        frame.image.copy_bits(address)
        del address
        if skeletons is not None and draw_skeleton:
            draw_skeletons(skeletons)
        pygame.display.update()    

def video_frame_ready(frame):
    if not video_display:
        return

    with screen_lock:
        address = surface_to_array(screen)
        frame.image.copy_bits(address)
        del address
        if skeletons is not None and draw_skeleton:
            draw_skeletons(skeletons)
        pygame.display.update()

if __name__ == '__main__':
    full_screen = False
    draw_skeleton = True
    video_display = False

    screen_lock = thread.allocate()

    screen = pygame.display.set_mode(DEPTH_WINSIZE,0,16)    
    pygame.display.set_caption('Python Kinect Demo')
    skeletons = None
    screen.fill(THECOLORS["black"])

    kinect = nui.Runtime()
    kinect.skeleton_engine.enabled = True
    def post_frame(frame):
        try:
            pygame.event.post(pygame.event.Event(KINECTEVENT, skeletons = frame.SkeletonData))
        except:
            # event queue full
            pass

    kinect.skeleton_frame_ready += post_frame
    
    kinect.depth_frame_ready += depth_frame_ready    
    kinect.video_frame_ready += video_frame_ready    
    
    kinect.video_stream.open(nui.ImageStreamType.Video, 2, nui.ImageResolution.Resolution640x480, nui.ImageType.Color)
    kinect.depth_stream.open(nui.ImageStreamType.Depth, 2, nui.ImageResolution.Resolution320x240, nui.ImageType.Depth)

    print('Controls: ')
    print('     d - Switch to depth view')
    print('     v - Switch to video view')
    print('     s - Toggle displaing of the skeleton')
    print('     u - Increase elevation angle')
    print('     j - Decrease elevation angle')

    # main game loop
    done = False
    rcount = 3;
    pcount = 3;
    record = False;
    prep = True;
    pygame.time.set_timer(RECORDEVENT, 1000);
    while not done:
        e = pygame.event.wait()
        dispInfo = pygame.display.Info()
        if e.type == pygame.QUIT:
            done = True
            break
        elif e.type = RECORDEVENT:
          if record:
            rcount-=1;
            if rcount==0:
              rcount=3;
              prep = True

          elif prep:
            pcount-=1
            
            if pcount==0:
              record = True;
              prep = False;
              pcount = 3;

        elif e.type == KINECTEVENT:
            skeletons = e.skeletons
            if record:
              collect(skeletons);
            else:
              skeletal_map = [];
            if ready:
              backend_funct(self,skeletal_map);
              record = False;
              ready = False;
            if draw_skeleton:
                draw_skeletons(skeletons)
                pygame.display.update()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                done = True
                break
            elif e.key == K_d:
                with screen_lock:
                    screen = pygame.display.set_mode(DEPTH_WINSIZE,0,16)
                    video_display = False
            elif e.key == K_v:
                with screen_lock:
                    screen = pygame.display.set_mode(VIDEO_WINSIZE,0,32)    
                    video_display = True
            elif e.key == K_s:
                draw_skeleton = not draw_skeleton
            elif e.key == K_u:
                kinect.camera.elevation_angle = kinect.camera.elevation_angle + 2
            elif e.key == K_j:
                kinect.camera.elevation_angle = kinect.camera.elevation_angle - 2
            elif e.key == K_x:
                kinect.camera.elevation_angle = 2
        if record:
          text=TextRender(screen,'recording...');
          text.show();