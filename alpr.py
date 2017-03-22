# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 22:18:14 2016

@author: Kenneth
"""
import Tkinter as tk
from gui import MainWindow
from constants.alprconstants import APP_VER


dependency = 'Tkinter'

try:
    __import__(dependency)
except ImportError as e:
    print str(e)+' :'+dependency+' '+'is probably not installed on the system'

#SPLASH
#from gui import Splash
#mSplash = SplashWindow()


#preload image constants
#preloaded = imgloader.PreloadImages()
root = tk.Tk()
root.title("License Plate Recognition (LPR) "+ APP_VER)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_percent, y_percent = 800.0/screen_width, 480.0/screen_height
root_w, root_h = x_percent*screen_width, y_percent*screen_height

posx = (screen_width/2)- (root_w/2)
posy = (screen_height/2)- (root_h/2)

print "root_w:",root_w," root_h:",root_h
#print  "Constants:", ROOT_WIDTH, ROOT_HEIGHT

root.geometry('%dx%d+%d+%d' %(root_w, root_h, posx, posy))

app = MainWindow(root, root_w, root_h)

root.focus_set()
root.mainloop()

