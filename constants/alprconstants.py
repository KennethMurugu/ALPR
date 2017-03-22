# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 13:20:16 2016

@author: Kenneth
"""
#import Tkinter as tk
#Will use universal widget methods winfo_screenwidth/height() to get width 
#and height of display monitor and reisze root aspect ratio to monitor
#aspect ratio


#MONITOR_WIDTH = tk.Frame(root=None).winfo_screenwidth()
import os
CWD = os.getcwd()
APP_VER = '0.1.1 BETA'
ROOT_WIDTH = 800
ROOT_HEIGHT = 480
CANVAS_WIDTH, CANVAS_HEIGHT = 500, 400

ASPECT_RATIO = float(ROOT_WIDTH)/ float(ROOT_HEIGHT)