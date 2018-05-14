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
    self.mode = self.TRAINING;
    self.backend = backend;
    self.wordlist = CircularArray(backend['words'])
    self.word = "None"
    self.test_word = self.wordlist.roll()
    self.backend_wait = True;
    self.show_depth = False;
    ####
    if self.video_display:
      size = self.dispInfo.current_w-self.VIDEO_WINSIZE[0];
    else:
      size = self.dispInfo.current_w-self.DEPTH_WINSIZE[0];
    size = size + 100
    #self.clock_image = resize((size,size), ou_img="ui/images/_clock.gif");
    self.sent_data = False;
    self.use_speech = True;
    self.repeat = False
    self.camera_surf = pygame.Surface(self.DEPTH_WINSIZE)
    
    
    ##########
    self.counter = self.READY_COUNTER;
    self.action = Text(self.screen,w=100, h=50,pos=(485,0),text=self.test_word[0],color=THECOLORS['white']);
    self.count = Text(self.screen,w=100, h=100,pos=(485,55),text=str(self.counter),color=THECOLORS['white']);

    ####general state display paramters
    self.mergin_side = 20;
    self.mergin_top = 20;
    ###top bar
    self.top_bar_size = (self.dispInfo.current_w-2*self.mergin_side,70);
    self.topbar_pos = (self.mergin_side,self.mergin_side)
    self.topbar = bars.topBar(self.top_bar_size,pos=self.topbar_pos);
    ###side bar
    self.side_bar_w = 100;
    self.side_bar_h = self.dispInfo.current_h-self.mergin_top*2-self.top_bar_size[1];
    self.side_bar_pos = (self.mergin_side,self.top_bar_size[1]+self.mergin_top);
    ###word bar
    w = self.dispInfo.current_w-self.side_bar_w-2*self.mergin_side
    self.word_bar_size = (w,70);
    self.word_bar_pos = (self.mergin_side+self.side_bar_w,self.mergin_side+self.top_bar_size[1])
    
    ###camera feedback pos
    self.camera_feed_pos = (self.mergin_side+self.side_bar_w,self.word_bar_pos[1]+self.word_bar_size[1]);
    ####SETUP display parameters
    self.train_button_pos = (100,100);
    self.train_button = Button(pos=self.train_button_pos,text="TRAINING");
    #++++++++++
    self.user_button_pos = (100,210);
    #++++++++
    self.depth_button = Button(text="DEPTH")
    #++++++
    self.user_button = Button(pos=self.user_button_pos,text="USER");
    self.setup_sidebar = Sidebar(self.side_bar_pos,w=self.side_bar_w,h=self.side_bar_h,buttons=[self.train_button,self.user_button,self.depth_button])
    self.setup_sidebar_surf = self.setup_sidebar.draw_buttons()

    ###Text input
    self.text_in_h = 40;
    self.text_in_w = 100;
    self.text_in_pos = (self.camera_feed_pos[0]+self.DEPTH_WINSIZE[0]+10,self.camera_feed_pos[1])
    self.text_input = InputBox(self.text_in_pos[0], self.text_in_pos[1], self.text_in_w, self.text_in_h)
    ####READY display parameters
    self.quit_button = Button(text="QUIT");
    #++++++++++
    self.setup_button = Button(text="SETUP");
    #++++++
    self.puase_button = Button(text="PAUSE");
    #++++++

    self.sidar_bar = Sidebar(self.side_bar_pos,w=self.side_bar_w,h=self.side_bar_h,buttons=[self.quit_button,self.puase_button,self.setup_button,self.depth_button])
    self.sidebar_surf = self.sidar_bar.draw_buttons()
    #++++++
    #self.clock_pos = (self.camera_feed_pos[0]+self.DEPTH_WINSIZE[0]+10,self.camera_feed_pos[1]+self.text_in_h)
    self.clock_pos = (self.camera_feed_pos[0]+self.DEPTH_WINSIZE[0]+70,self.camera_feed_pos[1])
    self.clock = Clock(size=self.DEPTH_WINSIZE[1] + 30);
    ####RECODRING display parameters 
    

    ####FEEDBACK parameters
    self.feedback_bar_pos=(self.word_bar_pos[0], self.camera_feed_pos[1]+self.DEPTH_WINSIZE[1]+10);
    self.feedback_bar_size = self.word_bar_size;


    
   
    self.speech_thread = SpeechTrigger(self);
    self.listen = False;
    ###
    self.ctl_word_size = 40;
    self.ctl_pose = self.camera_feed_pos[0],self.camera_feed_pos[1]+self.DEPTH_WINSIZE[1]+30
    self.ctl_size = self.word_bar_size[0],300
    self.clt_words=ControlWords(self.WORDS,font_size=self.ctl_word_size,pose=self.ctl_pose,size=self.ctl_size)
    self.setup_clt_words=ControlWords(self.SETUP_WORDS,font_size=self.ctl_word_size,pose=self.ctl_pose,size=self.ctl_size)
    self.ctl_surf = self.clt_words.show()
    self.setup_ctl_surf=self.setup_clt_words.show()

    ### Feedback bars
    self.congrats_bar = bars.congrats(self.feedback_bar_size,pos = self.feedback_bar_pos);
    self.no_data_bar = bars.noData(self.feedback_bar_size,pos = self.feedback_bar_pos);
    self.processing_bar = bars.processing(self.feedback_bar_size,pos = self.feedback_bar_pos)
    self.gogo_bar = bars.gogo(size=(self.clock.size, self.clock.size),pos=self.clock_pos);
    self.correct_word_pos = (self.feedback_bar_pos[0],(self.feedback_bar_pos[1]+self.feedback_bar_size[1]))
    ####Test words
    self.train_bars = mappers.trainer_vocab_display_mapper(self);
    self.test_bars = mappers.test__vocab_display_mapper(self);
    self.sorry_bar_mapper = mappers.sorry_bar_mapper(self);
    self.correct_word_bar = mappers.correct__word_display_mapper(self);
##### Methods 

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
