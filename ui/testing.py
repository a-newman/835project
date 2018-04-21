from PIL import Image
from resizeimage import resizeimage
import pygame
import numpy as np
class Clock:
  def __init__(self, size, in_img="images/clock.gif",out_img="images/clock.gif"):
    self.surf  = pygame.Surface((size,size));
    self.in_img = in_img;
    self.out_img = out_img;
    self.size = size;
    ###
    self.image = self.get_image();
    self.diagnol = self.get_diagnol();
    ##
    self.background_color=(0,0,0)
    self.clock_color = (0,255,0);

    self.font = pygame.font.Font("fonts/font.ttf", int(self.size*.8));
    
  def draw(self,count=0):
    font_surf = self.font.render(str(count), True, self.clock_color)
    self.surf.blit(self.image,(0,0))
    circle = pygame.draw.circle(self.surf, (23,45,86),(self.size/2,self.size/2),self.diagnol/2, (self.diagnol-self.size)/2);
    self.surf.blit(font_surf,((self.size-font_surf.get_width())/2,(self.size-font_surf.get_height())/2))
    return self.surf;
  def get_image(self):
    with open(self.in_img, 'r+b') as f:
      with Image.open(f) as image:
        cover = resizeimage.resize_cover(image, (self.size,self.size))
        cover.save(self.out_img, image.format)
    image = pygame.image.load(self.out_img);
    return image;
  def get_diagnol(self):
    return int(np.ceil(np.sqrt(2)*self.size));
def test():
  pygame.init();
  screen = pygame.display.set_mode((500,500))
  _clock = Clock(400).draw();

  clock = pygame.time.Clock()
  loop = True
  while loop:
    e = pygame.event.wait();
    if e.type==pygame.QUIT:
      loop = False
    screen.blit(_clock,(0,0))
    pygame.display.update()

    clock.tick()






  pygame.quit()
test()










 











