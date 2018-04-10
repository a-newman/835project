import pygame
from ui_utils import Button, ColorMap, CountDown

class Idle:
  def __init__(self, screen, params = {}):

    self.screen = screen;
    self.bg_color = ColorMap.WHITE;
    self.clock = pygame.time.Clock();
    self.frame_rate = 30;

  def setupButton(self):
    button =  Button(self.screen);
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
            print "You have clicked for setup!"
            return True;
      self.screen.fill(self.bg_color);
      button.show()

      pygame.display.flip();
      self.clock.tick(self.frame_rate);
# pygame.init()
# size = (500,500)
# screen = pygame.display.set_mode(size)
# idle = Idle(screen)
# idle.dispLoop()

class Setup:
  def __init__(self, screen):
    self.screen = screen;
    self.bg_color = ColorMap.WHITE;
    self.clock  = pygame.time.Clock();
    self.frame_rate = 30;
    #TODO
    #1. add the menu 
    #2. add the text
  def startButton(self):
    button =  Button(self.screen);
    button.x = 250;
    button.y = 250;
    button.w = 200;
    button.h = 100;
    button.font_size = 60;
    button.set_font()
    button.text = "Start";
    button.font_color = ColorMap.BLACK;
    button.hoverColor = ColorMap.GREEN;
    button.staticColor = ColorMap.GREY;
    return button;

  def dispLoop(self):
    button = self.startButton()
    loop = True 
    while loop:
      for event in pygame.event.get():
        if event.type==pygame.QUIT:
          loop = False;
          pygame.quit();
          return False;
        elif event.type==pygame.MOUSEBUTTONDOWN:
          if button.is_hovered():
            print "You're ready to start!"
            return True;
      self.screen.fill(self.bg_color);
      button.show()

      pygame.display.flip();
      self.clock.tick(self.frame_rate);



class Start:
  def __init__(self, screen):
    self.screen = screen;
    self.bg_color = ColorMap.WHITE;
    self.clock  = pygame.time.Clock();
    self.frame_rate = 30;
  def countSetup(self):
    cd = CountDown(self.screen)
    cd.x = 250;
    cd.y = 250;
    cd.h = 200;
    cd.w = 200;
    cd.font_size= 100;
    cd.font = pygame.font.Font(None, 100)
    cd.font_color = ColorMap.BLACK;
    cd.hoverColor = ColorMap.GREY;
    cd.staticColor = ColorMap.GREY;
    return cd
  def backButton(self):
    button =  Button(self.screen);
    button.w = 200;
    button.h = 100;
    button.x = self.screen.get_width()-button.w-10;
    button.y = self.screen.get_height()-button.h-10;
    button.font_size = 60;
    button.set_font()
    button.text = "GoBack";
    button.font_color = ColorMap.BLACK;
    button.hoverColor = ColorMap.GREEN;
    button.staticColor = ColorMap.GREY;
    return button;
  def dispLoop(self):
    pygame.time.set_timer(pygame.USEREVENT, 1000);
    loop = True;
    value = 'finished';
    cd = self.countSetup();
    button  = self.backButton()
    count = None
    while loop:
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              loop = False;
              value = 'quit';
          if event.type == pygame.USEREVENT:
            count = cd.count()
          if event.type == pygame.MOUSEBUTTONDOWN:
            if button.is_hovered():
              loop = False;
              value = 'back';

      self.screen.fill(ColorMap.WHITE)
      cd.show()
      button.show()
      if count=='go':
        loop = False;
   
      pygame.display.flip()
   
      # --- Limit to 60 frames per second
      self.clock.tick(60)
    return value;


class Recording:
  def __init__(self, screen):
    self.screen = screen;
    self.bg_color = ColorMap.WHITE;
    self.clock  = pygame.time.clock();
    self.frame_rate = 30;
  def dispLoop(self):
    pass
class Processing:
  def __init__(self, screen):
    self.screen = screen;
    self.bg_color = ColorMap.WHITE;
    self.clock  = pygame.time.Clock();
    self.frame_rate = 30;
  def dispLoop(self):
    pass 

class Feedback:
  def __init__(self, screen):
    self.screen = screen;
    self.bg_color = ColorMap.WHITE;
    self.clock  = pygame.time.Clock();
    self.frame_rate = 30;
  def dispLoop(self):
    pass 
  