import pygame
class Button:
  def __init__(self,screen, pose=(None,None), dimensions=(None,None),text=None,font_color=None, hoverColor=None,staticColor=None):
    self.screen = screen;
    self.x = pose[0];
    self.y = pose[1];
    self.h = dimensions[0];
    self.w = dimensions[1];
    self.font = pygame.font.Font(None, 20)
    self.text = text;
    self.font_color = font_color;
    self.hoverColor = hoverColor;
    self.staticColor = staticColor;
    self.color = self.staticColor;

  def is_hovered(self):
    pos = pygame.mouse.get_pos()
    return self.x <= pos[0] and self.x + self.w > pos[0] and \
               self.y <= pos[1] and self.y + self.h > pos[1];

  def draw(self):
    surf = self.font.render(self.text, True, self.font_color)
    rect = (self.x, self.y, self.w, self.h)
    x0 = self.x + (self.w - surf.get_width())/2
    y0 = self.y + (self.h - surf.get_height())/2
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
  WHITE = (255, 255, 255)
  GREEN = (0, 255, 0)
  BLUE = (0,0,255)
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
    button.h = 50;
    button.w = 100;
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
button_test()

