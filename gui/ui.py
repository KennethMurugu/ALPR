# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 22:30:24 2016

@author: Kenneth
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 12:19:43 2016

@author: Kenneth
"""

import tkFileDialog as tFD
import Tkinter as tk
import tkFont
from PIL import ImageTk
from constants.alprconstants import ROOT_WIDTH, ROOT_HEIGHT, CANVAS_WIDTH, CANVAS_HEIGHT, CWD
from fileops import getFileName, imgloader, OCR, crop
from mhelp import ShowHelp
from changelog import ShowChangelog
from tkMessageBox import showwarning
try:
    import Image
except ImportError:
    from PIL import Image         

class MainWindow():
     """Class will generate the main user interface.""" 
     groot = None
     frame_root = None
     imgloader=None
     file_name_list = []
     file_name_var = None
     x0, y0 = None, None
     listbox = None
     file_paths = []
     img_canvas = None
     canvas = None
     start_x, start_y,end_x, end_y = 0, 0, 0, 0
     current_img_path = ""
     global bbox
     bbox = None
     
     #
     #Initializing MainWindow Class
     #
     def __init__(self, root, root_w, root_h):
         global groot, file_name_list, file_name_var, frame_root, listbox, img_canvas, canvas

         self.crop_window_created = False
         #initialise imgloader
         #imgloader = ImageConstants()
         
         #configure root
         root.minsize(width=ROOT_WIDTH, height=ROOT_HEIGHT)
         root.resizable(width=False, height=False)
         #root bindings for keyboard shortcuts
         root.bind("<Control-H>", ShowHelp)
         root.bind("<Control-h>", ShowHelp)
         root.bind("<Control-O>", self.IndLoadImage)
         root.bind("<Control-o>", self.IndLoadImage)
         root.bind("<Control-Shift-L>", self.ClearListbox)
         root.bind("<Control-Shift-l>", self.ClearListbox)
         
         #font for button
         self.header_font = tkFont.Font(weight='bold',
                              underline=1, 
                              size=12,
                              family='Arial')
                              
         self.plate_font =  tkFont.Font(weight='bold', size=12)                            
         self.listbox_font = tkFont.Font(underline=0, size=10)
         
         #LABEL FOR BG image, place before all other widgets
         self.img = imgloader.MAIN_BG
         
         self.bg_height = self.img.height
         self.bg_width = self.img.width
         
         self.bg = ImageTk.PhotoImage(self.img)
         self.bg_label = tk.Label(master=root, image=self.bg)
         self.bg_label.image = self.bg
         self.width_diff = ROOT_WIDTH-self.bg_width
         self.height_diff = ROOT_HEIGHT-self.bg_height
         self.bg_label.place(x=-150, y=-100)
         
         
         
         #Canvas to show selected image
         self.canvas_w, self.canvas_h = root_w*0.68, root_h-6
         self.canvas = tk.Canvas(master=root,
                                 width=self.canvas_w,
                                 height=self.canvas_h,
                                 bd=1, bg='#111', 
                                 relief=tk.SUNKEN)
         
         
         self.img_w, self.img_h = self.bg.width(), self.bg.height()
         self.x_img = self.canvas_w/2 - (self.img_w/2)
         self.y_img = self.canvas_h/2 - (self.img_h/2)
         self.canvas_bg = ImageTk.PhotoImage(imgloader.CANVAS_BG)
         img_canvas =  self.canvas.create_image(self.canvas_w/2,
                                                self.canvas_h/2, 
                                                anchor=tk.CENTER, 
                                                image=self.bg)
         
         
         self.canvas.grid(sticky=tk.NE)
         #button to enable crop
         #self.cr = CropWindow()
         self.btn_bg_default = ImageTk.PhotoImage(imgloader.BTN_BG_DEFAULT)
         self.btn_crop = tk.Button(master=root, text="crop",
                                   anchor=tk.NE,
                                   command=self.CropInstance,                                  
                                   compound=tk.CENTER)
         self.btn_crop.grid(row=0, column=0,
                            sticky=tk.NE, padx=5,pady=5)
         self.btn_clear = tk.Button(master=root, text="clear",
                                   anchor=tk.NE,
                                   command=self.ClearCanvas)
         self.btn_clear.grid(row=0, column=0,
                            sticky=tk.NE, padx=5,pady=40)                   
         #bind events for crop functionality
         
    
         
         #add FRAME to window
         #frame to hold listbox
         self.frame_bg = ImageTk.PhotoImage(imgloader.FRAMELIST_BG)
         self.frame_posx, self.frame_posy = 0.725*root_w, 0.01*root_h
         self.frame_height, self.frame_width = root_h*0.60, root_w*0.2
         print self.frame_width
         self.frame_file_list = tk.Frame(root,
                                         bg="#e3e3e3",
                                         width=self.frame_width,
                                         height=self.frame_height,
                                         borderwidth=1)
         
         
         self.frame_file_list.grid(row=0,column=1,
                                   sticky=tk.N+tk.E,
                                   pady=10,padx=30,
                                   columnspan=2)
         
         
         #Listbox to hold file names
         self.scrollbar = tk.Scrollbar(master=self.frame_file_list,
                                       troughcolor='#ff0000')
         self.list = tk.Listbox(master=self.frame_file_list,
                                bg='#fff',
                                height=15,width=25,
                                yscrollcommand = self.scrollbar.set,
                                font=self.listbox_font,
                                activestyle=None)
                                
         self.list.grid(sticky=tk.N+tk.S,ipady=50)                       
         #event handler for listbox
         self.list.bind('<<ListboxSelect>>', self.ListSelection)
         
         
         self.scrollbar.grid(row=0,column=2,
                             sticky=tk.N+tk.S,
                             pady=0)
         self.scrollbar.config(command=self.list.yview)
         
         
         
         #button to start recognition process
         self.recog_var = tk.StringVar()
         self.recog_var.set("RECOGNIZE")
         #instance of OCR
         
         self.btn_recognize = tk.Button(master=root,
                                        textvariable=self.recog_var,
                                        foreground='#00aaff',
                                        state=tk.NORMAL,
                                        command=self.OCRInstance)
         self.btn_recognize.grid(row=0, column=1,
                                 sticky=tk.SE,
                                 pady=75,padx=10,
                                 ipadx=62)                               
       
         
         self.plate_canvas = tk.Canvas(master=root,
                                       relief=tk.SUNKEN, 
                                       width=190,height=30,
                                       bd=0, bg='#000')
         self.plate_canvas.grid(row=0,column=1,
                                sticky=tk.SE, pady=25,padx=12)
         
         self.plate_var = tk.StringVar()
         self.plate_var.set("[WAITING]")
         self.plate_label = tk.Label(master=root,
                                     bg='#000', anchor=tk.CENTER,
                                     textvariable=self.plate_var,
                                     fg='#00ff00', font=self.plate_font)
                                    
         self.plate_label.grid(row=0, column=1,
                               sticky=tk.SE, pady=30,padx=70)
         
         
         
         #add MENUBAR;options for help
         self.menubar = tk.Menu(master=root)
         self.filemenu = tk.Menu(self.menubar, tearoff=0)
         self.helpmenu = tk.Menu(self.menubar, tearoff=0)
         self.aboutmenu = tk.Menu(self.menubar, tearoff=0)
         
         
         self.menubar.add_cascade(label='File', menu=self.filemenu)
         self.menubar.add_cascade(label='Help', menu=self.helpmenu)
         self.menubar.add_cascade(label='About', menu=self.aboutmenu)
         self
         
         self.filemenu.add_command(label='Open...  Ctrl+O', command=self.IndLoadImage)
         self.filemenu.add_separator()
         self.filemenu.add_command(label='Clear List   Ctrl+Shift+L', command=self.ClearListbox)
         self.filemenu.add_separator()
         self.filemenu.add_command(label='Exit', command=self.MenuExit)
         #self.mhelp = ShowHelp(master=root)
         self.helpmenu.add_command(label='Help   Ctrl+H', command=ShowHelp)
         self.aboutmenu.add_command(label='LPR Changelog', command=ShowChangelog)
         
         
         root.config(menu=self.menubar)
         
         

         #may need to be used globally by other methods         
         listbox = self.list
         frame_root = self.frame_file_list
         canvas = self.canvas
         groot = root
         
#=======================End __init__==============================#
         
         
#=========================Crop Functionality==================#
     def CropInstance(self):
             global current_img_path
             #print current_img_path
             
             try :
                 #Create instance of Crop Window
                 self.cr = crop.CropWindow(self.canvas, img_canvas)
                 self.crop_window_created = self.cr.isWindowCreated()
                 if not self.crop_window_created:
                     #Create Crop Window, TODO: only if it does not exist yet
                     self.cr.Crop(current_img_path)
             except NameError as ne:
                 print ne
         
#=================OCR instance creation=================#
     def OCRInstance(self):
         global current_img_path,start_x, start_y, end_x, end_y
        
         alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
         numbers = '1234567890'
         special = '-'
         plate = ''
         
         try:
             self._ocr = OCR(current_img_path)
             self.plate_var.set('.....')
             self.LICENSE_PLATE = self._ocr.Start()
             
             for char in self.LICENSE_PLATE:
                 if char  in alphabet or char  in numbers or char in special:
                     if char=='Q':
                         char = '9'
                     plate = plate+char
             
             if self.LICENSE_PLATE != '':
                 self.plate_var.set(plate)
                 
             elif '\n' in self.LICENSE_PLATE:
                 showwarning(title='Text too long',
                             message=plate)
             else:
                 showwarning(title='Error in Processing',
                             message='Recognition Failed!')
                 self.plate_var.set('ERROR')            
         except NameError as ne:
             print ne

         
#================listbox event handler=================================#
 
     
    
     def ListSelection(self,event):
         #TODO: fix bug; IndexError after selecting additional files
         global listbox, file_paths, img_canvas, canvas, current_img_path
         index = listbox.curselection()

         print "ListSelection index: ",index
         try:
             #get index of the current selection
             select = index[0]
             #get file path at that index
             path = file_paths[select]
             #make current path globally available (for cropping)
             current_img_path = path
             print "currimgpath: ",current_img_path
             #load image with supplied path (PhotoImage)
             print "canvas_w:",self.canvas_w," canvas_h:",self.canvas_h
             img_to_load, message = imgloader.loadImage(path, self.canvas_w, self.canvas_h, Resize=True)
             
#             if message == "RESIZED":
#                 showwarning(title="Image Resized",
#                             message="The image may be resized and appear blurred/or squeezed in the display. NOTE: this will not affect processing")
             
             #remove current image
             canvas.delete(img_canvas)
             canvas.image = img_to_load #keep reference
             #load new image
             canvas.create_image(self.canvas_w/2,self.canvas_h/2, anchor=tk.CENTER, image=img_to_load)
             print 'LISTBOX SIZE: ',listbox.size()
         except IndexError as e:#handled for now
            print e
            print 'User probably clicked empty listbox'
                  
         
     
     
#=================Methods to LoadImages=====================#    
           
     
     def IndLoadImage(self,event=None):
         """Indirect method to load image; avoids use of lambda functions and global variables(partially)"""
        
         self.fileSelector(self.groot)
     
     def fileSelector(self,root):
         """Selects* image from directory and gets file name"""
         #set necessary variables
         global file_paths, listbox
         try:
             print file_paths
         except NameError:
             #init file_paths
             file_paths = []
             
         file_names = []
         #files  = []
         file_list = []#full path name
         file_options = {'initialdir':'/',
                              'title':'Choose file(s) to load',
                              'filetypes':[('JPEG','*.jpg *.jpeg'),
                                           ('Bitmap Image','*.bmp'),
                                           ('PNG Image','*.png')]}
         #open UI to select file
         file_tuple = tFD.askopenfilenames(parent=root, **file_options)
         print "File Tuple: ",file_tuple
         if file_tuple != '':
             for index, value in enumerate(file_tuple):
                 file_list.append(str(file_tuple[index]))
                 #file_paths.append(str(file_tuple[index]))
             #print self.file_list
             if file_paths == []:
                 file_paths = file_list
             else:
                 for each in file_list:
                     file_paths.append(each)
             #print len(file_paths)
             
             for f in file_list:
                 file_names.append(getFileName(f,'/'))
            # print (self.file_names)
            
             for name in file_names:
                 listbox.insert(tk.END, ' '+name)
             
             #for x in range(len(self.file_list)):
              #   self.files.append((self.file_list[x], self.file_names[x]))
             #files = zip(file_list, file_names)
             #print self.files
             
         
         
     def AddToFileList(self, file_names):
          global listbox
          file_list=[]
          for f in file_list:
              file_names.append(getFileName(f,'/'))
              # print (self.file_names)
            
          for name in file_names:
              listbox.insert(tk.END, ' '+name)
#=======================End load image================================#


#====================Methods to add button========================#
     
         
     def addButtonCommand(self,root,txt,command, x=50, y=150, side=tk.BOTTOM, anchor=tk.NW, bg='#fff', fill=tk.BOTH):
         """Resusable code to add button with callback function to window"""
         self.btn_txt_var = tk.StringVar()
         self.btn_txt_var.set(txt)
         
         self.options={'textvariable':self.btn_txt_var, 'command':command, 'padx':10, 'anchor':tk.CENTER, 'bg':bg}
         
         tk.Button(master=root, **self.options).place(x=x,y=y)
         
#=================end addutton========================#    
         
         
#================add labels=================#
         
     def addLabel(self, root, txt):
          global file_name_var, x0, y0
          x0,y0=-10,10
          file_name_var.set(txt)
          tk.Label(master=root, textvariable=file_name_var, bg='white').place(x=x0+10, y=y0+10)
          x0, y0 = x0+10, y0+10
          
    
     def MenuExit(self, root=groot):
         """Will destroy main window and exit application"""
         groot.destroy()
         
     def ClearCanvas(self):
         global canvas, img_canvas
         canvas.delete(img_canvas)
         img_canvas = canvas.create_image(self.canvas_w/2,self.canvas_h/2, anchor=tk.CENTER, image=self.bg)
         self.plate_var.set("[WAITING]")
     
     def ClearListbox(self, event=None):
         global file_paths
         #delete contents of the listbox
         listbox.delete(first=0, last=listbox.size()-1)
         #reset variable that holds paths to the images
         file_paths = []
         #delete image from canvas
         self.ClearCanvas()
     
     def TestHello(self):
         print "HELLLLLLLOOOOOOO!"
