# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 14:57:29 2019

@author: user
"""

from tkinter import *
import os
from PIL import Image
from PIL import ImageTk

class Checkbar_checkbutton(Button):
    def __init__(self, i, check, lst, *arg):
        super().__init__(*arg)
        self.i = i
        self.check = check
        self.currentPath = os.getcwd()
        self.image = Image.open(self.currentPath + '\\2.png')
        self.image = ImageTk.PhotoImage(self.image)
        self.configure(image = self.image)
        '''self.bt = Button(container, image = self.image, command = self.ChangeStatus)
        self.bt.pack()'''
        self.lst = lst
        
    def ChangeStatus(self):
        if self.check:
            self.currentPath = os.getcwd()
            self.image = Image.open(self.currentPath + '\\2.png')
            self.image = ImageTk.PhotoImage(self.image)
            self.configure(image = self.image)
            self.check = False
            self.lst.remove(self.i)
            #print(lst)
            
        else:
            self.currentPath = os.getcwd()
            self.image = Image.open(self.currentPath + '\\1.png')
            self.image = ImageTk.PhotoImage(self.image)
            self.configure(image = self.image)
            self.check = True
            self.lst.append(self.i)
            #print(lst)