import pygame
from pygame.color import THECOLORS
pygame.init()

class Text:
  def __init__(self, parent, w=100, h=50, pos=(0,0), text = "None",color = THECOLORS['white']):
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
    self.surf.fill(THECOLORS['black'])
    self.parent.blit(self.surf,self.pos);

if __name__ == '__main__':
  WINSIZE = 800,640;
  #screen_lock = thread.allocate()
  screen = pygame.display.set_mode(WINSIZE,0,16)
  #mems = PykinectInt(screen, backend = backend);
  #mems.loop(); 
  font = pygame.font.Font(None, 100);
  txt_ob = font.render("self.text", True, THECOLORS['white'])
  clock = pygame.time.Clock()
  txt = Text(screen);
  while True:
    print "running"
    txt.show()
    screen.blit(txt_ob,(2,8))
    pygame.display.update()
    clock.tick(34)
