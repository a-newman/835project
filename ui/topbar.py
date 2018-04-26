from button import Button 
import pygame
from pygame.color import THECOLORS
import random as rn;

def topBar(size,pos=(0,0)):

  bar = Button(dims=size,text = "Louder than words");
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

def congrats(size,pos = (0,0)):
  bar =  Button(dims=size,text = "Congratulations! You got it!");
  bar.pos = pos;
  bar.back_color_n = (12,12,55);
  bar.back_color_h = (3,32,11);
  bar.font_color = (2,255,3);
  return bar.show();
def sorry(size,word,pos = (0,0)):
  bar =  Button(dims=size,text = "Sorry! You have performed: "+word);
  bar.pos = pos;
  bar.back_color_n = (12,12,55);
  bar.back_color_h = (3,32,11);
  bar.font_color = (88,4,3);
  return bar.show();
def processing(size,pos = (0,0)):
  bar =  Button(dims=size,text = "processing...");
  r= rn.randint(0,255);
  g = rn.randint(0,255);
  bar.pos = pos;
  bar.back_color_n = (12,12,55);
  bar.back_color_h = (3,32,11);
  bar.font_color = (r,g,3);
  return bar.show();
def noData(size,pos = (0,0)):
  bar =  Button(dims=size,text = "No Data collected!");
  bar.pos = pos;
  bar.back_color_n = (12,12,55);
  bar.back_color_h = (3,32,11);
  bar.font_color = (88,4,3);
  return bar.show();
def gogo(size,pos = (0,0)):
  bar =  Button(dims=size,text = "GO!");
  bar.pos = pos;
  bar.back_color_n = (12,12,55);
  bar.back_color_h = (3,32,11);
  bar.font_color = (88,4,3);
  return bar.show();



