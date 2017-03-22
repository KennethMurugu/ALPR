# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 11:57:22 2016

@author: Kenneth
"""

from PIL import Image, ImageTk
from constants.alprconstants import CANVAS_WIDTH, CANVAS_HEIGHT
import os

cwd = os.getcwd()
"""
Will hold all constant image rsources; load images selected from the UI
"""
MAIN_BG = Image.open(cwd+'\\resources\\img\\alpr-main-bg.png')
CANVAS_BG = Image.open(cwd+'\\resources\\img\\canvas-bg.png')
FRAMELIST_BG = Image.open(cwd+'\\resources\\img\\listbox-bg.png')
BTN_BG_DEFAULT = Image.open(cwd+'\\resources\\img\\btn-bg-default.png')

"""
def PreloadImages():
    #image constants
    global MAIN_BG, CANVAS_BG, FRAMELIST_BG, BTN_BG_DEFAULT
    try:
        MAIN_BG = Image.open(cwd+'\\resources\\img\\alpr-main-bg.png')
        CANVAS_BG = Image.open(cwd+'\\resources\\img\\canvas-bg.png')
        FRAMELIST_BG = Image.open(cwd+'\\resources\\img\\listbox-bg.png')
        BTN_BG_DEFAULT = Image.open(cwd+'\\resources\\img\\btn-bg-default.png')
        return True
    except IOError:
        return False
"""
    
"""
Helper method to load user-selected images onto canvas
-path: absolute path to image
"""
def loadImage(path, canvas_w, canvas_h, Resize=True):
    #load image from given path
     img = Image.open(path)
     #determine if image res is equal to canvas res 
     if Resize:
         isNotEqual = resNotEqual(img.height, img.width, canvas_w, canvas_h) 
         #if true, resize to canvas res
         
         if (isNotEqual):
             print "NOT EQUAL"
             resized = img.resize((int(canvas_w),int(canvas_h)),
                                   Image.ANTIALIAS)
             return (ImageTk.PhotoImage(resized), "RESIZED")         
             
         else:
             return (ImageTk.PhotoImage(img), "NORMAL")
             
     else:
         return (ImageTk.PhotoImage(img), "NORMAL")      
             
             
             

#Helper method, determines if image res is equal to canvas res
def resNotEqual(img_height, img_width, canvas_width, canvas_height):
    return (img_height * img_width) != (canvas_width * canvas_height)    