import topbar as bars
def trainer_vocab_display_mapper(obj):
  disp_word_map = {}
  for word in obj.wordlist.arr:
    word_bar = bars.wordBar(obj.word_bar_size,word[0]+"("+word[1]+")",pos=obj.word_bar_pos)
    disp_word_map[word] = word_bar
  return disp_word_map
def test__vocab_display_mapper(obj):
  disp_word_map = {}
  for word in obj.wordlist.arr:
    word_bar = bars.wordBar(obj.word_bar_size,word[0],pos=obj.word_bar_pos)
    disp_word_map[word] = word_bar
  return disp_word_map
def sorry_bar_mapper(obj):
  disp_word_map = {}
  for word in obj.wordlist.arr:
    word_bar = bars.sorry(obj.feedback_bar_size,word[0]+"("+word[1]+")",pos = obj.feedback_bar_pos)
    disp_word_map[word[0]] = word_bar
  return disp_word_map
def correct__word_display_mapper(obj):
  disp_word_map = {}
  for word in obj.wordlist.arr:
    word_bar = bars.correct_word_bar(obj.feedback_bar_size,word[0]+"("+word[1]+")",pos=(obj.feedback_bar_pos[0],obj.feedback_bar_pos[1]+obj.feedback_bar_size[1]))
    disp_word_map[word] = word_bar
  return disp_word_map

