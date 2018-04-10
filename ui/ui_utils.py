import pygame
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
  def set_font(self):
    self.font=pygame.font.Font(None, self.font_size)

  def is_hovered(self):
    pos = pygame.mouse.get_pos()
    return self.x-self.w/2 <= pos[0] and self.x + self.w/2 > pos[0] and \
               self.y-self.h <= pos[1] and self.y > pos[1];

  def draw(self):
    surf = self.font.render(self.text, True, self.font_color)
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
  def __init__(self,screen, second=20):
    Button.__init__(self, screen)
    self.counts = ['go','GO!']+range(second);
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





