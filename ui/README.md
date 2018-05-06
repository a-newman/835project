## Quick UI reference 

### Integration(integration.py)
The entry class to the UI which defines the placements of all UI elements, handles timing, and displaying. Check `depth_frame_ready` , `video_frame_ready` and `draw_skeletons` functions for displaying things. Check [pygame display](https://www.pygame.org/docs/ref/display.html) and [Pygame Surface](https://www.pygame.org/docs/ref/surface.html) for more on creating windows and rendering sprites on them.  

### Event Handlers(event_handlers.py)
Implements a few functions that handle events including mouse clicks(mainly for acitivating buttons), timer events(by the `stransition_handle` function), and speech events(currently disabled). All those functions are activated in the `integration.py` `loop` function. 

### Sidebar(sidebar.py)
Implements the sidebar that contains the control functions(e.g. SETUP). check the following lines of code in `integration.py` on how they are used. 

```
self.setup_sidebar = Sidebar(self.side_bar_pos,w=self.side_bar_w,h=self.side_bar_h,buttons=[self.train_button,self.user_button,self.depth_button])
self.setup_sidebar_surf = self.setup_sidebar.draw_buttons()
```
and 
```
self.sidar_bar = Sidebar(self.side_bar_pos,w=self.side_bar_w,h=self.side_bar_h,buttons=[self.quit_button,self.puase_button,self.setup_button,self.depth_button])
    self.sidebar_surf = self.sidar_bar.draw_buttons()
```

Those instances are used in `disp_func.py` for displaying elements at different states of the control flow.

### bars(topbar.py)
Impelements that bars that display the words and the feedback. Check the following lines of code in `integration.py` and `disp_func.py` on initializing them.

- In `integration.py`
```
###top bar
self.top_bar_size = (self.dispInfo.current_w-2*self.mergin_side,70);
self.topbar_pos = (self.mergin_side,self.mergin_side)
self.topbar = bars.topBar(self.top_bar_size,pos=self.topbar_pos);
```
- In `disp_func.py`. Note: The following are probably responsible for the laggying(they are responsible for calling `set_font_size` alot). 
```
if obj.mode==obj.TRAINING:
    word_bar = bars.wordBar(obj.word_bar_size,obj.test_word[0]+"("+obj.test_word[1]+")",pos=obj.word_bar_pos)
  else:
    word_bar = bars.wordBar(obj.word_bar_size,obj.test_word[0],pos=obj.word_bar_pos)
  #gogo = bars.gogo(obj.DEPTH_WINSIZE,pos=obj.clock_pos);
  gogo = bars.gogo(size=(obj.clock.size, obj.clock.size),pos=obj.clock_pos);
```
```
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
```


### Speech detection(speech_detection.py)

### 

### Data Utils(data_utils.py)

### Control Words(control_words.py)

### Text(text.py)

### 
