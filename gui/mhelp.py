# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 14:39:25 2016

@author: Kenneth
"""
import Tkinter as tk
import tkFont

def ShowHelp(event=None):
    HEADINGS = ['Description', 'Usage']
    header_font = tkFont.Font(weight='bold',
                              underline=1, 
                              size=12,
                              family='Arial')
                              
    default_font = tkFont.Font(family='Arial',
                               size=10)
                               
    hlp= tk.Toplevel()
    #give window focus on creation
    hlp.focus_set()
    #custom title
    hlp.title('LPR | Help')
    #center on screen
    screen_width = hlp.winfo_screenwidth()
    screen_height = hlp.winfo_screenheight()
    posx = (screen_width/2)- 200
    posy = (screen_height/2)- 200
    hlp.geometry('400x400+%d+%d' %(posx,posy))
    hlp.resizable(width=False, height=False)
    
    
    #create text widget to display help info
    text =  tk.Text(hlp, cursor='arrow',
                    wrap=tk.WORD, 
                    state=tk.NORMAL,
                    bg="#e3e3e3",
                    width=50, height=20,
                    spacing1=5,
                    padx=5) 
    helptxt = open('resources/ex/help.txt').read()
    helptxt = helptxt.split('\n')
    print helptxt    
    
    start = 1.0
    end_row, end_col = 1, 0
    #end = float(end_row+'.'+end_col)
    
    
    #header and content alternate
    for i in range(len(helptxt)):
       divider = 10
       
       txt = helptxt[i]
       txt_len = len(txt)
       if len(str(txt_len)) == 1:
           divider = 10
       else:
           divider = 100
       #print txt_len
       end_col = txt_len
       
       end = float(end_row) +(float(end_col) / divider)
       #print end
       
       
       #need to add text first before assigning tags    
       text.insert(tk.INSERT, helptxt[i])
       if txt in HEADINGS: #header text
           
           text.tag_add("HEADER", start, end)
       else:
           text.tag_add("DEFAULT",start, end)
           
       text.insert(tk.INSERT, '\n')
       #print text.get(start,end)
       end_row += 1
       start += 1.0
       

    text.tag_configure("HEADER", font=header_font, foreground='#00aaff')  
    text.tag_configure("DEFAULT", font=default_font)  
    #print text.tag_ranges("HEADER")
    text.config(state=tk.DISABLED)
    text.grid(sticky=tk.NE)
