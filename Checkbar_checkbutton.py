# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 14:57:29 2019

@author: user
"""

from tkinter import *
import os
from PIL import Image
from PIL import ImageTk

def photoconverter(src,x = None,y = None):
        photo = Image.open(src)
        if x == None or y == None:
            pass
        else:
            photo = photo.resize((int(2*x/3),int(2*y/3)))
        photo = ImageTk.PhotoImage(photo)
        
        return photo
    
class Checkbar_checkbutton(Button):
    def __init__(self, i, check, lst, *arg):
        super().__init__(*arg)
        self.i = i
        self.check = check
        self.currentPath = os.getcwd()+"\\button"
        self.notchecked = photoconverter(self.currentPath + '\\playlist_notchecked.png',171,80)
        self.configure(image = self.notchecked,relief = FLAT,bg = "#347B36", bd = 0 , activebackground = "#347B36", highlightthickness = 0)
        '''self.bt = Button(container, image = self.image, command = self.ChangeStatus)
        self.bt.pack()'''
        self.lst = lst
        
    def ChangeStatus(self):
        if self.check:
            self.notchecked = photoconverter(self.currentPath + '\\playlist_notchecked.png',171,80)
            self.configure(image = self.notchecked,relief = FLAT,bg = "#347B36", bd = 0 , activebackground = "#347B36", highlightthickness = 0)
            self.check = False
            self.lst.remove(self.i)
            #print(lst)
            
        else:
            self.ischecked = photoconverter(self.currentPath + '\\playlist_ischecked.png',171,70)
            self.configure(image = self.ischecked,relief = FLAT,bg = "#347B36", bd = 0 , activebackground = "#347B36", highlightthickness = 0)
            self.check = True
            self.lst.append(self.i)
            #print(lst)