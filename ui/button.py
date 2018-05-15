import pygame
from pygame.color import THECOLORS
class Button:
  '''
  A class that defines a clickable button as Pygame surface.
  attributes 
    - dims: Button dimensions
    - pos: Position of the display Window
    - text: The libel of the Button
  methods
   - set_font_size: Fits the text into the bounding box of the Button
   - se_font_color: Changes the font color
   - reinitialize: reinializes the button class
   - is_hovered: True if the mouse is hovering the button
   - show: Does the internal rendering calls and returns the button as Pygame surface
   - set_dims: sets the dimensions of the button to the new dimensions passed into this  method
  '''
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
    self.font_size = (self.dims[1]);
    self.set_font_size()
    if self.font_size>self.dims[1]:
      self.font_size = self.dims[1];
    self.font = pygame.font.Font(self.font_fam, self.font_size);
    self.surf = self.font.render(self.label, True, self.font_color);
  def create(self):
    return pygame.font.Font(self.font_fam,self.font_size);
  def set_font_size(self):
    font = pygame.font.Font(self.font_fam,self.font_size);
    while True:
      if font.size(self.label)[0]<=self.dims[0]:
        break
      self.font_size=self.font_size-max(1,(font.size(self.label)[0]-self.dims[0])/len(self.label));
      font = pygame.font.Font(self.font_fam,self.font_size);
      
  def set_font_color(self):
    self.font = pygame.font.Font(self.font_fam, self.font_size);
    self.surf = self.font.render(self.label, True, self.font_color);


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
    self.set_font_color()
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
