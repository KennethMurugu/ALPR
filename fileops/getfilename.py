# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 13:36:32 2016

@author: Kenneth
"""
        
def getFileName(filestring,opt):
    """Splits file at the 'opt' keyword provided e.g '/' or '\'"""
    filestring_split = filestring.split(opt)
    len_split = len(filestring_split)
    
    filename = filestring_split[len_split-1]
    return filename