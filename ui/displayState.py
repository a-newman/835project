import pygame
from ui_utils import Button, ColorMap, CountDown
pic =  pygame.image.load('images/background.jpg')
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
    b_x = -100;
    b_y = -100;
    while loop:
      for event in pygame.event.get():
        if event.type==pygame.QUIT:
          loop = False;
          pygame.quit();
          return False;
        if event.type == pygame.VIDEORESIZE:
          self.screen=pygame.display.set_mode(event.dict['size'],pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
          self.screen.blit(pygame.transform.scale(pic,event.dict['size']),(0,0))
          pygame.display.flip()
        if event.type==pygame.MOUSEBUTTONDOWN:
          if button.is_hovered():
            print "You have clicked for setup!"
            return True;
      self.screen.fill(self.bg_color);
      self.screen.blit(pic,(-1,-1))
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
        if event.type==pygame.MOUSEBUTTONDOWN:
          if button.is_hovered():
            print "You're ready to start!"
            return True;
        if event.type == pygame.VIDEORESIZE:
          self.screen=pygame.display.set_mode(event.dict['size'],pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
          self.screen.blit(pygame.transform.scale(pic,event.dict['size']),(0,0))
          pygame.display.flip()
      self.screen.fill(self.bg_color);
      self.screen.blit(pic,(0,0))
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
    button  = self.backButton();
    count = None;
    while loop:
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              loop = False;
              value = 'quit';
          if event.type == pygame.USEREVENT:
            count = cd.count();
          if event.type == pygame.MOUSEBUTTONDOWN:
            if button.is_hovered():
              loop = False;
              value = 'back';
          if event.type == pygame.VIDEORESIZE:
            self.screen=pygame.display.set_mode(event.dict['size'],pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
            self.screen.blit(pygame.transform.scale(pic,event.dict['size']),(0,0))
            pygame.display.flip()

      self.screen.fill(ColorMap.WHITE);
      cd.show();
      button.show();
      if count=='go':
        loop = False;
   
      pygame.display.flip();
   
      # --- Limit to 60 frames per second
      self.clock.tick(60);
    return value;


class Recording:
  def __init__(self, screen):
    self.screen = screen;
    self.bg_color = ColorMap.WHITE;
    self.clock  = pygame.time.Clock();
    self.frame_rate = 30;
  def recordButton(self):
    button =  Button(self.screen);
    button.w = 100;
    button.h = 100;
    button.x = 250;
    button.y = 250;
    button.font_size = 100;
    button.set_font()
    button.text = "Recording..";
    button.font_color = ColorMap.RED;
    button.hoverColor = ColorMap.WHITE;
    button.staticColor = ColorMap.WHITE;
    return button;


  def dispLoop(self):
    button  = self.recordButton()
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
        if event.type == pygame.VIDEORESIZE:
          self.screen=pygame.display.set_mode(event.dict['size'],pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
          self.screen.blit(pygame.transform.scale(pic,event.dict['size']),(0,0))
          pygame.display.flip()
      self.screen.fill(self.bg_color);
      self.screen.blit(pic,(0,0))
      button.show()

      pygame.display.flip();
      self.clock.tick(self.frame_rate);
class Processing:
  def __init__(self, screen):
    self.screen = screen;
    self.bg_color = ColorMap.WHITE;
    self.clock  = pygame.time.Clock();
    self.frame_rate = 30;
  
  def recordButton(self):
    button =  Button(self.screen);
    button.w = 100;
    button.h = 100;
    button.x = 250;
    button.y = 250;
    button.font_size = 100;
    button.set_font()
    button.text = "Processing..";
    button.font_color = ColorMap.GREEN;
    button.hoverColor = ColorMap.WHITE;
    button.staticColor = ColorMap.WHITE;
    return button 
  def dispLoop(self):
    button  = self.recordButton()
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
        if event.type == pygame.VIDEORESIZE:
          self.screen=pygame.display.set_mode(event.dict['size'],pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
          self.screen.blit(pygame.transform.scale(pic,event.dict['size']),(0,0))
          pygame.display.flip()
      self.screen.fill(self.bg_color);
      self.screen.blit(pic,(0,0))
      button.show()

      pygame.display.flip();
      self.clock.tick(self.frame_rate);

class Feedback:
  def __init__(self, screen):
    self.screen = screen;
    self.bg_color = ColorMap.WHITE;
    self.clock  = pygame.time.Clock();
    self.frame_rate = 30;
    self.mergin=self.screen.get_width()*.02;
    ## lose parameters 
    self.sf_x = self.screen.get_width()*.45;
    self.sf_y = self.screen.get_height();
    self.sf_txt = (self.screen.get_width()*.5, self.screen.get_height()*.35)
    ## victory parameters
    self.hf_x = self.screen.get_width()*.45;
    self.hf_y = self.screen.get_height();
    self.hf_txt = (self.screen.get_width()*.5, self.screen.get_height()*.35)
    ### Exit parameters 
    self.exit_text = (self.screen.get_width()*.5,self.screen.get_height()*.55)
  def doubletxt(self,txt1,txt2,dims,fnt_s1,fnt_s2,ratio):
    reaction = pygame.font.Font(None, fnt_s1);
    cmplmt = pygame.font.Font(None, fnt_s2);
    s_surf = reaction.render(txt1, True, ColorMap.RED)
    c_surf = cmplmt.render(txt2, True, ColorMap.BLUE)
    
    if s_surf.get_width()+self.mergin>self.screen.get_width:
      fnt_s1-=2;
      self.doubletxt(txt1,txt2,dims,fnt_s1,fnt_s2)
    if c_surf.get_width()+self.mergin>self.screen.get_width:
      fnt_s2-=2;
      self.doubletxt(txt1,txt2,dims,fnt_s1,fnt_s2)
    if ratio>1:
      fnt_s1/=ratio;
    else:
      fnt_s2*=ratio;
    offset = s_surf.get_height();

    x0 = self.screen.get_width();
    y0 = dims[1]-s_surf.get_width()/2;
    y1 = dims[1]-c_surf.get_width()/2;
    ###
    sx_mod = x0*(1-(float(s_surf.get_width())/x0));
    cx_mod = x0*(1-(float(c_surf.get_width())/x0));
    s_x = sx_mod/2;
    c_x = cx_mod/2;
    self.screen.blit(s_surf,(s_x,y0));
    self.screen.blit(c_surf,(c_x,y0+offset));
  def imageDisp(self,img,dims):
    x_0 = dims[0]-img.get_width()/2;
    y_0 = dims[1]- img.get_height()-self.mergin;
    print "image coordinates: ",x_0,y_0;
    print "images dims:", img.get_width(), img.get_width()
    self.screen.blit(img,(x_0,y_0));


  def loseText(self):
    dims= self.sf_txt;
    txt1 = 'SORRY!';
    txt2 = "NEXT TIME";
    fnt_s1 = 80;
    fnt_s2 = 50;
    ratio=fnt_s2/float(fnt_s1);
    self.doubletxt(txt1,txt2,dims,fnt_s1,fnt_s2,ratio);

  def victoryText(self):
    dims= self.hf_txt;
    txt1 = 'GONGRAT!';
    txt2 = "YOU DID IT!";
    fnt_s1 = 80;
    fnt_s2 = 50;
    ratio=fnt_s2/float(fnt_s1);
    self.doubletxt(txt1,txt2,dims,fnt_s1,fnt_s2,ratio);
  def loseDisp(self):
    face = pygame.image.load('images/sad_face.png');
    self.imageDisp(face,(self.sf_x,self.sf_y))




  def victoryDisp(self):
    face = pygame.image.load('images/happy_face.png');
    self.imageDisp(face,(self.hf_x,self.hf_y));

  def nextWord(self):
    dims= self.exit_text;
    txt1 = 'READY FOR THE NEXT WORD?';
    txt2 = "GOOD LUCK!";
    fnt_s1 = 30;
    fnt_s2 = 50;
    ratio=fnt_s2/float(fnt_s1);
    self.doubletxt(txt1,txt2,dims,fnt_s1,fnt_s2,ratio);
  def dispLoop(self):
    '''
    if random number x is greator than .5:
      Do celebration:
        - show fireworks
        - Show they go it 
    else:
      Show them a sad face!
      tell them they didn't get it
    ''' 
    value = True;
    pygame.time.set_timer(pygame.USEREVENT, 1000);
    count = 3;
    #########
    import random 
    number = random.random()
    #########
    if number<.5:
      loop= True;
      text  = self.loseText()
      disp = self.loseDisp()
      while loop:
        for event in pygame.event.get():
          if event.type==pygame.QUIT:
            loop = False;
            value = False;
            pygame.quit();
        ###Timer herer
          if event.type==pygame.USEREVENT:
            count-=1;
          if event.type == pygame.VIDEORESIZE:
            self.screen=pygame.display.set_mode(event.dict['size'],pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
            self.screen.blit(pygame.transform.scale(pic,event.dict['size']),(0,0))
            pygame.display.flip()
        self.screen.fill(self.bg_color);
        self.screen.blit(pic,(0,0))
        #text.show()
        #disp.show()
        if count==0:
          loop = False
        self.loseText()
        self.loseDisp()

        pygame.display.flip();
        self.clock.tick(self.frame_rate);
    else:
      loop = True
      text  = self.victoryText()
      disp = self.victoryDisp()
      while loop:
        for event in pygame.event.get():
          if event.type==pygame.QUIT:
            loop = False;
            pygame.quit();
          ##Timer here
          if event.type==pygame.USEREVENT:
            count-=1;

        self.screen.fill(self.bg_color);
        self.screen.blit(pic,(0,0))
        if count==0:
          loop =  False
        self.victoryText()
        self.victoryDisp()

        pygame.display.flip();
        self.clock.tick(self.frame_rate);
    #next word
    loop = True 
    count = 3;
    ##text = nextWord()
    while loop:
      for event in pygame.event.get():
        if event.type==pygame.QUIT:
          loop = False;
          pygame.quit();
        if event.type==pygame.USEREVENT:
            count-=1;
        ##Timer here
      self.screen.fill(self.bg_color);
      self.screen.blit(pic,(0,0))
      self.nextWord()

      pygame.display.flip();
      self.clock.tick(self.frame_rate);
      if count==0:
        loop= False
    return value;






        

  