import pygame 
class Idle:
  def __init__(self, screen, params = {}):
    self.screen = screen;
  def setupButton(self):
    pass 
  def dispLoop:
    loop  = True
    while loop:
      for event in pygame.event.get():
        if event.type==pygame.QUIT:
          loop = False;
          pygame.quit();
        elif event.type==pygame.button;

      pygame.display.flip();
      clock.tick(60);
