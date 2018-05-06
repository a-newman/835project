import pygame 
from button import Button
from sidebar import Sidebar
import topbar

def build():
  ########sizes
  mergins = 20;
  win_size = (800,700);
  top_size = (win_size[0]-2*mergins,30);
  side_size = (100,win_size[1]-top_size[1]-2*mergins);
  word_size = (win_size[0]-mergins*2-side_size[0],80)

  #####coordinates 
  top_cord = (mergins,mergins);
  side_cord = (mergins,mergins+top_size[1]);
  word_cord = (side_size[0]+mergins,mergins+top_size[1])
  #####initializing 
  pygame.init();
  screen = pygame.display.set_mode(win_size);
  #####
  buttons = [Button(text="Quit"),Button(text="Setup"),Button(text="Depth")];
  side_bar = Sidebar(side_cord, w=side_size[0],h=side_size[1],buttons=buttons);
  #####
  top_bar = topbar.topBar(top_size,pos=top_cord);
  #####
  word_bar = topbar.word(word_size,"word",pos=word_cord);
  clock = pygame.time.Clock()
  

  #####
  exit = False 
  while not exit:
    e = pygame.event.wait();
    if e.type==pygame.QUIT:
      exit = True;

    cntnr = pygame.Surface((win_size[0]-2*mergins+4,win_size[1]-2*mergins+4));
    ####
    import random
    r = random.randint(23,150)
    g = random.randint(23,150)
    b = random.randint(23,150)
    ####
    cntnr.fill((r,g,b));
    side_surf = side_bar.draw_buttons();
    screen.blit(cntnr,(mergins-2,mergins-2))
    screen.blit(top_bar,top_cord);
    screen.blit(side_surf,side_cord);
    screen.blit(word_bar,word_cord);
    pygame.display.update();
    clock.tick(40)



  pygame.quit();
build()


