import pygame
from displayState import Idle, Setup, Start, Wait, Feedback
import start_state_logic 
import 
class WordGameUI:
  IDLE = 0;
  SETUP = 1;
  START = 2;
  RECORDING = 3;
  PROCESSING = 4
  FEEDBACK=5;
  def __init__(self, hieght=64, width = 64):
    self.h = hieght
    self.w =  width
    self.state = self.IDLE;
  def display_logic():

    if self.state == self.IDLE:
      self.idle()

    elif self.state == self.SETUP:
      self.setup()

    elif self.state == self.START:
      self.start()

    elif self.state == self.RECORDING:
      self.recording()

    elif self.state == self.PROCESSING:
      self.processing()

    elif self.state == self.FEEDBACK:
      self.feedback()

  def idle(self):
    '''
    1. show the IDLE state game display
      - Plain page with a nice back ground
      - Has a big bottom that says "start setup"
    2. Do the state transition to SETUP when appropriate
      - If the button is clicked transition to SETUP
      - otherwise stay IDLE
    '''
    #TODO
    pass 
  def setup(self):
    '''
    1. Display the SETUP user interface
      - plain page with a nice back ground 
      - has big button start says "start"
      - Contains a quick instruction on what happens after button click
      - dropdown menu for choosing countdown to performing the actions
    2. Make the transition to START when appropriate
      - If button is clicked transition to START
      - otherwise stay SETUP
    '''
    #TODO
    pass
  def start(self):
    '''
    1. show the START state game display
      - show the countdown clock for starting the action performance
      - Button for going back to setup
      - The word to be performed 
    2. Make the appropriate state transitions
      - If the "back" button is clicked, transition to setup
      - if the countDown expires Go to WAIT
      - otherwise state START
    3. Make the appropriate backend calls 
      - When countdown expires tell the backend to handle recording 
    '''
    pass 
  def recording(self):
    '''
    1. Show the RECORDING state display
      - plain page showing a recording symbol
    2. Make the appropriate transitions
      - Wait for a notification from backend indicating end of recording
      - When the notification arrives, transition to PROCESSING
    '''
    #TODO
    pass
  def processing(self):
    '''
    1. Show the PROCESSING state display
      - plain page showing a processing symbol
    2. Make the correct state transitions
      - Waiting a call from the backend with a result 
      - When the result arrives go to FEEDBACK
    '''
  def feedback(self):
    '''
    1. Display the feedback to the user
      - Display the result of the evaluation 
      - Display fireworks if evaluation returns true
    2. Make the appropriate state transitions
      - When feedback giving is done- go to START
    '''
    #TODO
    pass 
def options():
  #TODO
  pass 
if __name__=="__main__":
  args = options()
  game = WordGameUI(args);
  game.display_logic()