import pygame
class ControlWords:
  def __init__(self, words,font_size=30,pose=(12,12),size=(500,200)):
    self.words = words;
    self.pos = (12,12)
    self.font_size = font_size;
    self.pose = pose;
    self.surf = pygame.Surface(size);
    self.word_color = (0,234,255);
    self.definition_color = (255,255,255);
    self.font_fam = None;

  def show(self):
    font = pygame.font.Font(self.font_fam, 3*self.font_size/2)
    font.set_underline(True)
    suft = font.render("Control words",True,self.definition_color)
    self.surf.blit(suft,self.pos)
    y = self.pos[1]+suft.get_height()
    x= self.pos[0]
    for word in self.words:
      font_w = pygame.font.Font(self.font_fam, self.font_size).render(word,True,self.word_color);
      font_d = pygame.font.Font(self.font_fam, self.font_size).render(self.words[word],True,self.definition_color);
      self.surf.blit(font_w,(x,y));
      self.surf.blit(font_d,(x+font_w.get_width(),y));
      y+= font_w.get_height()
    return self.surf
def test():
  pygame.init()
  words = {"pause: ":"to pause","run: ": "to unpause","quit: ":"to quit","repeat: ": "To repeat the last word"}
  ctl_words = ControlWords(words, font_size=40,pose=(120, 430),size = (660, 200) );
  screen = pygame.display.set_mode((800,800));
  while True:
    e = pygame.event.wait();
    if e.type==pygame.QUIT:
      break
    screen.blit(ctl_words.show(),ctl_words.pose)
    pygame.display.update()
#test()

