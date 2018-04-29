import pygame
##### import
import thread
import itertools
import ctypes
# import pykinect
# from pykinect import nui
# from pykinect.nui import JointId
from pygame.color import THECOLORS
import numpy as np
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
    self.font=pygame.font.Font(None, int(self.font_size))

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
    self.font_size = self.screen.get_width()/5;
    self.mergin =  12
    self.ncolor = font_color;
    self.hover_color = hover_color;
    self.font_color = self.ncolor;
    self.font = pygame.font.Font(None, int(self.font_size));
    self.surf = self.font.render(self.word, True, self.font_color)
  def render(self):
    self.font = pygame.font.Font(None, int(self.font_size));
    self.surf = self.font.render(self.word, True, ColorMap.RED)
    if self.mergin+self.surf.get_width()>self.screen.get_width():
      remove = (self.mergin+self.surf.get_width())/float(self.screen.get_width());
      self.font_size+= (remove-1)*self.screen.get_width();
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

from PIL import Image
from resizeimage import resizeimage

def resize(size,img = 'ui/images/clock.gif',ou_img = 'ui/images/clock.gif'):
  with open(img, 'r+b') as f:
    with Image.open(f) as image:
        cover = resizeimage.resize_cover(image, size)
        cover.save(ou_img, image.format)
  image = pygame.image.load(ou_img);
  return image;


class Clock:
  def __init__(self, size, in_img="ui/images/clock.gif",out_img="ui/images/_clock.gif"):
    self.surf  = pygame.Surface((size,size));
    self.in_img = in_img;
    self.out_img = out_img;
    self.size = size;
    ###
    self.image = self.get_image();
    self.diagnol = self.get_diagnol();
    ##
    self.background_color=(0,0,0)
    self.clock_color = (0,255,0);

    self.font = pygame.font.Font("ui/fonts/font.ttf", int(self.size*.8));
    
  def draw(self,count=0):
    font_surf = self.font.render(str(count), True, self.clock_color)
    self.surf.blit(self.image,(0,0))
    circle = pygame.draw.circle(self.surf, (23,45,86),(self.size/2,self.size/2),self.diagnol/2, (self.diagnol-self.size)/2);
    self.surf.blit(font_surf,((self.size-font_surf.get_width())/2,(self.size-font_surf.get_height())/2))
    return self.surf;
  def get_image(self):
    with open(self.in_img, 'r+b') as f:
      with Image.open(f) as image:
        cover = resizeimage.resize_cover(image, (self.size,self.size))
        cover.save(self.out_img, image.format)
    image = pygame.image.load(self.out_img);
    return image;
  def get_diagnol(self):
    return int(np.ceil(np.sqrt(2)*self.size));
  


















