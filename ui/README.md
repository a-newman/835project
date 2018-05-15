## Quick UI reference 

### Integration(integration.py)
The entry class to the UI which defines the placements of all UI elements, handles timing, and displaying. Check `depth_frame_ready` , `video_frame_ready` and `draw_skeletons` functions for displaying things. Check [pygame display](https://www.pygame.org/docs/ref/display.html) and [Pygame Surface](https://www.pygame.org/docs/ref/surface.html) for more on creating windows and rendering sprites on them. 

The centerpiece of the UI. All the our files in this directory are helpers for this file. All the placements and the sizes of the UI display components are defined in the contructor of this class(the init function).

**Attributes**

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

**Methods**

- **collect**: Subscribes to the skeleton data from the Kinect 
- **draw_skeletons**: Draws the skeleton data on the screen 
- **word_trigger**: Speech call back function 
- **depth_frame_ready**: Display the depth, also calls the display functions from `disp_func.py`.
- **video_frame_ready**: Display the depth, also calls the display functions from `disp_func.py`.

### Event Handlers(event_handlers.py)
Implements the following functions for handling events.

**`mouse_handle`**

handles mouse clicks.
Parameters:
- **obj**: a pykinect integration object `PykinectInt` see `integration.py`
- **done**: Signal for the UI loop to exit when user clicks, set to **true** when the user clicks on the **quit** button.
   
See the following lines in `integration.py` on how it is called
```python 
if e.type ==MOUSEBUTTONDOWN:
  done=mouse_handle(self,done);
```

**`transition_handle`**

handles state transition and state events(timers). It is called by integration when timer event is triggered.
parameters:
- **obj**: a pykinect integration object `PykinectInt` see `integration.py`
- **background_color**: background color of the screen during the following state.
- **skeleton_counter**: Counts the number of skeleton messages recieved from the kinect so far, effective in **RECORDING** state only.

See the following lines in integration.py
```python 
elif e.type == RECORDEVENT:
  transition_handle(self,background_color,skeleton_counter)
```
**`word_handle`**

Handles speech events. 
parameters:
- **obj**: a pykinect integration object `PykinectInt` see `integration.py`
- **word**: The detected control word.
- **done**: **done**: Signal for the UI loop to exit when user clicks, set to **true** when the detected word is **quit**.

See the following lines in integration.py
```python
if e.type==SPEECHEVENT:
  while len(e.words)!=0:
    speech_word = e.words.pop(0)
    done = word_handle(self,speech_word,done)
```

### Sidebar(sidebar.py)

Contains the class, **Sidebar**, that impelements the sidebar that displays the control button. 
```python
class Sidebar:
```
A class that implements the side bar where buttons are displayed on.

**parameters**

- **(w,h)**: dimensions of the surface bounding the bar 
- **pos**: position of the bar in the display window
- **buttons**: list of buttons to display

**methods** 

- **draw_buttons**: draws the buttons on the bar surface 
- **get_button_pos**: gets position of button with given in index in the list of buttons
- **button_update**: reinitializes a given button

### bars(topbar.py)

The implements the bars that display is the project name, action word, feedback, etc.

### Speech detection(speech_detection.py)

The speech recognition modules. It uses Python's [Speech Recognition]() library with the [Google Web API Speech recogition Engine]() for backend. The file implements the following classes.
```python
class SpeechRecog:
```

A class that encapsolutes speech reocognition.

**attributes**

- **obj**: PyKinect integration object PyKinectInt
- **r**: recognizer obj, see the speech reocognition

**methods**

- **run**: speech recogntion loop method
- **is_word_text**: True if the given word is in the detected speech.
- **word_search**: search word in speech
-  **detect**: speech recognition calls this function to search the control words.

### Data Utils(data_utils.py)
Implements the data structure that defines the skeleton data sent to the backend. 
```python
class Skeletal:
```
A class that defines a skeleton as a list of joint positins

**parameters**
- **head**, **spine**, **shoulders**, etc: each as a single 3d position.
methods:
- **is_not_empty**: true if not all coordinates are zero.

```python
class ScanFrame:
```
A class that defines a frame, list of skeletons detected by the Kinect at once.

**parameters**
- **skeletons**: The list of skeletal objects

### Control Words(control_words.py)

Implements the surface that displays control(speech recognition) words.

### Text(text.py)
Contains a class that implements a text box for the user to type in words.
```python
class InputBox:
```
 class that defines a text box as Pygame surface

**parameters**

- **(w,h)**: dimensions of the box
- **(x,y)**: coordinates(position of the box) in the display window.
  
**methods**
- **handle_event**: handles keyboard and mouse events(e.g. user type a new word) 
- **update**: changes the width of the box for long text 
- **draw**: renders the text box on the input screen.

### UI utils 

Implements helper classes and functions. The following are the more relevant ones.
```python
class CircularArray:
```
 Defines a circular array class.

  **attributes**

  - **arr**: A python list containing the elements of the Array
  
  **Methods**

  - **roll**: pops the first element from the list(arr), appends to the end of the list(arr), and return that element.
  - **randRoll**: pops a random element from the list(arr), appends it to the end of the list(arr), and returns that element 

```python
class Clock:
```
a class that defines the count down clock.

**attributes**

- **size**: dimensions of the surface containing the clock
- **in_img**: Path to the image containing the back clock
- **out_img**: Path to save the image to when resized

**methods**
- g**et_image**: resizes and returns the resized input image
- **get_diagnol**: returns the diagnol of the rectangle with the dimensions of this surface
- **draw**: does the local rendering and returns the final surface.

### Button(button.py)
Contains the following class.
```python
class Button:
```
A class that defines a clickable button as Pygame surface.

**attributes**
- **dims**: Button dimensions
- **pos**: Position of the display Window
- **text**: The libel of the Button
  
**methods**

- **set_font_size**: Fits the text into the bounding box of the Button
- **se_font_color**: Changes the font color
- **reinitialize**: reinializes the button class
- **is_hovered**: True if the mouse is hovering the button
- **show**: Does the internal rendering calls and returns the button as Pygame surface
- **set_dims**: sets the dimensions of the button to the new dimensions passed into this  method

### Word display map(word_display_map.py)

Contains functions to pre-determine and pre-render the control words surfaces. Each of them returns a dictory mapping words to pygame surfaces. Since these surfaces are determined using the button class above, it is computationally expensive to re-render them each turn of the loop so this helper functions help us pre-determine the surfaces.
