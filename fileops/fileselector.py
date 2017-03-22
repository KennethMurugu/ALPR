# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 14:09:20 2016

@author: Kenneth
"""
from constants.alprconstants import CWD
import tkFileDialog as tFD
import Tkinter as tk
from fileops.getfilename import getFileName

def fileSelector(root, listbox, file_paths):
         """Selects* image from directory and gets file name"""
         #set necessary variables
         #global file_paths
         file_names = []
         files  = []
         file_list = []#full path name
         file_options = {'initialdir':'/',
                              'title':'Choose file(s) to load',
                              'filetypes':[('JPEG','*.jpg *.jpeg'),
                                           ('Bitmap Image','*.bmp'),
                                           ('PNG Images','*.png')]}
         #open UI to select file
         file_tuple = tFD.askopenfilenames(parent=root, **file_options)
         #print file_tuple
         if file_tuple != '':
             for index, value in enumerate(file_tuple):
                 file_list.append(str(file_tuple[index]))
             #print self.file_list
             file_paths = file_list
             
             for f in file_list:
                 file_names.append(getFileName(f,'/'))
            # print (self.file_names)
            
             for name in file_names:
                 listbox.insert(tk.END, name)
             
             #for x in range(len(self.file_list)):
              #   self.files.append((self.file_list[x], self.file_names[x]))
             files = zip(file_list, file_names)
             #print self.files