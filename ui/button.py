import pygame
from pygame.color import THECOLORS
class Button:
  def __init__(self,dims=(100,100),pos=(100,100),text = "button"):
    ####Sizes
    self.dims = dims
    self.mergin = 5;
    self.pos = pos;
    self.font_fam = None
    ########Colors
    self.back_color_n = THECOLORS["grey"];
    self.back_color_h = THECOLORS["green"];
    self.font_color = THECOLORS["white"];
    ######components
    self.label = text;
    self.surface = pygame.Surface(self.dims)
    self.font_size = (self.dims[0]);
    self.set_font_size()
    if self.font_size>self.dims[1]:
      self.font_size = self.dims[1];
    self.font = pygame.font.Font(self.font_fam, self.font_size);
    self.surf = self.font.render(self.label, True, self.font_color);
    
  def set_font_size(self):
    font = pygame.font.Font(self.font_fam,self.font_size);
    if font.size(self.label)[0]>self.dims[0]:
      self.font_size=self.font_size-max(1,(font.size(self.label)[0]-self.dims[0])/len(self.label));
      self.set_font_size();


  def reinitialize(self):
    self.__init__(dims=self.dims,text = self.label)
  def is_hovered(self):
    pos = pygame.mouse.get_pos();
    constraints = [pos[0]<(self.pos[0]+self.dims[0]),(pos[0]>self.pos[0]), (pos[1]>self.pos[1]),(pos[1]<self.pos[1]+self.dims[1])]
    #print constraints;
    if all(constraints):
      return True;
    return False;
  def show(self):
    if self.is_hovered():
      self.surface.fill(self.back_color_h);
    else:
      self.surface.fill(self.back_color_n);
    x_0 = (self.surface.get_width()-self.surf.get_width())/2;
    y_0 = (self.surface.get_height()-self.surf.get_height())/2;
    self.surface.blit(self.surf,(x_0,y_0));
    return self.surface;
  def set_dims(self,dims):
    self.dims = dims;
    self.surface = pygame.Surface(self.dims);
def test():
  size = (120,120);
  pygame.init();
  screen = pygame.display.set_mode((400,400));
  button = Button(size)
  exit = False;
  while not exit:
    e = pygame.event.wait();
    if e.type==pygame.QUIT:
      exit=True;
    pos = (50,50)
    button.pos=pos;
    screen.blit(button.show(),pos);
    pygame.display.update();



  pygame.quit()
#test();
