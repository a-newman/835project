
'''
Handles events and maps them their control functions 
All the functions in this file called from the loop function in integration.py
'''
import threading
from copy import deepcopy
def mouse_handle(obj,done):
  '''
  handles mouse clicks. 
  See the following lines in integration.py on how it is called
  >> if e.type ==MOUSEBUTTONDOWN:
  >>   done=mouse_handle(self,done);
  '''
  # Handle Depth button clicks 
  if obj.depth_button.is_hovered():
    obj.show_depth=not obj.show_depth

  #Handle button clicks in the Setup state
  if obj.state==obj.SETUP:
    if obj.train_button.is_hovered():
      obj.mode = obj.TRAINING;
      obj.state = obj.READY
      obj.counter=obj.READY_COUNTER; 
      obj.paused = False

    elif obj.user_button.is_hovered():
      obj.mode=obj.USER
      obj.state = obj.READY;
      obj.counter = obj.READY_COUNTER;
      obj.paused = False

  ## Handles button clicks in the ready(count down clock) state
  elif obj.state == obj.READY:
    if obj.quit_button.is_hovered():
      obj.listen=False;
      done =True;

    elif obj.setup_button.is_hovered():
      obj.state = obj.SETUP;

    elif obj.puase_button.is_hovered():
      obj.paused = not obj.paused

  ## Handle button clicks in the recording(GO) state
  elif obj.state == obj.RECORDING:
    if obj.quit_button.is_hovered():
      obj.listen=False;
      done =True;

    if obj.setup_button.is_hovered():
      obj.state = obj.SETUP;
      obj.skeletal_map = [];

    elif obj.puase_button.is_hovered():
      obj.paused = not obj.paused

  #Handle button clicks in Wait(PROCESSING) state
  elif obj.state == obj.WAIT:
    if obj.quit_button.is_hovered():
      obj.listen=False;
      done =True;

    if obj.setup_button.is_hovered():
      obj.state = obj.SETUP;

    if obj.puase_button.is_hovered():
      obj.paused = not obj.paused
  ## Handle feedback state button clicks
  elif obj.state == obj.FEEDBACK:
    if obj.quit_button.is_hovered():
      obj.listen=False;
      done =True;
    if obj.setup_button.is_hovered():
      obj.state = obj.SETUP;
    if obj.puase_button.is_hovered():
      obj.paused = not obj.paused
  return done
def transition_handle(obj,background_color,skeleton_counter):
  '''
  handles state transition and state events(timers). It is called by integration when timer event is triggered.
  See the following lines in integration.py
  >> elif e.type == RECORDEVENT:
  >>  transition_handle(self,background_color,skeleton_counter)
  '''
  if not obj.paused: ## Time events are not handles when game is puased
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

    ##Processing state
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
  '''
  Handles speech events. See the following lines in integration.py 
  >>if e.type==SPEECHEVENT:
  >>  while len(e.words)!=0:
  >>     speech_word = e.words.pop(0)
  >>     done = word_handle(self,speech_word,done)
  '''
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
  if obj.state==obj.SETUP:
    if word=="test":
      obj.mode = obj.USER
      obj.state = obj.READY
      obj.counter=obj.READY_COUNTER;
      # turn pause off 
      obj.paused = False
    if word=="train":
      obj.mode = obj.TRAINING
      obj.state = obj.READY
      obj.counter=obj.READY_COUNTER;
      # turn pause off 
      obj.paused = False
  return done

class myThread (threading.Thread):
  '''
  Runs the backend in the back ground so the rendering doesn't get intrupted
  '''
  def __init__(self, funct, obj):
    threading.Thread.__init__(self)
    self.funct = funct
    self.obj = obj;
  def run(self):
    self.funct(self.obj)


