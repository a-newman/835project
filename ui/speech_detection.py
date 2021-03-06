######Detecting word 
import threading
import re
import speech_recognition as sr
class SpeechRecog:
  '''
  A class that encapsolutes speech reocognition.
  attributes
  - obj: PyKinect integration object PyKinectInt
  - r: recognizer obj, see the speech reocognition
  methods
  - run: speech recogntion loop method
  - is_word_text: True if the given word is in the detected speech.
  - word_search: search word in speech
  - detect: speech recognition calls this function to search the control words.
  '''
  def __init__(self, game_obj=None):
    self.obj = game_obj;
    self.r = sr.Recognizer()
    self.r.energy_threshold = 1000
    self.r.non_speaking_duration=0.008
    self.r.pause_threshold = 0.008
  def run(self):
    while self.obj.listen:
      with sr.Microphone(1) as source:
        #self.r.adjust_for_ambient_noise(source)
        audio = self.r.listen(source,duration=2)
      try:
          text = self.r.recognize_google(audio, language='en-US')
          print("detected: ",text)
          self.detect(text);
          
      except sr.UnknownValueError:
          for index, name in enumerate(sr.Microphone.list_microphone_names()): 
            #print("mike found: " + str(index) + " " + name)
            pass
          print("I can't hear you! Speak louder!")
      except sr.RequestError as e:
          print("Could not request results from Google Speech Recognition service; {0}".format(e))
  def is_word_in_text(self,w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search
  def word_search(self,speech):
    detected_words = []
    for word in self.obj.control_words:
      detect_word = self.is_word_in_text(word.lower())(speech.lower());
      if detect_word!=None:
        detected_words.append(word);
    return detected_words


  def detect(self, speech):
    detected_words = self.word_search(speech);
    if detected_words!=[]:
      print "posting", detected_words
      self.obj.word_trigger(detected_words);
class SpeechTrigger(threading.Thread):
  def __init__(self,obj):
    threading.Thread.__init__(self)
    self.obj = obj;
  def run(self):
    speech_detection = SpeechRecog(game_obj=self.obj);
    speech_detection.run();