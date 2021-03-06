import topbar as bars
from copy import deepcopy
def setup_display_handler(obj):
  '''
  Handles displaying UI components in SETUP state
  ''' 
  obj.screen.blit(obj.topbar,obj.topbar_pos);
  obj.screen.blit(obj.setup_sidebar_surf,obj.side_bar_pos);
  obj.screen.blit(obj.setup_ctl_surf,obj.ctl_pose)




def ready_display_handler(obj):
  '''
  Handles displaying UI components in ready(count down) state
  '''
  if obj.mode==obj.TRAINING:
    word_bar = obj.train_bars[obj.test_word]
  else:
    word_bar = obj.test_bars[obj.test_word]
  obj.screen.blit(obj.topbar,obj.topbar_pos);
  obj.screen.blit(word_bar,obj.word_bar_pos);
  obj.screen.blit(obj.ctl_surf,obj.clt_words.pose)
  obj.screen.blit(obj.clock.draw(count=obj.counter),obj.clock_pos)
  obj.screen.blit(obj.sidebar_surf,obj.side_bar_pos);




def recording_display_handler(obj):
  
  if obj.mode==obj.TRAINING:
    word_bar = obj.train_bars[obj.test_word]
  else:
    word_bar = obj.test_bars[obj.test_word]
 
  gogo = obj.gogo_bar
  obj.screen.blit(gogo,obj.clock_pos)
  obj.screen.blit(obj.topbar,obj.topbar_pos);
  obj.screen.blit(obj.ctl_surf,obj.clt_words.pose)
  obj.screen.blit(word_bar,obj.word_bar_pos);
  obj.screen.blit(obj.sidebar_surf,obj.side_bar_pos);



def wait_display_handler(obj):
  obj.screen.blit(obj.topbar,obj.topbar_pos);
  obj.screen.blit(obj.sidebar_surf,obj.side_bar_pos);
  obj.screen.blit(obj.ctl_surf,obj.clt_words.pose)
  feed = obj.processing_bar
  obj.screen.blit(feed,obj.feedback_bar_pos);
def feedback_display_handler(obj):
  obj.screen.blit(obj.topbar,obj.topbar_pos);
  obj.screen.blit(obj.sidebar_surf,obj.side_bar_pos);
  if obj.sent_data:
    if obj.test_word==obj.word:
      ### Display congrats
      feed = obj.congrats_bar
      obj.screen.blit(feed,obj.feedback_bar_pos)

    else:
      ### Display sorry
      if obj.word=="None":
        feed =  obj.sorry_bar_mapper['aniga']
      else:
        feed =  obj.sorry_bar_mapper[obj.word[0]]#bars.sorry(obj.feedback_bar_size,obj.word,pos = obj.feedback_bar_pos)
      obj.screen.blit(feed, obj.feedback_bar_pos);
      feed_two = obj.correct_word_bar[obj.test_word];
      obj.screen.blit(feed_two, obj.correct_word_pos)
  else:
    feed= obj.no_data_bar
    obj.screen.blit(feed, obj.feedback_bar_pos);


def disp(obj):
  '''
  Maps states to display functions 
  '''
  if obj.state==obj.SETUP:
    setup_display_handler(obj)
  elif obj.state==obj.READY:
    ready_display_handler(obj)
  elif obj.state==obj.RECORDING:
    recording_display_handler(obj);
  elif obj.state==obj.WAIT:
    wait_display_handler(obj);
  elif obj.state==obj.FEEDBACK:
    feedback_display_handler(obj)
  else:
    print("illigal state!")