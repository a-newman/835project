import pygame as pg
from button import Button;



COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')



class InputBox:
  '''
  class that defines a text box as Pygame surface
  parameters 
    - (w,h): dimensions of the box
    - (x,y): coordinates(position of the box) in the display window.
  methods
    - handle_event: handles keyboard and mouse events(e.g. user type a new word) 
    - update: changes the width of the box for long text 
    - draw: renders the text box on the input screen.
  '''
  

  def __init__(self, x, y, w, h, text=''):
    self.button_w = w/2
    self.butt = Button(dims=(self.button_w,h),pos=(x,y),text = "save")
    self.rect = pg.Rect(x, y, w, h)
    self.color = COLOR_INACTIVE
    self.text = text
    self.font = pg.font.Font(None, 32)
    self.txt_surface = self.font.render(text, True, self.color)
    self.active = False
    self.surf = pg.Surface((w,h))


  def handle_event(self, event):
    if event.type == pg.MOUSEBUTTONDOWN:
      # If the user clicked on the input_box rect.
      if self.rect.collidepoint(event.pos):
        # Toggle the active variable.
        self.active = not self.active

      else:
        self.active = False
      # Change the current color of the input box.
      self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
    if event.type == pg.KEYDOWN:
      if self.active:
        if event.key == pg.K_RETURN:
          print(self.text)
          self.text = ''
        elif event.key == pg.K_BACKSPACE:
          self.text = self.text[:-1]
        else:
          self.text += event.unicode
        # Re-render the text.
        self.txt_surface = self.font.render(self.text, True, self.color)

  def update(self):
    # Resize the box if the text is too long.
    width = max(200, self.txt_surface.get_width()+10)
    self.rect.w = width

  def draw(self, screen):
    # Blit the text.
    self.surf.fill((30, 30, 30))
    self.surf.blit(self.txt_surface,(0,0))
    screen.blit(self.surf, (self.rect.x+5, self.rect.y+5))
    # Blit the rect.
    pg.draw.rect(screen, self.color, self.rect, 2)



def main():
  clock = pg.time.Clock()
  input_box1 = InputBox(100, 100, 140, 32)
  input_boxes = [input_box1]
  done = False

  while not done:
    for event in pg.event.get():
      if event.type == pg.QUIT:
          done = True
      for box in input_boxes:
          box.handle_event(event)

    for box in input_boxes:
      box.update()

    screen.fill((30, 30, 30))
    for box in input_boxes:
      box.draw(screen)

    pg.display.flip()
    clock.tick(30)


# if __name__ == '__main__':
#      main()
#      pg.quit()
