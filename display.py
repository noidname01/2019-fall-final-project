from tkinter import *
import os
from PIL import Image
from PIL import ImageTk
class test1:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("800x1080")
        self.window.title("test display")
        
        frame1 = Frame(self.window)
        text = Text(frame1)
        vsb = Scrollbar(orient="vertical", command=text.yview)
        text.configure(yscrollcommand=vsb.set)
        frame1.pack(fill="both",side="left")
        vsb.pack(side="right", fill="y")
        text.pack(fill="both", expand=True)
        
        self.currentPath = os.getcwd()
        self.filelist = os.listdir(self.currentPath+"\\src")
        self.thumbnails = []
        for thumbnail in self.filelist:
            image = Image.open(self.currentPath+"\\src\\" +thumbnail)
            image = ImageTk.PhotoImage(image)
            self.thumbnails.append(image)
        
        for photo in self.thumbnails:
            b = Button(frame1, image = photo, text = "test1", compound = "left")
            text.window_create("end", window=b)
            text.insert("end", "\n")
        

        self.window.mainloop()
        
test1()