## Quick UI reference 

### Integration(integration.py)
The entry class to the UI which defines the placements of all UI elements, handles timing, and displaying. Check `depth_frame_ready` , `video_frame_ready` and `draw_skeletons` functions for displaying things. Check [pygame display](https://www.pygame.org/docs/ref/display.html) and [Pygame Surface](https://www.pygame.org/docs/ref/surface.html) for more on creating windows and rendering sprites on them. 

The centerpiece of the UI. All the our files in this directory are helpers for this file. All the placements and the sizes of the UI display components are defined in the contructor of this class(the init function).

##### Attributes 
* **screen**: The pygame display window;
* **screen_lock**: The pygame display lock for preventing threading from doing simoultaneous renderning.
* **draw_skeleton**: If **true** skeletons will be displayed on the screen. 
* **video_display**: If **true** RGB will be displayed on the screen.
* **dispInfo**: Current window dimensions
* **skeleton_to_depth_image**: skeleton to 2d depth convertor method
* control_words**: List of speech words for controlling the dispaly
* **paused**: if **true** the control flow is paused, clocks stop.
* **skeletons**: Holds the recieved skeletons for the backend and displaying 
* **self.skeletal_map**: List of processed skeletons to be sent to the backend for storing and classifications.
* **state**: The state of the game. Takes one of **SETUP**,**READY**,**RECORDING**,**WAIT**,**FEEDBACK**. In **SETUP** is state the game is waiting for the user to select mode, in **READY** the game is countdown for the user to get ready for the next action, in **RECORDING** the user performs the action and the game records,in **WAIT**(only in testing mode) the UI is waiting for the backend end to respond with a classification result, and finally in **FEEDBACK**(only in test mode) the UI tells the user wether they got the word right or not.
* **mode**: Mode of the game. Inlcuding the project supports two, modes **TRAINING**(practice or training mode) and **USER**(test mode).
* **backend**: Backend or classification information for calling when the skeleton data is collected.
* **wordlist**: List of foreign langauge words as Circular Array object. The words are currently from the backend. 
* **word**: The word returned by the backend for classification.
* **test_word**: The word displayed to the user.
* **backend_wait**: If **true** wait for the backend to return classification.
* **show_depth**: If **true** the depth data from the Kinect is displayed.
* **use_speech**: If **true** speech is used for controller the state transitions.
* **repeat**: If **true** the system shows the last word again.
* **camera_surf**: The pygame surface where all kinect feeds(depth, video, and skeleton) are displayed on when enabled.
* **counter**: State life time counter. 
* **mergin_side**: is of the screen side mergins, space between where things are drawn and where the edge of the display window on the sides.
* **mergin_top**: top and bottom screen mergins.
* **top_bar_size**: size(width, height) of the bar that displays the name(Louder than Words).
* **topbar_pos**: The location of the bar that displays the name(Louder than words).
* **side_bar_w**: Width of the sidebar where control buttons are displayed on.
* **side_bar_h**: Height of the sidebar where control buttons are displayed on.
* **side_bar_pos**: The position of the sidebar where control buttons are displayed on.
* **word_bar_size**: The size of the bar that displays the action word. 
* **word_bar_pos**: The position of the bar that displays the action word.
* **camera_feed_pos**: Position of the camera feed window. 
* **text_in_h**, **text_in_w**, **text_in_pos**: The height, width, and the position of the text box. The box where the user would enter the words.
* **clock_pos**: The position of the count down clock.
* **feedback_bar_pos** and **feedback_bar_size**: The position and size of the feedback back bar.
* **listen**: If **false** the speech thread exits. The UI will no longer recieve speech events.
* **ctl_word_size**, **ctl_pose**,and **ctl_size**: the font size, position, and dimensions of the control words bar.


### Event Handlers(event_handlers.py)
Implements the following functions for handling events.

`mouse_handle`
handles mouse clicks.
Parameters:
- **obj**: a pykinect integration object `PykinectInt` see `integration.py`
- **done**: Signal for the UI loop to exit when user clicks, set to **true** when the user clicks on the **quit** button.
   
See the following lines in `integration.py` on how it is called
  >> if e.type ==MOUSEBUTTONDOWN:
  >>   done=mouse_handle(self,done);
 

`transition_handle`
  handles state transition and state events(timers). It is called by integration when timer event is triggered.
parameters:
- **obj**: a pykinect integration object `PykinectInt` see `integration.py`
- **background_color**: background color of the screen during the following state.
- **skeleton_counter**: Counts the number of skeleton messages recieved from the kinect so far, effective in **RECORDING** state only.

See the following lines in integration.py
  >> elif e.type == RECORDEVENT:
  >>  transition_handle(self,background_color,skeleton_counter)

word_handle(obj,word,done):
Handles speech events. 
parameters:
- **obj**: a pykinect integration object `PykinectInt` see `integration.py`
- **word**: The detected control word.
- **done**: **done**: Signal for the UI loop to exit when user clicks, set to **true** when the detected word is **quit**.

See the following lines in integration.py
  >>if e.type==SPEECHEVENT:
  >>  while len(e.words)!=0:
  >>     speech_word = e.words.pop(0)
  >>     done = word_handle(self,speech_word,done)


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
