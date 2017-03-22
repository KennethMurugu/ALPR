# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 16:23:55 2016

@author: Kenneth
"""

# -*- coding: utf-8 -*-
import Tkinter as tk
from PIL import Image, ImageTk
from tkMessageBox import showerror, askyesno

class CropWindow():
    """This class will generate the interface the user will use to crop an image"""
    def __init__(self, UIcanvas, img_on_UIcanvas):
        self.canvas = UIcanvas
        self.img_on_canvas = img_on_UIcanvas
        self.window_created = False
        print "CropWindow intialised"

    def Crop(self, path):
        """Will open the Crop Window"""
        global img, crop
        self.window_created = True
        self.path = path
        self.crop = tk.Toplevel(None)
        self.crop.protocol("WM_DELETE_WINDOW", self.CloseCropWindow)
        
#        tk.Label(crop, text=self.path).grid()
        self.crop.title("Crop Window")
        #load image specified in path var
        img = Image.open(self.path)
        img = ImageTk.PhotoImage(img)
        #print img.height()
        #create canvas to show image
        global crop_canvas            
        crop_canvas = tk.Canvas(master=self.crop, bg='#000',
                                width=img.width(), height=img.height())
        
        crop_canvas.bind('<Button-1>', self.Btn1Pressed)
        crop_canvas.bind('<ButtonRelease-1>', self.Btn1Released)
        crop_canvas.bind('<B1-Motion>', self.Btn1Motion)
        
        
        crop_canvas.create_image(0,0,anchor=tk.NW, image=img)
        crop_canvas.image = img #keep image reference
        crop_canvas.grid(sticky=tk.NW)
        self.crop.focus_set()
        
        #btns for zoom functionality
        """
        zoom_in = tk.Button(master=self.crop_canvas,text='+', anchor=tk.NE,
                            command=self.ZoomIn)
        zoom_out = tk.Button(master=self.crop_canvas,text='-',anchor=tk.NE, 
                             command=self.ZoomOut)
        """
        #zoom_in.place(x=img.width()-14,y=0)
        #zoom_out.place(x=img.width()-14,y=30)
    
    """
    Event Listener methods to create the drag bounding box
    """
    def Btn1Pressed(self,event):
         global start_x, start_y
         start_x, start_y = event.x, event.y
       
    def Btn1Motion(self, event):
        x1, y1 = event.x, event.y
        try:
            crop_canvas.delete(self.bbox)
            self.bbox = crop_canvas.create_rectangle(start_x, start_y,x1,y1,outline='#ff0000')
        except:
            self.bbox = crop_canvas.create_rectangle(start_x, start_y,x1,y1,outline='#ff0000')
            
    def Btn1Released(self,event):
         global end_x, end_y, canvas, file_paths, img
         end_x, end_y = event.x, event.y
         coord = start_x, end_x,start_y, end_y
         print coord
         if end_x > img.width():
            err = showerror(title="Error",
                       message="Error occured during cropping, probably because the bounds of the crop were outside the image boundary.")
            self.crop.focus_set()
         else:     
             try:
                 crop_canvas.delete(self.bbox)
                 self.bbox = crop_canvas.create_rectangle(start_x, start_y, end_x, end_y, outline='#ff0000')
             except:
                 self.bbox = crop_canvas.create_rectangle(start_x, start_y, end_x, end_y, outline='#ff0000')
         
             crop_exit = askyesno(master=self.crop ,title = 'Crop Captured',
                      message="Coordinates for the crop successfully captured.\nExit the Crop Window?")
             #print "CROP_EXIT: ",crop_exit  
             if crop_exit:         
                 #write coords to temp file for ocr.py         
                 f = open('temp\\COORDS', 'w')
                 for i in coord:
                     f.write(str(i)+'\n')
                 f.close()
                 self.crop.withdraw()
                 #self.canvas.delete(self.img_on_canvas)
                 #self.canvas.create_image(img.width()/2, img.height()/2,
                                         #anchor=tk.CENTER, image=img)
             else:
                 self.crop.focus_set()
    def CloseCropWindow(self):
        self.window_created = False
        self.crop.withdraw()
             
    def isWindowCreated(self):
        return self.window_created
        
    def ZoomIn(self):
        print 'dcsc'
        
    def ZoomOut(self):
        print'asda'
    