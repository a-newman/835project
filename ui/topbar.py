from button import Button 
import pygame
from pygame.color import THECOLORS

def topBar(size,pos=(0,0)):

  bar = Button(dims=size,text = "Loader than Word");
  bar.pos = pos
  bar.back_color_n = (129,120,13);
  bar.back_color_h = (129,120,13);
  bar.font_color = THECOLORS["white"];
  return bar.show();
def wordBar(size,word,pos=(0,0)):
  bar = Button(dims=size,text = "word: "+word);
  bar.pos = pos;
  bar.back_color_n = (12,12,155);
  bar.back_color_h = (32,32,115);
  bar.font_color = (255,255,12);
  return bar.show();
