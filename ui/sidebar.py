from button import Button 
import pygame
from pygame.color import THECOLORS

class Sidebar:
  def __init__(self,pos,w=200,h=800,buttons=[]):
    self.pos = (100,100)
    self.buttons = buttons;
    self.side_mergin = 10;
    self.top_mergin = 10;
    self.space = 10;
    self.w = w;
    self.h = h;
    self.surf = pygame.Surface((self.w, self.h))
    #####
    self.bg_color = THECOLORS['white']
    self.surf.fill(self.bg_color)
    #####
    self.b_w = self.w-2*self.side_mergin;
    self.b_h = self.w/3;
    self.button_update()
  def draw_buttons(self):
    for index,button in enumerate(self.buttons):
      b_surf = button.show()
      pos = self.get_button_pos(index);
      button.pos = (pos[0]+self.pos[0],pos[1]+self.pos[1])
      self.surf.blit(b_surf,pos);

    return self.surf

  def get_button_pos(self,index):
    x = self.side_mergin;
    y = self.top_mergin+index*(self.space+self.b_h);
    return (x,y)
  def button_update(self):
    self.b_w = self.w-2*self.side_mergin;
    self.b_h = self.w/2;
    for button in self.buttons:
      button.dims = (self.b_w, self.b_h);
      button.reinitialize();
def test():
  size = (120,600);
  pygame.init();
  screen = pygame.display.set_mode((800,800));
  buttons = [Button(dims=size,text="buton1"),Button(dims=size,text="buton2"),Button(dims=size,text="buton3")];
  bar = Sidebar((50,50),w=size[0],h=size[1],buttons = buttons)
  exit = False;
  while not exit:
    e = pygame.event.wait();
    if e.type==pygame.QUIT:
      exit=True;
    surf = bar.draw_buttons();
    screen.blit(surf,bar.pos);
    pygame.display.update();



  pygame.quit()
#test()





  
