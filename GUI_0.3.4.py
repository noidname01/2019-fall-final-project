from tkinter import *
import tkinter.messagebox
from tkinter import ttk
from youtube_downloader_plan2 import youtube_downloader
from selenium import webdriver
from time import sleep
import time
import os
import requests
import re
import threading
import shutil
from pygame import mixer
import random
import sys
from time import sleep
from bs4 import BeautifulSoup
from PIL import Image
from PIL import ImageTk
from Checkbar_checkbutton import Checkbar_checkbutton
from search import Search

def photoconverter(src,x = None,y = None):
        photo = Image.open(src)
        if x == None or y == None:
            pass
        else:
            photo = photo.resize((int(2*x/3),int(2*y/3)))
        photo = ImageTk.PhotoImage(photo)
        
        return photo

class Loading_GUI:
    def __init__(self, master, issingle, url, last_window):
        self.window = master
        self.window.title("Loading...")
        self.window.geometry("960x720")
        self.last_window = last_window
        self.window.resizable(False,False)
        self.buttonPath = os.getcwd()+'//button'
        
        s = ttk.Style()
        s.theme_use('alt')
        s.configure("Horizontal.TProgressbar", foreground="#367B34", background="#367B34")
        self.loading_background = photoconverter(self.buttonPath+'//loading_background.png',1440,1080)
        self.background = Canvas(self.window, width = 960, height = 720)
        self.background.pack(fill="both",expand = True)
        
        self.background.create_image(480,360,image = self.loading_background)
        self.progressBar = ttk.Progressbar(self.background,style="Horizontal.TProgressbar",orient="horizontal",length=313, mode="determinate")
        self.background.create_window(265,603,window = self.progressBar)
        self.progressBar["maximum"] = 100
        
        self.issingle = issingle
        self.url = url
        
        self.main()
    def main(self):
        self.ytd = youtube_downloader(self.url, self.issingle, not self.issingle, self.progressBar)
        self.ytd.clear()
        if not self.issingle:
            t = threading.Thread(target = self.playlist_starter)
            t.setDaemon(True)
            t.start()
        else:
            t = threading.Thread(target = self.single_starter)
            t.setDaemon(True)
            t.start()
    def playlist_starter(self):
        self.ytd.main()
        self.window.destroy()
        Playlist_results_GUI(self.last_window,self.ytd.playlist_information)
        
    def single_starter(self):
        self.ytd.main()
        self.window.destroy()
    
class Downloader_GUI:
    def __init__(self, master):
        self.window = master
        self.window.title("YouTube Video Downloader")
        self.window.geometry("960x720")
        self.window.resizable(False,False)
        self.buttonPath = os.getcwd()+'//button'
        
        self.download_background = photoconverter(self.buttonPath+'\\download_background.png',1440,1080)
        self.download_button = photoconverter(self.buttonPath+'\\download_button.png',668,283)
        self.download_back = photoconverter(self.buttonPath+'\\download_back.png',346,321)

        self.background = Canvas(self.window, width = 960, height = 720)
        self.background.pack(fill= "both" ,expand = True)
        self.background.create_image(960//2,720//2, image = self.download_background)
        
        self.btGoback = Button(self.background, image = self.download_back, command = self.Goback, relief = FLAT,bg = "#347B36", bd = 0 , activebackground = "#347B36", highlightthickness = 0)
        self.background.create_window(161, 601, window = self.btGoback)
        self.URL = StringVar()
        self.entry = Entry(self.background, textvariable = self.URL, font = "Helvetica 30 bold", width = 35, relief = FLAT)
        self.background.create_window(467 , 265, window = self.entry)
        self.btDownload = Button(self.background, image = self.download_button, command = self.Download_video ,relief = FLAT,bg = "#347B36", bd = 0 , activebackground = "#347B36", highlightthickness = 0)
        self.background.create_window(507, 613, window = self.btDownload)
        self.btCheckbar = Checkbar_radiobutton(self.background)
        
        
        '''self.vtype = IntVar()
        rbtSingle = Radiobutton(self.frame3, text = "Single Video", variable = self.vtype, value = 1)
        rbtPlaylist = Radiobutton(self.frame3, text = "Playlist", variable = self.vtype, value = 2)
        label2.grid(row = 1, column = 1)
        rbtSingle.grid(row = 1, column = 2)
        rbtPlaylist.grid(row = 1, column = 3)'''
        
    def Download_video(self):
        if self.btCheckbar.i == 0:
            self.tl = Toplevel(self.window)
            self.loading = Loading_GUI(self.tl,True,self.URL.get(),self.window)
            self.Showinfo()
        else:
            self.background.destroy()
            self.tl = Toplevel(self.window)
            self.loading = Loading_GUI(self.tl,False,self.URL.get(),self.window)
            
            
        """
        #self.labeltext.set("Download processing...")
        if self.btCheckbar.i == 0:
            self.ytd = youtube_downloader(self.URL.get(), True, False)
            self.Showinfo()
        else:
            self.ytd = youtube_downloader(self.URL.get(), False, True)
            
            Playlist_results_GUI(self.window,self.ytd.playlist_information)
        """
        '''if self.vtype.get() == 1:
            self.ytd = youtube_downloader(self.URL.get(), True, False)
        else:
            self.ytd = youtube_downloader(self.URL.get(), False, True)
        self.Showinfo()'''
        
    def Showinfo(self):
        tkinter.messagebox.showinfo("Status", "Download Processing!")
        '''if self.ytd.is_downloaded():
            tkinter.messagebox.showinfo("Status", "Download Success!")
        else:
            tkinter.messagebox.showwarning("Status", "Download failed, please try again later")'''
    
    def Goback(self):
        self.background.destroy()
        Main_GUI(self.window)
        
class Playlist_results_GUI:
    def __init__(self, master = None, lst=[]):
        self.window = master
        self.window.geometry("960x720")
        self.window.resizable(False,False)
        self.playlist_information = lst
        self.title = [x[1] for x in self.playlist_information]
        self.ytd = youtube_downloader
        self.buttonPath = os.getcwd() + "\\button"
        """
        self.frame0 = Frame(self.window, bg='white')
        self.frame0.pack(fill = BOTH)
        btGoback = Button(self.frame0, text = "Go back", command = self.Goback)
        btGoback.pack(side = LEFT)
        btDownload = Button(self.frame0, text = "Download", command = self.Download)
        btDownload.pack()
        """
        self.playlist_background = photoconverter(self.buttonPath+"\\playlist_background.png",1440,1080)
        
        self.background1 = Canvas(self.window,width=960,height=720)
        self.background1.pack(fill = 'both', expand = True)
        self.background1.create_image(480,360, image = self.playlist_background)
       
        self.frame1 = Frame(self.background1, width = 760, height = 470, relief = FLAT, bd = 0 , highlightthickness = 0)
        self.result_display = Canvas(self.frame1, width = 760, height = 470, scrollregion=(100,150,860,150+len(self.title)*160), bg = "#000000")
        self.vsb = Scrollbar(self.frame1, orient = "vertical", command = self.result_display.yview)
        self.vsb.pack(side = "right", fill = "y")
        self.result_display.configure(yscrollcommand = self.vsb.set)
        self.result_display.pack(fill = "both", expand = True)
        self.background1.create_window(480,370, window = self.frame1)
        
        
        
        #place(x = 100+380 , y = 150+235)
        
        
        
        self.currentPath = os.getcwd()
        self.filelist = os.listdir(self.currentPath+"\\playlist")
        self.list_to_download =[]
        self.thumbnails = []
        for i in range(len(self.filelist)):
            image = Image.open(self.currentPath+"\\playlist\\"+str(i)+".png")
            image = image.resize((200,150))
            image = ImageTk.PhotoImage(image)
            self.thumbnails.append(image)
    
        for i in range(len(self.thumbnails)):
            b0 = Label(self.result_display, image = self.thumbnails[i])
            if len(self.title[i]) > 25:
                for j in range(25,len(self.title[i])):
                    if self.title[i][j] ==  " ":
                        self.title[i] = self.title[i][:j+1] + "\n" + self.title[i][j+1:]
                        break
            b1 = Label(self.result_display, text = self.title[i])
            b1.config(font = ("Arial", 12))
            b2 = Checkbar_checkbutton(i, False, self.list_to_download, self.result_display)
            b2.configure(command = b2.ChangeStatus)
            self.result_display.create_window(150,100+(200*i), window = b0)
            self.result_display.create_window(475,100+(200*i), window = b1)
            self.result_display.create_window(800,100+(200*i), window = b2)
        

        self.window.mainloop()
        
    def Goback(self):
        self.background1.destroy()
        #self.frame1.destroy()
        #self.background.destroy()
        self.vsb.destroy()
        self.list_to_download.clear()
        self.ytd.clear()
        Downloader_GUI(self.window)

    def Download(self):
        #print(self.lst)
        for i in self.list_to_download:
            url = self.playlist_information[i][2]
            title = self.playlist_information[i][1]
            self.thumbnail_downloader(url,str(i))
        """
        for j in self.list_to_download:
            self.ytd(self.playlist_information[j][0], True, False, )
        """
        self.Showinfo()
        
    def Showinfo(self):
        tkinter.messagebox.showinfo("Status", "Download Success!")
        
    def thumbnail_downloader(self,url,title):
        import cv2
        import numpy as np
        #import requests
        
        resp = requests.get(url, stream=True).raw
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        cv2.imwrite('thumbnails\\'+title+'.png', image)
        print(title+'.png Success!')
        
class Search_GUI:
    def __init__(self, master = None):
        self.window = master
        self.window.title("Search YouTube Video(s)")
        self.window.geometry("960x720")
        self.search = Search
        self.buttonPath = os.getcwd() + "\\button"
        self.keyword = StringVar()
        
        self.search_background = photoconverter(self.buttonPath+"\\search_background.png",1440,1080)
        self.search_back = photoconverter(self.buttonPath+"\\search_back.png",453,157)
        self.search_button_png = photoconverter(self.buttonPath+"\\search_button.png",212,191)
        self.search_download = photoconverter(self.buttonPath+"\\search_download.png",571,145)
        
        self.background = Canvas(self.window, width = 960, height = 720, bg = "white")
        self.background.pack(fill= "both" ,expand = True)
        self.background.create_image(480,360, image = self.search_background)
        
        self.frame1 = Frame(self.background, width = 840, height = 410, relief = FLAT, bd = 0 , highlightthickness = 0)
        self.result_display = Canvas(self.frame1, width = 840, height = 410, scrollregion=(60,165,900,200*20), bg = "#FFFFFF")
        self.vsb = Scrollbar(self.frame1, orient = "vertical", command = self.result_display.yview)
        self.vsb.pack(side = "right", fill = "y")
        self.result_display.configure(yscrollcommand = self.vsb.set)
        self.result_display.pack(fill = "both", expand = True)
        self.background.create_window(480,370, window = self.frame1)
        
        self.back = Button(self.background,image = self.search_back, command = self.Goback, relief = FLAT,bg = "#347B36", bd = 0 , activebackground = "#347B36", highlightthickness = 0)
        self.background.create_window(248,663,window = self.back)
        self.entry = Entry(self.background, textvariable = self.keyword, font = "Helvetica 22 bold", width = 25, relief = FLAT)
        self.background.create_window(470,77,window = self.entry)
        self.search_button = Button(self.background, image = self.search_button_png, command = self.Search_video, relief = FLAT,bg = "#347B36", bd = 0 , activebackground = "#347B36", highlightthickness = 0)
        self.background.create_window(852,68, window = self.search_button)
        self.download = Button(self.background, image = self.search_download, relief = FLAT,bg = "#347B36", bd = 0 , activebackground = "#347B36", highlightthickness = 0)
        self.background.create_window(694,663,window = self.download)
        
        self.window.mainloop()
        
    def Search_video(self):
        self.search = self.search(self.keyword.get())
        self.Search_Result(lst = self.search.search_result)
     
        
    def Search_Result(self, lst):
        self.search_result = lst
        self.title = [x[1] for x in self.search_result]
        self.currentPath = os.getcwd()
        self.filelist = os.listdir(self.currentPath+"\\search")
        self.list_to_download =[]
        self.thumbnails = []
        self.ischecked = False
        
        self.search_bar = photoconverter(self.currentPath+"\\button\\search_bar.png",1260,261)
        
        for i in range(len(self.filelist)):
            image = Image.open(self.currentPath+"\\search\\"+str(i)+".png")
            image = image.resize((240,180))
            image = ImageTk.PhotoImage(image)
            self.thumbnails.append(image)
    
        for i in range(len(self.thumbnails)):
            if len(self.title[i]) > 15:
                for j in range(15,len(self.title[i])):
                    if self.title[i][j] ==  " ":
                        self.title[i] = self.title[i][:j+1] + "\n" + self.title[i][j+1:]
                        break
            bar = Canvas(self.result_display,width = 800, height = 200, bg = "white")
            bar.bind("<Button-1>",self.changeBackground)
            b1 = Label(bar,image = self.thumbnails[i], bg = "#FFFFFF")
            b2 = Label(bar, text = self.title[i], bg ="#FFFFFF", font = "Helvetica 16 bold")
            bar.create_window(140,110,window = b1,tags = "search_content")
            bar.create_window(550,110,window = b2,tags = "search_content")
            self.result_display.create_window(500,220+(220*i), window = bar)
    
    def changeBackground(self,event):
        if not self.ischecked:
            event.widget.create_image(420,87,image = self.search_bar, tags = "search_bar")
            event.widget.itemconfig("search_content",backgroundcolor = "#347B36" )
        else:
            event.widget.delete("search_bar")
            event.widget.itemconfig("search_content",backgroundcolor = "#FFFFFF" )
        
    def Goback(self):
        self.background.destroy()
        #self.frame3.destroy()
        Main_GUI(self.window)
        self.background.destroy()
        Main_GUI(self.master)
    
        
'''
class Search_Result_GUI:
    def __init__(self, master = None, keyword = "", lst = []):
        self.window = master
        self.window.title("Search Results")
        self.window.geometry("960x720")
        self.window.resizable(False,False)
        self.search_result = lst
        self.title = [x[1] for x in self.search_result]
        self.ytd = youtube_downloader
        
        self.frame0 = Frame(self.window)
        self.frame0.pack(fill = BOTH)
        btGoback = Button(self.frame0, text = "Go back", command = self.Goback)
        btGoback.pack(side = LEFT)
        btDownload = Button(self.frame0, text = "Download", command = self.Download)
        btDownload.pack()
        
        self.frame1 = Frame(self.window)
        self.frame1.pack(fill=BOTH, expand = True)
        self.background = Canvas(self.frame1,width=960,height=720, scrollregion=(0,0,960,len(self.title)*200))
        self.background.config(bg = '#000000')
        self.vsb = Scrollbar(self.frame1,orient="vertical", command=self.background.yview)
        self.vsb.pack(side="right", fill="y")
        self.background.configure(yscrollcommand=self.vsb.set)
        self.background.pack(fill="both",side="left",expand = True)
        # Results should be Search(keyword)
        
        self.currentPath = os.getcwd()
        self.filelist = os.listdir(self.currentPath+"\\search")
        self.list_to_download =[]
        self.thumbnails = []
        for i in range(len(self.filelist)):
            image = Image.open(self.currentPath+"\\search\\"+str(i)+".png")
            image = image.resize((240,180))
            image = ImageTk.PhotoImage(image)
            self.thumbnails.append(image)
    
        for i in range(len(self.thumbnails)):
            b0 = Label(self.background, image = self.thumbnails[i])
            if len(self.title[i]) > 15:
                for j in range(15,len(self.title[i])):
                    if self.title[i][j] ==  " ":
                        self.title[i] = self.title[i][:j+1] + "\n" + self.title[i][j+1:]
                        break
            b1 = Label(self.background, text = self.title[i])
            b1.config(font = ("Arial", 16))
            b2 = Checkbar_checkbutton(i, False, self.list_to_download, self.background)
            b2.configure(command = b2.ChangeStatus)
            self.background.create_window(120,60+(200*i), window = b0)
            self.background.create_window(475,60+(200*i), window = b1)
            self.background.create_window(840,60+(200*i), window = b2)
        

        self.window.mainloop()
        
    def Goback(self):
        self.frame0.destroy()
        self.frame1.destroy()
        Search_GUI(self.window)
    
    def Download(self):
        #print(self.lst)
        for i in self.list_to_download:
            url = self.search_result[i][2]
            title = self.search_result[i][1]
            self.thumbnail_downloader(url,str(i))
        for j in self.list_to_download:
            self.ytd(self.search_result[j][0], True, False)
        self.Showinfo()
        
    def Showinfo(self):
        tkinter.messagebox.showinfo("Status", "Download Success!")
        
    def thumbnail_downloader(self,url,title):
        import cv2
        import numpy as np
        #import requests
        
        resp = requests.get(url, stream=True).raw
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        cv2.imwrite('thumbnails\\'+title+'.png', image)
        print(title+'.png Success!')
'''
class Player_GUI:
    
    def __init__(self, master = None):
        self.cur_path = os.getcwd()+'\\downloads'
        self.button_src = os.getcwd()+'\\button'
        self.filelist = []
        self.playlist = []
        self.ispause = False
        self.loop_play_times = 0
        self.isloop_play = False
        self.count = 0
        self.is_next_song = False
        self.israndom_play = False
        self.nowplaying = str()
        
        mixer.init()
        self.window = master
        self.window.geometry("960x720")
        self.window.title("mp3 player")
        self.window.resizable(False,False)
        #self.window.configure(background = "#367B34")
        
        #self.thumbnail = photoconverter(os.getcwd()+"\\thumbnails"+"\\1.png",480,360)
        self.play_png = photoconverter(self.button_src+"\\play.png",144,147)
        self.pause_png = photoconverter(self.button_src+"\\pause.png",150,150)
        self.not_loop_play_png = photoconverter(self.button_src+"\\not_loop.png",195,160)
        self.loop_play_png = photoconverter(self.button_src+"\\is_loop.png",195,160)
        self.not_random_play_png = photoconverter(self.button_src+"\\not_random.png",194,185)
        self.random_play_png = photoconverter(self.button_src+"\\is_random.png",194,185)
        self.previous_song_png = photoconverter(self.button_src+"\\previous_song.png",210,200)
        self.next_song_png = photoconverter(self.button_src+"\\next_song.png",125,131)
        self.nowplaying_png = photoconverter(self.button_src+"\\title.png",957,228)
        self.back_png = photoconverter(self.button_src+"\\back.png",369,295)
        self.slider_png = photoconverter(self.button_src+"\\volume_lever.png",99,54)
        self.player_background = photoconverter(self.button_src+"\\background.png",1440,1080)
        
        self.background = Canvas(self.window, width = 960, height = 960)
        self.background.pack(fill= "both" ,expand = True)
        self.background.create_image(480,360, image = self.player_background)
        #self.background.create_image(330,350,image = self.thumbnail)
        
        files = os.listdir(self.cur_path)
        self.filelist = ['downloads\\'+x for x in files]
        self.playlist = [x for x in self.filelist]
        
        self.label_text = StringVar()
        self.volume = 30
        
        self.button1 = Button(self.background, image = self.pause_png , command = self.pause,  relief = FLAT, bg = "#347B36", bd = 0 , activebackground = "#347B36", highlightthickness = 0)
        self.background.create_window(240,612, window = self.button1)
        self.button2 = Button(self.background, image = self.not_loop_play_png , command = self.loop_play, relief = FLAT,bg = "#347B36", bd = 0 , activebackground = "#347B36", highlightthickness = 0)
        self.background.create_window(720,565, window = self.button2)
        self.button3 = Button(self.background, image = self.not_random_play_png , command = self.random_play, relief = FLAT,bg = "#347B36", bd = 0 , activebackground = "#347B36", highlightthickness = 0)
        self.background.create_window(535,595, window = self.button3)
        self.button4 = Button(self.background, image = self.previous_song_png , command = self.previous_song, relief = FLAT, bg = "#347B36", bd = 0 , activebackground = "#347B36", highlightthickness = 0)
        self.background.create_window(90,630, window = self.button4)
        self.button5 = Button(self.background, image = self.next_song_png, command = self.next_song, relief = FLAT, bg = "#347B36", bd = 0 , activebackground = "#347B36", highlightthickness = 0)
        self.background.create_window(380,598, window = self.button5)
        
        self.nowplaying_label = Label(self.background,textvariable = self.label_text, bg = "#FFFFFF")
        self.nowplaying_label.config(font=("Arial", 16),width = 40)
        self.background.create_window(330,100,window = self.nowplaying_label )
        self.back_button = Button(self.background, image = self.back_png, command = self.Goback, relief = FLAT, bg = "#347B36", bd = 0 , activebackground = "#347B36", highlightthickness = 0)
        self.background.create_window(835,410,window = self.back_button)
        
        self.slider_y = 680
        self.background.create_image(860,680, image = self.slider_png, tags="slider")
        self.background.bind("<B1-Motion>",self.drag)
        self.background.bind("<ButtonRelease-1>",self.release)
        
        mixer.music.load(self.playlist[self.count])
        mixer.music.set_volume(self.volume/100)
        mixer.music.play(loops = 0)
        self.nowplaying = self.playlist[self.count]
        self.nowplaying = self.nowplaying.replace(".mp3","")
        self.label_text.set(self.nowplaying.replace("downloads\\",""))
        
        t = threading.Thread(target = self.play)
        t.setDaemon(True)
        t.start()
        
        self.window.protocol("WM_DELETE_WINDOW",self.stop)
        self.window.mainloop()
    
    def drag(self,event):
        if self.background.find_withtag("slider"):
            if event.y_root>=550 and event.y_root<=680:
                dy = event.y_root-self.slider_y
                if dy>0:
                    self.background.move("slider",0,dy)
                else:
                    self.background.move("slider",0,dy)
                self.slider_y+=event.y_root-self.slider_y
                
    def release(self,event):
        if self.background.find_withtag("slider"):
            volume =(680-event.y_root)/(680-550)
            self.set_volume(volume)
            
    def decounter(self):
        if self.count == 0 and not self.isloop_play:
            self.count = len(self.playlist)-1
            
        elif self.isloop_play:
            self.count = 0
            
        else:
            self.count -= 1
                
    def counter(self):
        if self.count == len(self.playlist)-1 or self.isloop_play:
            self.count = 0
        else:
            self.count += 1
            
    def pause(self):
        if self.is_next_song:
            self.is_next_song = False
        
        if not self.ispause:
            mixer.music.pause()
            self.ispause = True
            
        else:
            mixer.music.unpause()
            self.ispause = False
            
        self.button1.configure(image = self.play_png if self.ispause else self.pause_png)
            
    def random_play(self):
        if not self.israndom_play:
            if not self.isloop_play:
                random.shuffle(self.playlist)
                self.randomplaylist = [x for x in self.playlist]
                self.nowplaying = self.nowplaying.replace(".mp3","")
                self.label_text.set(self.nowplaying.replace("downloads\\",""))
                self.israndom_play = True
            else:
                self.playlist = self.loopplaylist
                self.israndom_play = True
        else:
            if self.isloop_play:
                self.playlist = self.loopplaylist
                self.israndom_play = False
            else:
                self.playlist = [x for x in self.filelist]
                self.count = self.playlist.index(self.nowplaying+".mp3")
                self.israndom_play = False
        self.button3.configure(image = self.random_play_png if self.israndom_play else self.not_random_play_png)
    
    def loop_play(self):
        if self.isloop_play and not self.israndom_play:
            self.playlist = [x for x in self.filelist]
            self.count = self.playlist.index(self.nowplaying+".mp3")
            self.isloop_play = False
        elif self.isloop_play and self.israndom_play:
            self.playlist = self.randomplaylist
            self.count = self.playlist.index(self.nowplaying+".mp3")
            self.isloop_play = False
        else:
            self.loopplaylist = [self.nowplaying+".mp3"]
            self.playlist = self.loopplaylist
            self.isloop_play = True
        self.button2.configure(image = self.loop_play_png if self.isloop_play else self.not_loop_play_png)   
    
    def next_song(self):
        self.ispause = False
        self.button1.configure(image = self.play_png if self.ispause else self.pause_png)
        mixer.music.stop()
        self.counter()
        mixer.music.load(self.playlist[self.count])
        mixer.music.play(loops = 0)
        self.nowplaying = self.playlist[self.count]
        self.nowplaying = self.nowplaying.replace(".mp3","")
        self.label_text.set(self.nowplaying.replace("downloads\\",""))
        
    def previous_song(self):
        self.ispause = False
        self.button1.configure(image = self.play_png if self.ispause else self.pause_png)
        mixer.music.stop()
        self.decounter()
        mixer.music.load(self.playlist[self.count])
        mixer.music.play(loops = 0)
        self.nowplaying = self.playlist[self.count]
        self.nowplaying = self.nowplaying.replace(".mp3","")
        self.label_text.set(self.nowplaying.replace("downloads\\",""))
          
    def set_volume(self,volume):
        mixer.music.set_volume(volume)
        
    def stop(self):
        mixer.music.stop()
        self.window.destroy()
        sys.exit()
        
    def play(self):
        while True:
            if not mixer.music.get_busy() and not self.ispause:
                self.next_song()
            sleep(0.25)
        
    def Goback(self):
        self.background.destroy()
        mixer.music.stop()
        Main_GUI(self.window)
        
class Main_GUI:
    def __init__(self, master = None):
        self.window = master
        self.window.title("Main GUI")
        self.window.geometry("737x550")
        self.window.resizable(False,False)
        self.buttonPath = os.getcwd()+'//button'
        
        self.main_background = photoconverter(self.buttonPath+'\\main_background.png',1106,825)
        self.main_download = photoconverter(self.buttonPath+'\\main_download.png',369,198)
        self.main_play = photoconverter(self.buttonPath+'\\main_play.png',263,167)
        self.main_search = photoconverter(self.buttonPath+'\\main_search.png',369,198)
        
        self.background = Canvas(self.window, width = 737, height = 550)
        self.background.pack(fill= "both" ,expand = True)
        self.background.create_image(737//2,550//2, image = self.main_background)
        
        
        self.btDownloader = Button(self.background, image = self.main_download , command = self.toDownloader,relief = FLAT,bg = "#347B36", bd = 0 , activebackground = "#347B36", highlightthickness = 0)
        self.background.create_window(185,297,window = self.btDownloader)
        self.btPlayer = Button(self.background, image = self.main_play, command = self.toPlayer ,relief = FLAT,bg = "#347B36", bd = 0 , activebackground = "#347B36", highlightthickness = 0) 
        self.background.create_window(144,444,window = self.btPlayer)
        self.btSearch = Button(self.background, image = self.main_search , command = self.toSearch ,relief = FLAT,bg = "#347B36", bd = 0 , activebackground = "#347B36", highlightthickness = 0) 
        self.background.create_window(171,128,window = self.btSearch)
    
        self.window.mainloop()
        
    def toDownloader(self):
        self.background.destroy()
        Downloader_GUI(self.window)
        
    def toSearch(self):
        self.background.destroy()
        Search_GUI(self.window)
        
    def toPlayer(self):
        self.background.destroy()
        Player_GUI(self.window)
               
class Checkbar_radiobutton(Button):
    def __init__(self, container, image = None, command = None, i=0, check = False):
        super().__init__()
        self.i = i
        self.check = check
        self.background = container
        self.buttonPath = os.getcwd()+'//button'
        self.download_type_single = photoconverter(self.buttonPath+'\\download_type_single.png',607,98)
        self.download_type_playlist = photoconverter(self.buttonPath+'\\download_type_playlist.png',484,121)
        self.bt = Button(self.background, image = self.download_type_single, command = self.ChangeStatus,relief = FLAT,bg = "#347B36", bd = 0 , activebackground = "#000000", highlightthickness = 0)
        self.background.create_window(535, 440, window = self.bt)
        
    def ChangeStatus(self):
        if self.check:
            self.bt.configure(image = self.download_type_single)
            self.check = False
            self.i = 0
        else:
            self.bt.configure(image = self.download_type_playlist)
            self.check = True
            self.i = 1
            
window = Tk()
Main_GUI(window)
#window.mainloop()
