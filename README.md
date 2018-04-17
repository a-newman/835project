### Proposed UI-Backend interfacing 
The backend provides the following.
1. A pre-trained Model
2. A function that takes a time interval(in seconds) and a model,  collects the data for that time interval, uses the model to classify the gesture, and finally returns a score for the performed gesture. 
The UI is responsible for 
1. Loading the model 
2. Determing the time interval for the user gesture performances to be recorded
3. Calling the backend to collect the data with the interval

### BackEnd TODO: 
- [ ] Normalize frames from the Kinect by position (set x, y, z to 0)? 
- [ ] Normalize by shoulder width? 
- [ ] Consider not using feet cause they seem super noisy
- [ ] More robust data collection. Super noisy rn. 



### FrontEnd TODO:
- [ ] Add the backEnd interfacing 
- [ ] Fix the display timing issues with recording and processing states
- [ ] Add droping dopdown menu for a countdown to the user performing the action
- [ ] Making things look nice(they look unpleasant now) 
- [ ] Maybe pygame is too much work for the long run(doesn't even have buttons), could experiment with wxPython.
- [ ] Setup the recording and processing timers 

## Running the UI
If you may need to install Pygame
`pip install pygame` do should it 

Change directory to *ui* and run `python gameUI.py`

Keep clicking the buttons to advance 

For recording and processing states just click on the text to advance for now.

### Prototype Feedback

Timing issues 
1. Waiting before action is too long 
2. Recording time is too long
Add more modes to the UI(Let me signal when ready to perform)
1. Clicker(probably not hard to add)
2. Speech (1) be careful with background noise given the distance from the screen (2) You could get the computer closer and use the computer's microphone for speech detection.
3. Gesture 
Confusing things
1. What’s the countdown for?
2. Why is it defualting to waving? Need none-of-the-above prediction
You could add 
1. More control over the words to be shown (1) Could go back to previous words (2) Could pause and start whenever (3) Let me choose the word
3. Add a mode where you keep doing the action until you get it or get tired of it(signal pass).
4. Could add demo window(pre-recorded video?)




