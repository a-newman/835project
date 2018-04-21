import pygame
##### import
import thread
from pygame.color import THECOLORS
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

class TextRender:
  def __init__(self,screen,word, font_color=ColorMap.RED, hover_color=ColorMap.GREEN):
    self.word = word;
    self.screen = screen;
    self.x_0 = self.screen.get_width()/2;
    self.y_0 = self.screen.get_height()/2;
    self.font_size = self.screen.get_width()/2;
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
class Menu:
  def __init__(self,screen, buttons = []):
    self.buttons = buttons;

class CountDown:
  def __init__(self):
    print








 











