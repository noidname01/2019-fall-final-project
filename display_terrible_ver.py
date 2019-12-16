from tkinter import *
import os
from PIL import Image
from PIL import ImageTk
"""class container:
    def __init__(self,i):
        super
        
c= container()
c.nujm"""
class test1:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("800x1080")
        self.window.title("test display")
        
        frame1 = Frame(self.window)
        text = Text(frame1, bg = "#347B36")
        vsb = Scrollbar(orient="vertical", command=text.yview)
        text.configure(yscrollcommand=vsb.set)
        frame1.pack(fill="y",side="left")
        vsb.pack(side="right", fill="y")
        text.pack(fill="y",expand=True)
        
        self.currentPath = os.getcwd()
        self.filelist = os.listdir(self.currentPath+"\\src")
        self.thumbnails = []
        for thumbnail in self.filelist:
            image = Image.open(self.currentPath+"\\src\\" +thumbnail)
            image = image.resize((246,138))
            image = ImageTk.PhotoImage(image)
            self.thumbnails.append(image)
        
        self.button_text_list = []
        self.button_list = []
        self.button_ischecked = []
        for i in range(len(self.thumbnails)):
            button_text = StringVar()
            button_text.set("test1")
            self.button_text_list.append(button_text)
            b = Button(frame1, image = self.thumbnails[i], textvariable = self.button_text_list[i] , compound = "left")
            self.button_list.append(b)
            self.button_ischecked.append(False)
            #self.button_list[i].configure(command = self.changeBG(i))
            text.window_create("end", window=b)
            text.insert("end", "\n")
        
        Button(self.window, text = "test1").pack()
        self.window.mainloop()
        
    """def changeBG(self,i):
        print("in")
        if not self.button_ischecked[i]:
            self.button_list[i].configure(bg = "#367B34")
            self.button_ischecked[i] = True
        else:
            self.button_list[i].configure(bg = "#FFFFFF")
            self.button_ischecked[i] = False"""
        
test1()