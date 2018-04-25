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
from ui_utils import TextRender,CircularArray,Clock ,resize
from button import Button;
import topbar as bars
from sidebar import Sidebar
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
  ###STATES
  SETUP = 0;
  RECORDING = 1;
  FEEDBACK = 2;
  READY = 3;
  WAIT = 4;
  ###modes
  USER = 0;
  TRAINING = 1;
  #### Limits
  READY_COUNTER=2;
  RECONDING_COUNTER=2;
  FEEDBACK_COUNTER = 3;
  WAIT_COUNTER=2;
  

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
    self.state = self.SETUP;
    self.mode = self.TRAINING;
    self.backend = backend;
    self.wordlist = CircularArray(backend['words'])
    self.word = "None"
    self.test_word = self.wordlist.roll()
    self.backend_wait = True;
    ####
    if self.video_display:
      size = self.dispInfo.current_w-self.VIDEO_WINSIZE[0];
    else:
      size = self.dispInfo.current_w-self.DEPTH_WINSIZE[0];
    #self.clock_image = resize((size,size), ou_img="ui/images/_clock.gif");
    
    #####Disp objects
    
    self.clock = Clock(min(size,self.DEPTH_WINSIZE[1]));
    ##########
    self.counter = self.READY_COUNTER;
    self.action = Text(self.screen,w=100, h=50,pos=(485,0),text=self.test_word,color=THECOLORS['white']);
    self.count = Text(self.screen,w=100, h=100,pos=(485,55),text=str(self.counter),color=THECOLORS['white']);

    ####general state display paramters
    self.mergin_side = 20;
    self.mergin_top = 20;
    ###top bar
    self.top_bar_size = (self.dispInfo.current_w-2*self.mergin_side,70);
    self.topbar = bars.topBar(self.top_bar_size,pos=(self.mergin_side,self.mergin_side));
    ###side bar
    self.side_bar_w = 100;
    self.side_bar_h = self.dispInfo.current_h-self.mergin_top*2-self.top_bar_size[1];
    self.side_bar_pos = (self.mergin_side,self.top_bar_size[1]+self.mergin_top);
    ###word bar
    w = self.dispInfo.current_w-self.side_bar_w-2*self.mergin_side
    self.word_bar_size = (w,70);
    self.word_bar_pos = (self.mergin_side+self.side_bar_w,self.mergin_side+self.top_bar_size[1])
    self.word_bar = bars.wordBar(self.word_bar_size,self.test_word,pos=self.word_bar_pos)
    ###camera feedback pos
    self.camera_feed_pos = (self.mergin_side+self.side_bar_w,self.word_bar_pos[1]+self.word_bar_size[1]);
    ####SETUP display parameters
    self.train_button_pos = (100,100);
    self.train_button = Button(pos=self.train_button_pos,text="TRAINING");
    #++++++++++
    self.user_button_pos = (100,210);
    self.user_button = Button(pos=self.user_button_pos,text="USER");

    ####READY display parameters
    self.quit_button = Button(text="QUIT");
    #++++++++++
    self.setup_button = Button(text="SETUP");
    #++++++
    self.puase_button = Button(text="PUASE");
    self.sidar_bar = Sidebar(self.side_bar_pos,w=self.side_bar_w,h=self.side_bar_h,buttons=[self.quit_button,self.puase_button,self.setup_button])
    ####RECODRING display parameters 
    ####FEEDBACK parameters

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
    return skltl;
  def collect(self,skltns):
    sf = [];
    for index, sklton in enumerate(skltns):
      sk = self.map_skeleton(sklton)
      if sk.is_empty():
        sf.append(sk);
    if not sf==[]:
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

      self.screen.blit(depth_surface,self.camera_feed_pos)
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
      self.screen.blit(vid_surface,self.camera_feed_pos);
      if self.skeletons is not None and self.draw_skeleton:
        self.draw_skeletons(self.skeletons)
        if self.state==self.RECORDING:
          self.collect(self.skeletons);
      self.disp()
      pygame.display.update()


  def setup_display_handler(self):
    ##display two buttons 
    self.screen.blit(self.train_button.show(),self.train_button.pos);
    self.screen.blit(self.user_button.show(),self.user_button.pos)
  def ready_display_handler(self):
    pass 
  def recording_display_handler(self):
    pass 
  def wait_display_handler(self):
    pass 
  def feedback_display_handler(self):
    pass 
  def disp(self):
    if self.state==self.SETUP:
      self.setup_display_handler()
    elif self.state==self.READY:
      self.ready_display_handler()
    elif self.state==self.RECORDING:
      self.recording_display_handler();
    elif self.state==self.WAIT:
      self.wait_display_handler();
    elif self.state==self.FEEDBACK:
      self.feedback_display_handler()
    else:
      print "illigal state!"


  def loop(self):
    pygame.display.set_caption('Loader than words')
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

    pygame.time.set_timer(RECORDEVENT, 800);
    done = False
    skeleton_counter = 0
    while not done:
      e = pygame.event.wait()
      self.dispInfo = pygame.display.Info()
      if e.type == pygame.QUIT:
        done = True
        break
      elif e.type == RECORDEVENT:
        ##recording
        if self.state == self.RECORDING:
          if self.counter<=0:
            if not self.skeletal_map==[]:
              self.backend_data = deepcopy(self.skeletal_map)
              print ""
              print "number of frames send:", len(self.backend_data)
              print "number of frames recieved:", skeleton_counter;
              print ""
              skeleton_counter=0
              self.skeletal_map = []
              if self.mode==self.USER:
                thread = myThread(self.backend['get_classification'], self);
              if self.mode == TRAINING:
                thread = myThread(self.backend['save_sequence'], self);

              thread.start()
            if self.mode == self.TRAINING:
              self.state = self.READY;
              self.counter=self.READY_COUNTER;
            if self.mode == self.USER:
              self.state = self.WAIT;
              self.state = self.WAIT_COUNTER

          else:
            self.counter-=1;

        ##waiting 
        elif self.state==self.WAIT:
          if not backend_wait:
            self.state = self.FEEDBACK;
            self.counter = self.FEEDBACK_COUNTER;
            self.backend_wait=True;
          elif self.counter<=0:
            self.state = self.FEEDBACK
            self.counter = self.FEEDBACK_COUNTER;
            self.word = "None";
            self.backend_wait = True;
          else:
            self.counter-=1;
        ##feedback state
        elif self.state == self.FEEDBACK:
          if counter<=0:
            self.counter = self.READY_COUNTER
            self.state = self.READY
          else:
            self.counter-=1
        ## state READY->countdown to word 
        elif self.state==self.READY:
          if self.counter<=0:
            if self.mode == self.TRAINING:
              self.state = self.RECORDING;
              self.test_word=self.wordlist.roll();
              self.counter = self.RECORDING_COUNTER;
            if self.mode == self.USER:
              self.state = self.RECORDING
              self.counter = self.RECONDING_COUNTER
          else:
            self.counter-=1;



      elif e.type == KINECTEVENT:
          skeletons = e.skeletons
          ###COLLECTING DATA
          if self.state==self.RECORDING:
            skeleton_counter+=1;
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
      if e.type ==MOUSEBUTTONDOWN:
        if self.state==self.SETUP:
          ##if hovering mode: set the mode to mode that mode 
          ##transition to next READY 
          pass
        if self.state == self.READY:
          ##if hovering SETUP: back to hovering
          ## if hovering PAUSE: pause
          ## if quit then quit: leave the game 
          pass 
        if self.state == self.RECORDING:
          ##if hovering SETUP: back to hovering
          ## if hovering PAUSE: pause
          ## if quit then quit: leave the game 
          pass 
        if self.state == self.WAIT:
          ##if hovering SETUP: back to hovering
          ## if hovering PAUSE: pause
          ## if quit then quit: leave the game 
          pass 
        if self.state == self.FEEDBACK:
          ##if hovering SETUP: back to hovering
          ## if hovering PAUSE: pause
          ## if quit then quit: leave the game e
          pass 
      


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