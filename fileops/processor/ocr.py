# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 21:50:52 2016

@author: Kenneth
"""
from pytesseract import image_to_string
from PIL import Image, ImageTk
from tkMessageBox import showerror
import numpy as np
from scipy import misc, ndimage
from skimage import measure
from skimage.segmentation import clear_border
import matplotlib.pyplot as plt

import cv2

class OCR():
    """This class handles image processing and character recognition"""
    
    def __init__(self, path):
        self.path = path
        try:
            f = open('temp\\COORDS','r')
            f_split = f.read().split()
            f.close()
        except IOError:
            showerror(title='Fatal Error',
                      message='Unable to read coordinates for image reading')
        
        self.x0 = int(f_split[0])
        self.x1 = int(f_split[1])
        self.y0 = int(f_split[2])
        self.y1 = int(f_split[3])
        print "OCR img path: ",self.path
    
    def Start(self):
        #use scipy.misc to read image as numpy array, grayscale
        img= cv2.imread(self.path)
        l = img.shape[-1]
        
        #grayscale image
        gray_scaled= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
        
        
        #crop img using given coordinates
        img_cropped = gray_scaled[self.y0:self.y1, self.x0:self.x1]
        #threshold grayscaled+cropped image
        ret, threshed = cv2.threshold(img_cropped,0,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        #make img larger to improve accuracy
        resized = misc.imresize(threshed, 1.5)
        #apply gaussian filter
        resized = ndimage.gaussian_filter(resized, sigma=l/(4.*10), order=0)
        #apply mask to get rid of noise
        mask = (resized > resized.mean()).astype(np.float)
        #connected component analysis
        all_labels = measure.label(mask)
        blob_labels = measure.label(mask, background=1)
        plt.imshow(blob_labels)
        #need to get image as PhotoImage object
        cv2.imwrite('tempimg.png', resized)
        #img_converted = ImageTk.PhotoImage(Image.open('tempimg.png')) 
        #OCR it!
        plate = image_to_string(Image.open('tempimg.png'), lang='eng')
        print "PLATE: ",plate
        
#        #read color image from disc
#        img_color = cv2.imread(self.path)
#        
#        #convert to grayscale
#        img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
#        
#        #crop image from given coordinates
#        img_gray_cropped = img_gray[self.y0:self.y1, self.x0:self.x1]
#        
#        #
#        #THRESHOLDING
#        #
#        
#        #basic thresholding
#        ret, thresh = ret, threshed = cv2.threshold(img_gray_cropped,0,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
#        
#        #find contours on the threshed image
#        contours, hierarchy = cv2.findContours(threshed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#        
#        #loop through each contour, draw on mask image
#        mask = np.zeros(threshed.shape, np.uint8)
#        for h, cnt in  enumerate(contours):
#            if cv2.contourArea(cnt) > 20:
#                cv2.drawContours(mask, [cnt],0, 255, 1)
#        
#        
#        cleared = mask
#        clear_border(cleared)
#        #make img larger to improve accuracy
#        resized = misc.imresize(cleared, 1.1)
#        
#        #need PhotoImage object; save to disk (temp) and re-read
#        cv2.imwrite('tempimg.png', resized)
#        
#        #use tesseract to read
#        plate = image_to_string(Image.open('tempimg.png'), lang='eng')
        
        
        return plate
        