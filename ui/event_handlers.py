
import threading
from copy import deepcopy
def mouse_handle(obj,done):
  if obj.depth_button.is_hovered():
    obj.show_depth=not obj.show_depth
  if obj.state==obj.SETUP:
    ##if hovering mode: set the mode to mode that mode 
    ##transition to next READY
    if obj.train_button.is_hovered():
      obj.mode = obj.TRAINING;
      obj.state = obj.READY
      obj.counter=obj.READY_COUNTER;
    elif obj.user_button.is_hovered():
      obj.mode=obj.USER
      obj.state = obj.READY;
      obj.counter = obj.READY_COUNTER;
  elif obj.state == obj.READY:
    ##if hovering SETUP: back to hovering
    ## if hovering PAUSE: pause
    ## if quit then quit: leave the game
    if obj.quit_button.is_hovered():
      obj.listen=False;
      done =True;
    elif obj.setup_button.is_hovered():
      obj.state = obj.SETUP;
    elif obj.puase_button.is_hovered():
      obj.paused = not obj.paused


  elif obj.state == obj.RECORDING:
    ##if hovering SETUP: back to hovering
    ## if hovering PAUSE: pause
    ## if quit then quit: leave the game 
    if obj.quit_button.is_hovered():
      obj.listen=False;
      done =True;
    if obj.setup_button.is_hovered():
      obj.state = obj.SETUP;
      obj.skeletal_map = [];
    elif obj.puase_button.is_hovered():
      obj.paused = not obj.paused
  elif obj.state == obj.WAIT:
    ##if hovering SETUP: back to hovering
    ## if hovering PAUSE: pause
    ## if quit then quit: leave the game 
    if obj.quit_button.is_hovered():
      obj.listen=False;
      done =True;
    if obj.setup_button.is_hovered():
      obj.state = obj.SETUP;
    if obj.puase_button.is_hovered():
      obj.paused = not obj.paused
  elif obj.state == obj.FEEDBACK:
    ##if hovering SETUP: back to hovering
    ## if hovering PAUSE: pause
    ## if quit then quit: leave the game e
    if obj.quit_button.is_hovered():
      obj.listen=False;
      done =True;
    if obj.setup_button.is_hovered():
      obj.state = obj.SETUP;
    if obj.puase_button.is_hovered():
      obj.paused = not obj.paused
  return done
def transition_handle(obj,background_color,skeleton_counter):
  if not obj.paused:
    if obj.state == obj.RECORDING:
      #print obj.skeletal_map
      if obj.counter<=0:
        with obj.screen_lock:
          obj.screen.fill(background_color)
        if not obj.skeletal_map==[]:
          obj.backend_data = deepcopy(obj.skeletal_map)
          print("")
          print("number of frames send:", len(obj.backend_data))
          print("number of frames recieved:", skeleton_counter);
          print("")
          skeleton_counter=0
          obj.skeletal_map = []
          obj.sent_data = True;
          if obj.mode==obj.USER:
            thread = myThread(obj.backend['get_classification'], obj);
          if obj.mode == obj.TRAINING:
            thread = myThread(obj.backend['save_sequence'], obj);

          thread.start()
        else:
          print("No data recieved")
          obj.sent_data = False
        if obj.mode == obj.TRAINING:
          obj.state = obj.READY;
          obj.counter=obj.READY_COUNTER;
          obj.test_word = obj.wordlist.roll()
        if obj.mode == obj.USER:
          obj.state = obj.WAIT;
          obj.state = obj.WAIT_COUNTER
        
      else:
        obj.counter-=1;

    ##waiting 
    elif obj.state==obj.WAIT:
      if not obj.backend_wait:
        with obj.screen_lock:
          obj.screen.fill(background_color)
        obj.state = obj.FEEDBACK;
        obj.counter = obj.FEEDBACK_COUNTER;
        obj.backend_wait=True;
      elif obj.counter<=0:
        with obj.screen_lock:
          obj.screen.fill(background_color)
        obj.state = obj.FEEDBACK
        obj.counter = obj.FEEDBACK_COUNTER;
        obj.word = "None";
        obj.backend_wait = True;

      else:
        obj.counter-=1;
    ##feedback state
    elif obj.state == obj.FEEDBACK:
      if obj.counter<=0:
        with obj.screen_lock:
          obj.screen.fill(background_color)
        obj.counter = obj.READY_COUNTER
        obj.state = obj.READY
        if not obj.repeat:
          obj.test_word=obj.wordlist.roll();
        obj.repeat=False;

      else:
        obj.counter-=1
    ## state READY->countdown to word 
    elif obj.state==obj.READY:
      if obj.counter<=0:
        with obj.screen_lock:
          obj.screen.fill(background_color)
        if obj.mode == obj.TRAINING:
          obj.state = obj.RECORDING;
          obj.counter = obj.RECORDING_COUNTER;
        if obj.mode == obj.USER:
          obj.state = obj.RECORDING
          obj.counter = obj.RECORDING_COUNTER
      else:
        obj.counter-=1;
def word_handle(obj,word,done):
  if word=="pause":
    print "pausing"
    obj.paused = True
  elif word == "quit":
    print "quitting"
    obj.listen = False
    done = True;
  elif word == "run":
    print "running"
    
    obj.paused=False
  elif word == "repeat":
    obj.repeat=True;
  return done

class myThread (threading.Thread):
  def __init__(self, funct, obj):
    threading.Thread.__init__(self)
    self.funct = funct
    self.obj = obj;
  def run(self):
    self.funct(self.obj)


