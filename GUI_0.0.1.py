from tkinter import *
#from m1 import youtube_downloader

class youtube_downloader_GUI:
    def __init__(self):
        window = Tk()
        window.title("Youtube Video Downloader")
        
        frame1 = Frame(window)
        frame1.pack()
        label1 = Label(frame1, text = "paste your URL below: ")
        label1.grid(row = 1, column = 1)
        
        frame2 = Frame(window)
        frame2.pack()
        self.URL = StringVar()
        entry = Entry(frame2, textvariable = self.URL)
        btDownload = Button(frame2, text = "Download", command = self.Download_video)
        entry.grid(row = 1, column = 1)
        btDownload.grid(row = 1, column = 2)
        
        frame3 = Frame(window)
        frame3.pack()
        self.status = StringVar()
        self.status.set("")
        label2 = Label(frame3, textvariable = self.status)
        label2.grid(row = 1, column = 1)
        
        window.mainloop()
        
    def Download_video(self):
        self.status.set("Download in process, please wait a minute...")
        #youtube_downloader(self.URL.get(), True, False)
    
youtube_downloader_GUI()