import pygame
##### import
import thread
import itertools
import ctypes
import pykinect
from pykinect import nui
from pykinect.nui import JointId

class ColorMap:
  BLACK = (0,0,0)
  BLUE =(0,0,255)
  GREEN = (0,255,0)
  RED = (255,0,0)
  WHITE = (255,255,255)
  AQUA = (0,255,255)
  FUCHSIA = (255,0,255)
  YELLOW = (255,255,0)
  GREY = (200,200,200)
  SKY = (0, 51, 102);


class Button:
  def __init__(self,screen, pose=(None,None), dimensions=(None,None),text=None,font_color=None, hoverColor=None,staticColor=None):
    self.screen = screen;
    self.x = pose[0];
    self.y = pose[1];
    self.h = dimensions[0];
    self.w = dimensions[1];
    self.font_size=20;
    self.font = pygame.font.Font(None, 100)
    self.text = text;
    self.font_color = font_color;
    self.hoverColor = hoverColor;
    self.staticColor = staticColor;
    self.color = self.staticColor;
    self.mergin = 10;
  def set_font(self):
    self.font=pygame.font.Font(None, self.font_size)

  def is_hovered(self):
    pos = pygame.mouse.get_pos()
    return self.x-self.w/2 <= pos[0] and self.x + self.w/2 > pos[0] and \
               self.y-self.h <= pos[1] and self.y > pos[1];

  def draw(self):
    surf = self.font.render(self.text, True, self.font_color)
    if surf.get_width()+self.mergin>self.w:
      self.font_size-=2;
      self.set_font();
      self.draw();
    rect = (self.x-self.w/2, self.y-self.h, self.w, self.h)
    x0 = self.x-self.w/2 + (self.w - surf.get_width())/2
    y0 = self.y-self.h + (self.h - surf.get_height())/2
    self.screen.fill(self.color, rect)
    self.screen.blit(surf, (x0, y0))
  def show(self):
    self.color = self.staticColor;
    if self.is_hovered():
      self.color = self.hoverColor;
    self.draw()


def button_test():
  '''
  test button
  '''
  pygame.init()
  BLACK = (0, 0, 0)
  WHITE = (155, 155, 155)
  GREEN = (0, 155, 0)
  BLUE = (123,35,155)
  RED = (255, 0, 0)
  size = (500, 500)
  screen = pygame.display.set_mode(size)
 
  pygame.display.set_caption("My Game")
 
  done = False
 
  clock = pygame.time.Clock()

  button = Button(screen)
  while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    

    button.x = 250;
    button.y = 250;
    button.h = 100;
    button.w = 200;
    button.font_size = 100;
    button.set_font()
    button.text = "setup"
    button.font_color = BLACK;
    button.hoverColor = GREEN
    button.staticColor = BLUE;
     

    screen.fill(WHITE)
    button.show()
 
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
  # Close the window and quit.
  pygame.quit()
#button_test()
class CountDown(Button):
  def __init__(self,screen, second=2):
    Button.__init__(self, screen)
    self.counts = ['go','GO!']+list(range(second));
  def count(self):
    self.text = str(self.counts.pop());
    return self.text
def countDown_test():
  pygame.init()
  size  = (500,500)
  screen = pygame.display.set_mode(size);
  pygame.display.set_caption("My Game");
  clock = pygame.time.Clock()
  pygame.time.set_timer(pygame.USEREVENT, 1000)

  cd = CountDown(screen)
  cd.x = 250;
  cd.y = 250;
  cd.h = 200;
  cd.w = 200;
  cd.font_size= 100;
  cd.font = pygame.font.Font(None, 100)
  cd.font_color = ColorMap.BLACK;
  cd.hoverColor = ColorMap.GREY;
  cd.staticColor = ColorMap.GREY;

  loop = True
  count = None
  while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False;
        if event.type == pygame.USEREVENT:
          count = cd.count()

    screen.fill(ColorMap.WHITE)
    cd.show()
    if count=='go':
      loop = False;
 
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
  pygame.quit()

##countDown_test()

class CircularArray:
  def __init__(self,array):
    self.arr = array;
  def roll(self):
    element = self.arr.pop(0);
    self.arr.append(element);
    return element;
  def randRoll(self):
    import random;
    n = random.randint(0,len(self.arr)-1);
    element = self.arr.pop(n);
    self.append(element);
class TextRender:
  def __init__(self,screen,word, font_color=ColorMap.RED, hover_color=ColorMap.GREEN):
    self.word = word;
    self.screen = screen;
    self.x_0 = self.screen.get_width()/2;
    self.y_0 = self.screen.get_height()/2;
    self.font_size = 100;
    self.mergin =  12
    self.ncolor = font_color;
    self.hover_color = hover_color;
    self.font_color = self.ncolor;
    self.font = pygame.font.Font(None, self.font_size);
    self.surf = self.font.render(self.word, True, self.font_color)
  def render(self):
    self.font = pygame.font.Font(None, self.font_size);
    self.surf = self.font.render(self.word, True, ColorMap.RED)
    if self.mergin+self.surf.get_width()>self.screen.get_width():
      remove = (self.mergin+self.surf.get_width())/float(self.screen.get_width());
      self.font_size+= (remove-1)*self.screen.get_width;
      self.render()
    x_0 = self.x_0-self.surf.get_width()/2;
    y_0 =self.y_0-self.surf.get_height()/2;
    self.screen.blit(self.surf,(x_0,y_0));
  def is_hovered(self):
    pos = pygame.mouse.get_pos();
    x_align = pos[0]>self.x_0 and pos[0]<self.surf.get_width()+self.x_0;
    y_align = pos[1]>self.y_0 and pos[1]<self.surf.get_height()+self.y_0;
    return x_align and y_align;
  def show(self,colorify=True):
    if colorify:
      if self.is_hovered():
        self.font_color=self.hover_color;
      else:
        self.font_color=self.ncolor;
    self.render()
def text_test():
  pygame.init()
  size  = (500,500)
  screen = pygame.display.set_mode(size);
  pygame.display.set_caption("My Game");
  clock = pygame.time.Clock()
  text = TextRender(screen,"word");
  text.x_0 = 250
  text.y_0 = 250
  done = False
  while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()
    

    
    screen.fill(ColorMap.WHITE)
    text.show()
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)
#text_test()
class MovingGroundEffects:
  def __init__(self, screen,image=None,x = -2,y=-2):
    self.image = image;
    self.screen = screen;
    self.x = x;
    self.y = y;
  def flashing_stars(self):
    pass
  def draw(self):
    i_w = self.image.get_width()
    
    if (i_w+self.x)<-1:
      self.x = i_w;
    self.screen.blit(self.image,(self.x,self.y));
  def move(self):
    self.x-=1;
    self.draw()

def scolling_backgrnd(screen,image='ui/images/space.jpg'):
  _image=pygame.image.load(image)
  bckObj = MovingGroundEffects(screen,image=_image)
  bckObj1 = MovingGroundEffects(screen,image=_image,x=_image.get_width())
  return bckObj,bckObj1


class PykinectMembers:
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
  KINECTEVENT = pygame.USEREVENT
  RECORDEVENT = pygame.USEREVENT+1
  DEPTH_WINSIZE = 320,240
  VIDEO_WINSIZE = 640,480
  def __init__(self,screen):
    self.screen_lock = thread.allocate();
    self.screen = []
    self.skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image
    self.kinect = nui.Runtime();
    self.kinect.skeleton_engine.enabled = True;
    self.full_screen = False;
    self.draw_skeleton = True;
    self.video_display = False;
    self.skeletal_map = [];
    self.skeletons = None;
    self.draw_skeleton = True
    # recipe to get address of surface: http://archives.seul.org/pygame/users/Apr-2008/msg00218.html
    if hasattr(ctypes.pythonapi, 'Py_InitModule4'):
       Py_ssize_t = ctypes.c_int
    elif hasattr(ctypes.pythonapi, 'Py_InitModule4_64'):
       Py_ssize_t = ctypes.c_int64
    else:
       raise TypeError("Cannot determine type of Py_ssize_t")

    self._PyObject_AsWriteBuffer = ctypes.pythonapi.PyObject_AsWriteBuffer
    self._PyObject_AsWriteBuffer.restype = ctypes.c_int
    self._PyObject_AsWriteBuffer.argtypes = [ctypes.py_object,
                                      ctypes.POINTER(ctypes.c_void_p),
                                      ctypes.POINTER(Py_ssize_t)]

  def pos_to_array(self,joint):
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
    return skltl;

  def collect(self,skltns):
    sf = [];
    for index, sklton in enumerate(skltns):
      sk = self.map_skeleton(skltn)
      sf.append(sk);
    skeletal_map.append(ScanFrame(sf));

  def draw_skeleton_data(self,pSkelton, index, positions, width = 4):
    start = pSkelton.SkeletonPositions[positions[0]]
       
    for position in itertools.islice(positions, 1, None):
      next = pSkelton.SkeletonPositions[position.value]
      
      curstart = self.skeleton_to_depth_image(start, dispInfo.current_w, dispInfo.current_h) 
      curend = self.skeleton_to_depth_image(next, dispInfo.current_w, dispInfo.current_h)

      pygame.draw.line(self.screen, SKELETON_COLORS[index], curstart, curend, width)
      
      start = next
  def surface_to_array(self,surface):
    buffer_interface = surface.get_buffer()
    address = ctypes.c_void_p()
    size = Py_ssize_t()
    self._PyObject_AsWriteBuffer(buffer_interface,
                        ctypes.byref(address), ctypes.byref(size))
    bytes = (ctypes.c_byte * size.value).from_address(address.value)
    bytes.object = buffer_interface
    return bytes
  def draw_skeletons(self,skeletons):
    for index, data in enumerate(skeletons):
      # draw the Head
      HeadPos = self.skeleton_to_depth_image(data.SkeletonPositions[JointId.Head], dispInfo.current_w, dispInfo.current_h) 
      self.draw_skeleton_data(data, index, SPINE, 10)
      pygame.draw.circle(self.screen, self.SKELETON_COLORS[index], (int(HeadPos[0]), int(HeadPos[1])), 20, 0)
  
      # drawing the limbs
      self.draw_skeleton_data(data, index, self.LEFT_ARM)
      self.draw_skeleton_data(data, index, self.RIGHT_ARM)
      self.draw_skeleton_data(data, index, self.LEFT_LEG)
      self.draw_skeleton_data(data, index, self.RIGHT_LEG)
  def depth_frame_ready(self,frame):
    if video_display:
      return

    with self.screen_lock:
      address = self.surface_to_array(self.screen)
      frame.image.copy_bits(address)
      del address
      if self.skeletons is not None and self.draw_skeleton:
          self.draw_skeletons(skeletons)
      pygame.display.update()    
  def video_frame_ready(self,frame):
    if not self.video_display:
      return

    with self.screen_lock:
      address = self.surface_to_array(self.screen)
      frame.image.copy_bits(address)
      del address
      if skeletons is not None and draw_skeleton:
          self.draw_skeletons(skeletons)
      pygame.display.update()
  def post_frame(self,frame):
    try:
      pygame.event.post(pygame.event.Event(self.KINECTEVENT, skeletons = frame.SkeletonData))
    except:
      # event queue full
      pass
  def run(self):
    self.kinect.skeleton_frame_ready += self.post_frame
    self.kinect.depth_frame_ready += self.depth_frame_ready    
    self.kinect.video_frame_ready += self.video_frame_ready
    self.kinect.video_stream.open(nui.ImageStreamType.Video, 2, nui.ImageResolution.Resolution640x480, nui.ImageType.Color);
    self.kinect.depth_stream.open(nui.ImageStreamType.Depth, 2, nui.ImageResolution.Resolution320x240, nui.ImageType.Depth);
def testPykinect():
  DEPTH_WINSIZE = (800,800)
  screen = pygame.display.set_mode(DEPTH_WINSIZE,0,16)    
  pygame.display.set_caption('Python Kinect Demo')
  skeletons = None;
  screen.fill(THECOLORS["black"]);
  mems = PykinectMembers(screen)
  mems.run();
















