import topbar as bars
from copy import deepcopy
def setup_display_handler(obj):
  ##display two buttons 
  obj.screen.blit(obj.topbar,obj.topbar_pos);
  obj.screen.blit(obj.setup_sidebar_surf,obj.side_bar_pos);
  obj.screen.blit(obj.ctl_surf,obj.ctl_pose)
def ready_display_handler(obj):
  #word_bar = bars.wordBar(obj.word_bar_size,obj.test_word,pos=obj.word_bar_pos)
  if obj.mode==obj.TRAINING:
    word_bar = bars.wordBar(obj.word_bar_size,obj.test_word[0]+" ("+obj.test_word[1]+")",pos=obj.word_bar_pos)
  else:
    word_bar = bars.wordBar(obj.word_bar_size,obj.test_word[0],pos=obj.word_bar_pos)
  obj.screen.blit(obj.topbar,obj.topbar_pos);
  obj.screen.blit(word_bar,obj.word_bar_pos);
  obj.screen.blit(obj.ctl_surf,obj.clt_words.pose)
  obj.screen.blit(obj.clock.draw(count=obj.counter),obj.clock_pos)
  obj.screen.blit(obj.sidebar_surf,obj.side_bar_pos);
def recording_display_handler(obj):
  # word_bar = bars.wordBar(obj.word_bar_size,obj.test_word,pos=obj.word_bar_pos)
  if obj.mode==obj.TRAINING:
    word_bar = bars.wordBar(obj.word_bar_size,obj.test_word[0]+"("+obj.test_word[1]+")",pos=obj.word_bar_pos)
  else:
    word_bar = bars.wordBar(obj.word_bar_size,obj.test_word[0],pos=obj.word_bar_pos)
  #gogo = bars.gogo(obj.DEPTH_WINSIZE,pos=obj.clock_pos);
  gogo = bars.gogo(size=(obj.clock.size, obj.clock.size),pos=obj.clock_pos);
  obj.screen.blit(gogo,obj.clock_pos)
  obj.screen.blit(obj.topbar,obj.topbar_pos);
  obj.screen.blit(obj.ctl_surf,obj.clt_words.pose)
  obj.screen.blit(word_bar,obj.word_bar_pos);
  obj.screen.blit(obj.sidebar_surf,obj.side_bar_pos);
  ##########Recording simple
def wait_display_handler(obj):
  obj.screen.blit(obj.topbar,obj.topbar_pos);
  obj.screen.blit(obj.sidebar_surf,obj.side_bar_pos);
  obj.screen.blit(obj.ctl_surf,obj.clt_words.pose)
  feed = bars.processing(obj.feedback_bar_size,pos = obj.feedback_bar_pos)
  obj.screen.blit(feed,obj.feedback_bar_pos);
def feedback_display_handler(obj):
  obj.screen.blit(obj.topbar,obj.topbar_pos);
  obj.screen.blit(obj.sidar_bar.draw_buttons(),obj.side_bar_pos);
  if obj.sent_data:
    if obj.test_word==obj.word:
      ### Display congrats
      feed = bars.congrats(obj.feedback_bar_size,pos = obj.feedback_bar_pos);
      obj.screen.blit(feed,obj.feedback_bar_pos)

    else:
      ### Display sorry
      feed =  bars.sorry(obj.feedback_bar_size,obj.word,pos = obj.feedback_bar_pos)
      obj.screen.blit(feed, obj.feedback_bar_pos);
  else:
    feed= bars.noData(obj.feedback_bar_size,pos = obj.feedback_bar_pos);
    obj.screen.blit(feed, obj.feedback_bar_pos);
def disp(obj):
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