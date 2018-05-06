import pygame
from ui.ui_utils import Button, ColorMap, CountDown, CircularArray,scolling_backgrnd
import threading

BASE_IMAGE_PATH = "ui/images/" 

pic =  pygame.image.load(BASE_IMAGE_PATH + 'background.jpg')

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
    ###
    bg_0,bg_1 = scolling_backgrnd(self.screen)
    ###
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
            print("You have clicked for setup!")
            return True;
      self.screen.fill(self.bg_color);
      #self.screen.blit(pic,(-1,-1))
      bg_0.move();
      bg_1.move();
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
    bg_0,bg_1 = scolling_backgrnd(self.screen)
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
            print("You're ready to start!")
            return True;
        if event.type == pygame.VIDEORESIZE:
          self.screen=pygame.display.set_mode(event.dict['size'],pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
          self.screen.blit(pygame.transform.scale(pic,event.dict['size']),(0,0))
          pygame.display.flip()
      self.screen.fill(self.bg_color);
      #self.screen.blit(pic,(0,0))
      bg_0.move();
      bg_1.move();
      button.show()

      pygame.display.flip();
      self.clock.tick(self.frame_rate);



class Start:
  def __init__(self, screen,ui = None, backend={}):
    self.ui = ui;
    self.screen = screen;
    self.bg_color = ColorMap.WHITE;
    self.clock  = pygame.time.Clock();
    self.frame_rate = 30;
    self.mergin = 12;
    world_list =  backend['words'];
    self.arr = CircularArray(world_list);
  def countSetup(self):
    cd = CountDown(self.screen)
    cd.h = 200;
    cd.w = 200;
    cd.x = self.screen.get_width()/2.2;
    cd.y = self.screen.get_height()-10;
    
    cd.font_size= 150;
    cd.font = pygame.font.Font(None, 150)
    cd.font_color = ColorMap.RED;
    cd.hoverColor = ColorMap.SKY;
    cd.staticColor = ColorMap.SKY;
    return cd
  def backButton(self):
    button =  Button(self.screen);
    button.w = 100;
    button.h = 50;
    button.x = self.screen.get_width()-button.w-10;
    button.y = self.screen.get_height()-10;
    button.font_size = 60;
    button.set_font()
    button.text = "GoBack";
    button.font_color = ColorMap.BLACK;
    button.hoverColor = ColorMap.GREEN;
    button.staticColor = ColorMap.GREY;
    return button;

  def dspWord(self,word,fnt_s):
    font = pygame.font.Font(None, fnt_s);
    surf = font.render(word, True, ColorMap.WHITE)
    if surf.get_width()+self.mergin > self.screen.get_width():
      fnt_s-=2;
      self.dspWord(word,fnt_s)
    x0 = self.screen.get_width();
    y0 = self.screen.get_width()/5;
    x_mod = x0*(1-(float(surf.get_width())/x0));
    
    x = x_mod/2;
  
    self.screen.blit(surf,(x,y0));
  def get_word(self,rand = False):
    word = None;
    if rand:
      word = self.arr.randRoll();
    else:
      word = self.arr.roll();
    self.ui.test_word = word
    return word 
  def dispWord(self,word):
    word = "word: "+word;
    fnt_s = 100;
    self.dspWord(word,fnt_s);
    
  def dispLoop(self):
    bg_0,bg_1 = scolling_backgrnd(self.screen)
    
    pygame.time.set_timer(pygame.USEREVENT, 1000);
    loop = True;
    value = 'finished';
    cd = self.countSetup();
    button  = self.backButton();
    count = None;
    word = self.get_word()
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
      bg_0.move();
      bg_1.move();
      cd.show();
      button.show();
      self.dispWord(word)
      if count=='go':
        loop = False;
   
      pygame.display.flip();
   
      # --- Limit to 60 frames per second
      self.clock.tick(self.frame_rate);
    return value;


class Recording:
  def __init__(self, screen, ui=None,backend={}):
    self.ui = ui;
    self.screen = screen;
    self.bg_color = ColorMap.WHITE;
    self.clock  = pygame.time.Clock();
    self.frame_rate = 30;
    self.word = "None"
    self.backend=backend
  def recordButton(self):
    button =  Button(self.screen);
    if self.screen.get_width()<self.screen.get_height():
      button.w = self.screen.get_width()/3;
      button.h = self.screen.get_width()/5;
    else:
      button.w = self.screen.get_height()/3;
      button.h = self.screen.get_height()/5;
    button.x = self.screen.get_width()/2;
    button.y = self.screen.get_height()/2;
    button.font_size = 100;
    button.set_font()
    button.text = "Recording...";
    button.font_color = ColorMap.RED;
    button.hoverColor = ColorMap.WHITE;
    button.staticColor = ColorMap.WHITE;
    return button;


  def dispLoop(self):
    bg_0,bg_1 = scolling_backgrnd(self.screen)

    thread = myThread(self.backend['get_classification'], self)
    thread.start()
    pygame.time.set_timer(pygame.USEREVENT, 1000);
    button  = self.recordButton()
    loop  = True
    counter = 2;
    while loop:

      for event in pygame.event.get():
        if event.type==pygame.QUIT:
          loop = False;
          pygame.quit();
          return False;
        if event.type==pygame.MOUSEBUTTONDOWN:
          if button.is_hovered():
            print("You have clicked for setup!")
            return True;
        if event.type == pygame.VIDEORESIZE:
          self.screen=pygame.display.set_mode(event.dict['size'],pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
          self.screen.blit(pygame.transform.scale(pic,event.dict['size']),(0,0))
          pygame.display.flip()
        if event.type==pygame.USEREVENT:
          counter-=1
      if counter==0:
        self.ui.result_word = self.word;
        loop=False
      self.screen.fill(self.bg_color);
      #self.screen.blit(pic,(0,0))
      bg_0.move();
      bg_1.move();
      button.show()

      pygame.display.flip();
      #print("resulting word: ",self.word)
      self.clock.tick(self.frame_rate);
class Processing:
  def __init__(self, screen,ui=None,backend={}):
    self.ui = ui;
    self.screen = screen;
    self.bg_color = ColorMap.WHITE;
    self.clock  = pygame.time.Clock();
    self.frame_rate = 30;
  
  def recordButton(self):
    button =  Button(self.screen);
    if self.screen.get_width()<self.screen.get_height():
      button.w = self.screen.get_width()/3;
      button.h = self.screen.get_width()/5;
    else:
      button.w = self.screen.get_height()/3;
      button.h = self.screen.get_height()/5;
    button.x = self.screen.get_width()/2;
    button.y = self.screen.get_height()/2;
    button.font_size = 100;
    button.set_font()
    button.text = "Processing..";
    button.font_color = ColorMap.GREEN;
    button.hoverColor = ColorMap.WHITE;
    button.staticColor = ColorMap.WHITE;
    return button 
  def dispLoop(self):
    bg_0,bg_1 = scolling_backgrnd(self.screen)
    button  = self.recordButton()
    loop  = False;
    while loop:
      for event in pygame.event.get():
        if event.type==pygame.QUIT:
          loop = False;
          pygame.quit();
          return False;
        elif event.type==pygame.MOUSEBUTTONDOWN:
          if button.is_hovered():
            print("You have clicked for setup!")
            return True;
        if event.type == pygame.VIDEORESIZE:
          self.screen=pygame.display.set_mode(event.dict['size'],pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
          self.screen.blit(pygame.transform.scale(pic,event.dict['size']),(0,0))
          pygame.display.flip()
      self.screen.fill(self.bg_color);
      #self.screen.blit(pic,(0,0))
      bg_0.move();
      bg_1.move();
      button.show()

      pygame.display.flip();
      self.clock.tick(self.frame_rate);

class Feedback:
  def __init__(self, screen,ui=None ,backend={}):
    self.ui = ui;
    self.screen = screen;
    self.bg_color = ColorMap.WHITE;
    self.clock  = pygame.time.Clock();
    self.frame_rate = 30;
    self.mergin=self.screen.get_width()*.02;
    ## lose parameters 
    self.sf_x = self.screen.get_width()*.48;
    self.sf_y = self.screen.get_height();
    self.sf_txt = (self.screen.get_width()*.5, self.screen.get_height()*.38)
    ## victory parameters
    self.hf_x = self.screen.get_width()*.45;
    self.hf_y = self.screen.get_height();
    self.hf_txt = (self.screen.get_width()*.5, self.screen.get_height()*.38)
    ### Exit parameters 
    self.exit_text = (self.screen.get_width()*.5,self.screen.get_height()*.55)
  def doubletxt(self,txt1,txt2,dims,fnt_s1,fnt_s2,ratio,clr1=ColorMap.RED,clr2=ColorMap.BLUE):
    reaction = pygame.font.Font(None, fnt_s1);
    cmplmt = pygame.font.Font(None, fnt_s2);
    s_surf = reaction.render(txt1, True, clr1)
    c_surf = cmplmt.render(txt2, True, clr2)
    
    if s_surf.get_width()+self.mergin>self.screen.get_width():
      fnt_s1-=2;
      self.doubletxt(txt1,txt2,dims,fnt_s1,fnt_s2)
    if c_surf.get_width()+self.mergin>self.screen.get_width():
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
    y_0 = dims[1]- img.get_height()-self.mergin
    #print("image coordinates: ",x_0,y_0)
    #print("images dims:", img.get_width(), img.get_width())
    self.screen.blit(img,(x_0,y_0))


  def loseText(self,clr1=ColorMap.RED,clr2=ColorMap.RED):
    dims= self.sf_txt;
    txt1 = 'SORRY!';
    txt2 = "YOU HAD: "+self.ui.result_word;
    fnt_s1 = 80;
    fnt_s2 = 50;
    ratio=fnt_s2/float(fnt_s1);
    self.doubletxt(txt1,txt2,dims,fnt_s1,fnt_s2,ratio,clr1,clr2);

  def victoryText(self,clr1=ColorMap.GREEN,clr2=ColorMap.GREEN):
    dims= self.hf_txt;
    txt1 = 'GONGRATS!';
    txt2 = "YOU DID IT!";
    fnt_s1 = 80;
    fnt_s2 = 50;
    ratio=fnt_s2/float(fnt_s1);
    self.doubletxt(txt1,txt2,dims,fnt_s1,fnt_s2,ratio,clr1,clr2);
  def loseDisp(self):
    face = pygame.image.load(BASE_IMAGE_PATH + 'sad_face.png');
    self.imageDisp(face,(self.sf_x,self.sf_y))
  def display_result(self,clr1=None,clr2=None):
    dims  = (self.screen.get_width()*.55, self.screen.get_height()*.55)
    txt1 = "You had:"
    txt2 = self.ui.result_word
    fnt_s1 = 50;
    fnt_s2 = 60;
    ratio=fnt_s2/float(fnt_s1);
    self.doubletxt(txt1,txt2,dims,fnt_s1,fnt_s2,ratio,clr1,clr2);




  def victoryDisp(self):
    face = pygame.image.load(BASE_IMAGE_PATH + 'happy_face.png');
    self.imageDisp(face,(self.hf_x,self.hf_y));

  def nextWord(self,clr1=ColorMap.WHITE,clr2=ColorMap.WHITE):
    dims= self.exit_text;
    txt1 = 'READY FOR THE NEXT WORD?';
    txt2 = "GOOD LUCK!";
    fnt_s1 = 30;
    fnt_s2 = 50;
    ratio=fnt_s2/float(fnt_s1);
    self.doubletxt(txt1,txt2,dims,fnt_s1,fnt_s2,ratio,clr1,clr2);
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
    bg_0,bg_1 = scolling_backgrnd(self.screen)
    value = True;
    pygame.time.set_timer(pygame.USEREVENT, 1000);
    count = 3;
    #########
    import random 
    number = random.random()
    #########
    #print('test:',self.ui.test_word,'resulting:',self.ui.result_word);
    if self.ui.test_word!=self.ui.result_word:
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
        #self.screen.blit(pic,(0,0))
        #text.show()
        #disp.show()
        bg_0.move();
        bg_1.move();
        if count==0:
          loop = False
        self.loseText()
        self.loseDisp()
        #self.display_result();

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
        bg_0.move();
        bg_1.move();
        #self.screen.blit(pic,(0,0))
        if count==0:
          loop =  False
        self.victoryText()
        self.victoryDisp()
        #self.display_result();

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
      #self.screen.blit(pic,(0,0))
      bg_0.move();
      bg_1.move();
      self.nextWord();
      

      pygame.display.flip();
      self.clock.tick(self.frame_rate);
      if count==0:
        loop= False
    return value;



class myThread (threading.Thread):
  def __init__(self, funct, obj):
    threading.Thread.__init__(self)
    self.funct = funct
    self.obj = obj;
  def run(self):
    self.funct(self.obj)



        

  
