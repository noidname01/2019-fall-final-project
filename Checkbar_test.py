# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 18:29:06 2019

@author: user
"""

from tkinter import *
import os
from PIL import Image
from PIL import ImageTk

class Checkbar:
    def __init__(self, container, image = None, command = None, i=0, check = False):
        self.i = i
        self.check = check
        self.currentPath = os.getcwd()
        self.image = Image.open(self.currentPath + '\\2.png')
        self.image = ImageTk.PhotoImage(self.image)
        Button(container, image = self.image).pack()
        
class test_GUI:
    def __init__(self, master = None):
        self.window = master
        
        self.frame = Frame(self.window)
        self.frame.pack()
        
        self.currentPath = os.getcwd()
        self.image = Image.open(self.currentPath + '\\2.png')
        self.image = ImageTk.PhotoImage(self.image)
        bt = Button(self.frame, image = self.image)
        bt.pack()
        
window = Tk()
test_GUI(window)
window.mainloop()