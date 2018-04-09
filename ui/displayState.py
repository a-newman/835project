import pygame
from ui_utils import Button, ColorMap
class Idle:
  def __init__(self, screen, params = {}):

    self.screen = screen;
    self.bg_color = ColorMap.WHITE;
    self.clock = pygame.time.Clock();
    self.frame_rate = 30;

  def setupButton(self):
    button =  Button(screen);
    button.x = 250;
    button.y = 250;
    button.w = 200;
    button.h = 100;
    button.font_size = 60;
    button.set_font()
    button.text = "setup";
    button.font_color = ColorMap.BLACK;
    button.hoverColor = ColorMap.GREEN;
    button.staticColor = ColorMap.GREY;
    return button;
    
  def dispLoop(self):
    button  = self.setupButton()
    loop  = True
    while loop:
      for event in pygame.event.get():
        if event.type==pygame.QUIT:
          loop = False;
          pygame.quit();
          return False;
        elif event.type==pygame.MOUSEBUTTONDOWN:
          if button.is_hovered():
            print "Clicked!!!"
            return True;
      screen.fill(self.bg_color);
      button.show()

      pygame.display.flip();
      self.clock.tick(self.frame_rate);
pygame.init()
size = (500,500)
screen = pygame.display.set_mode(size)
idle = Idle(screen)
idle.dispLoop()