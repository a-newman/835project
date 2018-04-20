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
from copy import deepcopy
import time
import ctypes
from ui_utils import TextRender,CircularArray
import threading

import pykinect
from pykinect import nui
from pykinect.nui import JointId

import pygame
from pygame.color import THECOLORS
from pygame.locals import *
class Text:
  def __init__(self, parent, w=100, h=50, pos=(0,0), text = "None",color = THECOLORS['black']):
    self.parent = parent;
    self.pos = pos;
    self.w = w;
    self.h = w;
    self.font_color = color;
    self.text = text
    self.font_size = self.w/len(text) - 10
    font = pygame.font.Font(None, self.font_size);
    txt_ob = font.render(self.text, True, self.font_color)
    self.surf = pygame.Surface((w,h));
  def show(self):
    self.parent.blit(self.surf,self.pos);

    





KINECTEVENT = pygame.USEREVENT
RECORDEVENT = pygame.USEREVENT+1

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







class PykinectInt:
  DEPTH_WINSIZE = 320,240
  VIDEO_WINSIZE = 640,480
  ###states
  IDLE = 0;
  RECORDING = 1; 
  FEEDBACK = 2;
  WAIT = 3;
  ###modes
  USER = 0;
  TRAINING = 1;
  ####
  COUNTER = 4

  def __init__(self,screen,backend = {}):
    self.screen = screen;
    self.screen_lock = thread.allocate()
    self.draw_skeleton = True
    self.video_display = False
    self.dispInfo = pygame.display.Info()
    self.skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image
    self.skeletons = None
    self.DEPTH_WINSIZE = 320,240
    self.VIDEO_WINSIZE = 640,480
    self.skeletal_map = []
    self.state = self.IDLE;
    self.mode = self.TRAINING;
    self.backend = backend;
    self.wordlist = CircularArray(backend['words'])
    self.word = "None"
    self.test_word = self.wordlist.roll()
    self.backend_wait = True;
    
    #####Disp object
    self.counter = self.COUNTER;
    self.action = Text(self.screen,w=100, h=50,pos=(485,0),text=self.test_word,color=THECOLORS['white']);
    self.count = Text(self.screen,w=100, h=100,pos=(485,55),text=str(self.counter),color=THECOLORS['white']);

  def surface_to_array(self,surface):
    buffer_interface = surface.get_buffer()
    address = ctypes.c_void_p()
    size = Py_ssize_t()
    _PyObject_AsWriteBuffer(buffer_interface,
                          ctypes.byref(address), ctypes.byref(size))
    bytes = (ctypes.c_byte * size.value).from_address(address.value)
    bytes.object = buffer_interface
    return bytes
  def pos_to_array(self,joint):
    #print "joint", joint
    return [joint.x,joint.y,joint.z]

  def map_skeleton(self,skeleton):
    skltl = Skeletal();
    skltl.head = self.pos_to_array(skeleton.SkeletonPositions[JointId.Head]);
      
    skltl.should_center = self.pos_to_array(skeleton.SkeletonPositions[JointId.ShoulderCenter]);
    skltl.shoulder_left = self.pos_to_array(skeleton.SkeletonPositions[JointId.ShoulderLeft]);
    skltl.shoulder_right = self.pos_to_array(skeleton.SkeletonPositions[JointId.ShoulderRight]);

    skltl.elbow_left = self.pos_to_array(skeleton.SkeletonPositions[JointId.ElbowLeft]);
    skltl.elbow_right = self.pos_to_array(skeleton.SkeletonPositions[JointId.ElbowRight]);

    skltl.wrist_left = self.pos_to_array(skeleton.SkeletonPositions[JointId.WristLeft]);
    skltl.wrist_right = self.pos_to_array(skeleton.SkeletonPositions[JointId.WristRight]);

    skltl.hand_left =self.pos_to_array(skeleton.SkeletonPositions[JointId.HandLeft]);
    skltl.hand_right =self.pos_to_array(skeleton.SkeletonPositions[JointId.HandRight]);

    skltl.hip_center =self.pos_to_array(skeleton.SkeletonPositions[JointId.HipCenter]);
    skltl.hip_left =self.pos_to_array(skeleton.SkeletonPositions[JointId.HipLeft]);
    skltl.hip_right =self.pos_to_array(skeleton.SkeletonPositions[JointId.HandRight]);

    skltl.ankle_left =self.pos_to_array(skeleton.SkeletonPositions[JointId.AnkleLeft]);
    skltl.ankle_right =self.pos_to_array(skeleton.SkeletonPositions[JointId.AnkleRight]);

    skltl.foot_left =self.pos_to_array(skeleton.SkeletonPositions[JointId.FootLeft]);
    skltl.foot_right =self.pos_to_array(skeleton.SkeletonPositions[JointId.FootRight]);

    skltl.knee_left =self.pos_to_array(skeleton.SkeletonPositions[JointId.KneeLeft]);
    skltl.knee_right =self.pos_to_array(skeleton.SkeletonPositions[JointId.KneeRight]);
    skltl.spine =self.pos_to_array(skeleton.SkeletonPositions[JointId.spine]);
    if not skltl.is_empty():
      print "has data";
    return skltl;
  def collect(self,skltns):
    sf = [];
    for index, sklton in enumerate(skltns):
      sk = self.map_skeleton(sklton)
      if not sk.is_empty():
        sf.append(sk);
    self.skeletal_map.append(ScanFrame(sf));

  def draw_skeleton_data(self,pSkelton, index, positions, width = 4):
    start = pSkelton.SkeletonPositions[positions[0]]
       
    for position in itertools.islice(positions, 1, None):
      next = pSkelton.SkeletonPositions[position.value]
      if self.video_display:
        curstart = self.skeleton_to_depth_image(start, self.VIDEO_WINSIZE[0], self.VIDEO_WINSIZE[1]) 
        curend = self.skeleton_to_depth_image(next, self.VIDEO_WINSIZE[0], self.VIDEO_WINSIZE[1])
        if curstart[0]<self.VIDEO_WINSIZE[0] and curstart[1]<self.VIDEO_WINSIZE[1]:
          if curend[0]<self.VIDEO_WINSIZE[0] and curend[1]<self.VIDEO_WINSIZE[1]:
            pygame.draw.line(self.screen, SKELETON_COLORS[index], curstart, curend, width);
      else:
        curstart = self.skeleton_to_depth_image(start, self.DEPTH_WINSIZE[0], self.DEPTH_WINSIZE[1]) 
        curend = self.skeleton_to_depth_image(next, self.DEPTH_WINSIZE[0], self.DEPTH_WINSIZE[1])
        if curstart[0]<self.DEPTH_WINSIZE[0] and curstart[1]<self.DEPTH_WINSIZE[1]:
          if curend[0]<self.DEPTH_WINSIZE[0] and curend[1]<self.DEPTH_WINSIZE[1]:
            pygame.draw.line(self.screen, SKELETON_COLORS[index], curstart, curend, width);
      start = next
  def draw_skeletons(self,skeletons):
    for index, data in enumerate(skeletons):
      # draw the Head
      if self.video_display:
        HeadPos = self.skeleton_to_depth_image(data.SkeletonPositions[JointId.Head], self.VIDEO_WINSIZE[0], self.VIDEO_WINSIZE[1])
      else:
        HeadPos = self.skeleton_to_depth_image(data.SkeletonPositions[JointId.Head], self.DEPTH_WINSIZE[0], self.DEPTH_WINSIZE[1])
      self.draw_skeleton_data(data, index, SPINE, 10)
      pygame.draw.circle(self.screen, SKELETON_COLORS[index], (int(HeadPos[0]), int(HeadPos[1])), 20, 0)
  
      # drawing the limbs
      self.draw_skeleton_data(data, index, LEFT_ARM)
      self.draw_skeleton_data(data, index, RIGHT_ARM)
      self.draw_skeleton_data(data, index, LEFT_LEG)
      self.draw_skeleton_data(data, index, RIGHT_LEG)
  def depth_frame_ready(self,frame):
    if self.video_display:
      return
    #print "Adding depth........"
    depth_surface = pygame.Surface(self.DEPTH_WINSIZE);

    with self.screen_lock:
      address = self.surface_to_array(depth_surface)
      frame.image.copy_bits(address)
      #print "deleting..."
      del address
      if self.skeletons is not None and self.draw_skeleton:
        self.draw_skeletons(self.skeletons)
        if self.state==self.RECORDING:
          self.collect(self.skeletons);

      self.screen.blit(depth_surface,(0,0))
      self.disp()
      pygame.display.update()
      #print "deleted!"


  def video_frame_ready(self,frame):
    #print "video_display: ",self.video_display
    if not self.video_display:
      return
    #print "Adding......."
    vid_surface = pygame.Surface(self.VIDEO_WINSIZE);

    with self.screen_lock:
      address = self.surface_to_array(vid_surface)
      frame.image.copy_bits(address)
      del address
      self.screen.blit(vid_surface);
      if self.skeletons is not None and self.draw_skeleton:
        self.draw_skeletons(self.skeletons)
        if self.state==self.RECORDING:
          self.collect(self.skeletons);
      self.disp()
      pygame.display.update()


  def dispWord(self):
    surf = pygame.Surface((200,200));
    txt_render = TextRender(surf,self.test_word, font_color=THECOLORS['red'], hover_color=THECOLORS['green']).show();
    self.screen.blit(surf,(588,0));
  


  def dispCount(self):
    surf = pygame.Surface((200,200));
    txt_render = TextRender(surf,str(self.counter), font_color=THECOLORS['red'], hover_color=THECOLORS['green']).show();
    self.screen.blit(surf,(588,300));



  def dispProcessing(self):
    pass 
  def dispSelectMenu(self):
    pass 
  def disp(self):
    if self.state == self.RECORDING:
      self.dispWord();
      self.dispCount();
    if self.state == self.WAIT:
      self.dispProcessing();
    if self.state == self.IDLE:
      self.dispSelectMenu()

  def idle(self):
    self.state = self.RECORDING;





  def collecting(self):
    recording = True;
    e = pygame.event.wait();
    if e.type==RECORDEVENT:
      if self.counter<=0:
        self.backend_data = deepcopy(self.skeletal_map)
        self.skeletal_map = []

        thread = myThread(self.backend['save_sequence'], self);

        thread.start()
        self.state = self.WAIT;
        self.backend_wait=True;
        self.counter=self.COUNTER;

      else:
        self.counter-=1;
    elif e.type == KINECTEVENT:
      print "collecting"
      skeletons = e.skeletons
      self.collect(skeletons);
    
  def wait(self):
    if not self.backend_wait:
      if self.mode == self.TRAINING:
        self.state = self.RECORDING;
        self.test_word=self.wordlist.roll();
      if self.mode == self.USER:
        self.state = self.FEEDBACK


  def loop(self):
    pygame.display.set_caption('Python Kinect Demo')
    self.screen.fill(THECOLORS["black"])


    kinect = nui.Runtime()
    kinect.skeleton_engine.enabled = True
    def post_frame(frame):
        try:
          pygame.event.post(pygame.event.Event(KINECTEVENT, skeletons = frame.SkeletonData))
        except:
          pass
    kinect.skeleton_frame_ready += post_frame
    
    kinect.depth_frame_ready += self.depth_frame_ready    
    kinect.video_frame_ready += self.video_frame_ready    
    
    kinect.video_stream.open(nui.ImageStreamType.Video, 2, nui.ImageResolution.Resolution640x480, nui.ImageType.Color)
    kinect.depth_stream.open(nui.ImageStreamType.Depth, 2, nui.ImageResolution.Resolution320x240, nui.ImageType.Depth)

    print('Controls: ')
    print('     d - Switch to depth view')
    print('     v - Switch to video view')
    print('     s - Toggle displaing of the skeleton')
    print('     u - Increase elevation angle')
    print('     j - Decrease elevation angle')

    pygame.time.set_timer(RECORDEVENT, 1000);
    done = False
    while not done:
      e = pygame.event.wait()
      self.dispInfo = pygame.display.Info()
      if e.type == pygame.QUIT:
        done = True
        break
      elif e.type == RECORDEVENT:
        if self.state == self.RECORDING:
          if self.counter<=0:
            self.backend_data = deepcopy(self.skeletal_map)
            print "number of data points: ", self.backend_data
            self.skeletal_map = []

            thread = myThread(self.backend['save_sequence'], self);

            thread.start()
            self.state = self.WAIT;
            self.backend_wait=True;
            self.counter=self.COUNTER;

          else:
            self.counter-=1;

      elif e.type == KINECTEVENT:
          skeletons = e.skeletons
          ###COLLECTING DATA
          if self.state==self.RECORDING:
            self.collect(skeletons);
          if self.draw_skeleton:
            self.draw_skeletons(skeletons)
            pygame.display.update()
      elif e.type == KEYDOWN:
        if e.key == K_ESCAPE:
          done = True
          break
        elif e.key == K_d:
          with self.screen_lock:
            self.video_display = False
        elif e.key == K_v:
          with self.screen_lock:
            self.screen = pygame.display.set_mode(self.VIDEO_WINSIZE,0,16)
            self.video_display = True
        elif e.key == K_s:
          self.draw_skeleton = not self.draw_skeleton
        elif e.key == K_u:
          kinect.camera.elevation_angle = kinect.camera.elevation_angle + 2
        elif e.key == K_j:
          kinect.camera.elevation_angle = kinect.camera.elevation_angle - 2
        elif e.key == K_x:
          kinect.camera.elevation_angle = 2
      if self.state==self.IDLE:
        self.collecting();
      if self.state==self.WAIT:
        self.wait();


class myThread (threading.Thread):
  def __init__(self, funct, obj):
    threading.Thread.__init__(self)
    self.funct = funct
    self.obj = obj;
  def run(self):
    self.funct(self.obj)


def runUI(backend):
  WINSIZE = 800,640;
  screen_lock = thread.allocate()
  screen = pygame.display.set_mode(WINSIZE,0,16)
  mems = PykinectInt(screen, backend = backend);
  mems.loop();


# if __name__ == '__main__':
#   WINSIZE = 800,640;
#   screen_lock = thread.allocate()
#   screen = pygame.display.set_mode(WINSIZE,0,16)
#   mems = PykinectInt(screen, backend = backend);
#   mems.loop();  
