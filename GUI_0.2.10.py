from tkinter import *
import tkinter.messagebox
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

class Downloader_GUI:
    def __init__(self, master):
        self.window = master
        self.window.title("YouTube Video Downloader")
        self.window.geometry("800x500")
        
        image = Image.open("download_button.gif")
        self.photo = ImageTk.PhotoImage(image)
        
        self.frame0 = Frame(self.window, bg='white')
        self.frame0.pack(fill = BOTH)
        btGoback = Button(self.frame0, text = "Go back", command = self.Goback)
        btGoback.pack(side = LEFT)
        
        self.frame1 = Frame(self.window, bg='white')
        self.frame1.pack(fill = BOTH)
        #self.labeltext = StringVar()
        #self.labeltext.set("paste your URL below")
        self.label1 = Label(self.frame1, text = "Paste your URL below :")
        self.label1.pack()
        
        self.frame2 = Frame(self.window, bg='white')
        self.frame2.pack(pady = 10)
        self.URL = StringVar()
        entry = Entry(self.frame2, textvariable = self.URL)
        btDownload = Button(self.frame2, image = self.photo, command = self.Download_video ,highlightthickness = 0,bd = 0)
        entry.grid(row = 1, column = 1)
        btDownload.grid(row = 1, column = 2)
        
        self.frame3 = Frame(window, bg='white')
        self.frame3.pack(fill = BOTH)
        label2 = Label(self.frame3, text = "Choose URL type: ")
        label2.pack(side = LEFT)
        self.btCheckbar = Checkbar_radiobutton(self.frame3)
        '''self.vtype = IntVar()
        rbtSingle = Radiobutton(self.frame3, text = "Single Video", variable = self.vtype, value = 1)
        rbtPlaylist = Radiobutton(self.frame3, text = "Playlist", variable = self.vtype, value = 2)
        label2.grid(row = 1, column = 1)
        rbtSingle.grid(row = 1, column = 2)
        rbtPlaylist.grid(row = 1, column = 3)'''
        
    def Download_video(self):
        #self.labeltext.set("Download processing...")
        if self.btCheckbar.i == 0:
            self.ytd = youtube_downloader(self.URL.get(), True, False)
            self.Showinfo()
        else:
            self.ytd = youtube_downloader(self.URL.get(), False, True)
            self.frame0.destroy()
            self.frame1.destroy()
            self.frame2.destroy()
            self.frame3.destroy()
            Playlist_results_GUI(self.window,self.ytd.playlist_information)
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
        self.frame0.destroy()
        self.frame1.destroy()
        self.frame2.destroy()
        self.frame3.destroy()
        Main_GUI(self.window)
        
    

class Playlist_results_GUI:
    def __init__(self, master = None, lst=[]):
        self.window = master
        self.window.geometry("960x720")
        self.window.resizable(False,False)
        self.title = [x[1] for x in lst]
        self.frame0 = Frame(self.window, bg='white')
        self.frame0.pack(fill = BOTH)
        btGoback = Button(self.frame0, text = "Go back", command = self.Goback)
        btGoback.pack(side = LEFT)
        btDownload = Button(self.frame0, text = "Download", command = self.Download)
        btDownload.pack()
        
        self.frame1 = Frame(self.window)
        self.frame1.pack(fill=BOTH, expand = True)
        self.background = Canvas(self.frame1,width=960,height=720, scrollregion=(0,0,960,len(self.title)*110))
        self.vsb = Scrollbar(self.frame1,orient="vertical", command=self.background.yview)
        self.vsb.pack(side="right", fill="y")
        self.background.configure(yscrollcommand=self.vsb.set)
        self.background.pack(fill="both",side="left",expand = True)
        
        
        self.currentPath = os.getcwd()
        self.filelist = os.listdir(self.currentPath+"\\src")
        self.lst =[]
        self.thumbnails = []
        for i in range(len(self.filelist)):
            image = Image.open(self.currentPath+"\\src\\"+str(i)+".png")
            image = image.resize((200,100))
            image = ImageTk.PhotoImage(image)
            self.thumbnails.append(image)
    
        for i in range(len(self.thumbnails)):
            b0 = Label(self.background, image = self.thumbnails[i])
            if len(self.title[i]) > 25:
                for j in range(25,len(self.title[i])):
                    if self.title[i][j] ==  " ":
                        self.title[i] = self.title[i][:j+1] + "\n" + self.title[i][j+1:]
                        break
            b1 = Label(self.background, text = self.title[i])
            b1.config(font = ("Arial", 16))
            b2 = Checkbar_checkbutton(i, False, self.lst, self.background)
            b2.configure(command = b2.ChangeStatus)
            self.background.create_window(110,60+(110*i), window = b0)
            self.background.create_window(465,60+(110*i), window = b1)
            self.background.create_window(830,60+(110*i), window = b2)
        

        self.window.mainloop()
        
    def Goback(self):
        self.frame0.destroy()
        self.frame1.destroy()
        #self.background.destroy()
        self.vsb.destroy()
        self.lst.clear()
        Downloader_GUI(self.window)

    def Download(self):
        print(self.lst)

class Search_GUI:
    def __init__(self, master = None):
        self.window = master
        self.window.title("Search YouTube Video(s)")
        self.window.geometry("800x500")
        
        self.frame0 = Frame(self.window)
        self.frame0.pack(fill = BOTH)
        btGoback = Button(self.frame0, text = "Go back", command = self.Goback)
        btGoback.pack(side = LEFT)
        
        self.frame1 = Frame(self.window)
        self.frame1.pack(fill = BOTH)
        self.label1 = Label(self.frame1, text = "Enter keywords below :")
        self.label1.pack()
        
        self.frame2 = Frame(self.window)
        self.frame2.pack(pady = 10)
        self.keyword = StringVar()
        entry = Entry(self.frame2, textvariable = self.keyword)
        btSearch = Button(self.frame2, text = "Search", command = self.Search_video)
        entry.grid(row = 1, column = 1)
        btSearch.grid(row = 1, column = 2)
        
    def Search_video(self):
        self.frame0.destroy()
        self.frame1.destroy()
        self.frame2.destroy()
        Search_Result_GUI(self.window, self.keyword)
        
    def Goback(self):
        self.frame0.destroy()
        self.frame1.destroy()
        self.frame2.destroy()
        #self.frame3.destroy()
        Main_GUI(self.window)


class Search_Result_GUI:
    def __init__(self, master = None, keyword = ""):
        self.window = master
        self.window.title("Search Results")
        self.window.geometry("800x500")
        
        self.frame0 = Frame(self.window)
        self.frame0.pack(fill = BOTH)
        btGoback = Button(self.frame0, text = "Go back", command = self.Goback)
        btGoback.pack(side = LEFT)
        
        self.frame1 = Frame(self.window)
        self.frame1.pack()
        label = Label(self.frame1, text = "Results")
        label.pack()
        # Results should be Search(keyword)
        
    def Goback(self):
        self.frame0.destroy()
        self.frame1.destroy()
        Search_GUI(self.window)
        

def photoconverter(src,x = None,y = None):
        photo = Image.open(src)
        if x == None or y == None:
            pass
        else:
            photo = photo.resize((int(2*x/3),int(2*y/3)))
        photo = ImageTk.PhotoImage(photo)
        
        return photo

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
        self.currentPath = os.getcwd()
        self.image = Image.open(self.currentPath + '\\2.png')
        self.image = ImageTk.PhotoImage(self.image)
        self.bt = Button(container, image = self.image, command = self.ChangeStatus)
        self.bt.pack()
        
    def ChangeStatus(self):
        if self.check:
            self.currentPath = os.getcwd()
            self.image = Image.open(self.currentPath + '\\2.png')
            self.image = ImageTk.PhotoImage(self.image)
            self.bt.configure(image = self.image)
            self.check = False
            self.i = 0
        else:
            self.currentPath = os.getcwd()
            self.image = Image.open(self.currentPath + '\\1.png')
            self.image = ImageTk.PhotoImage(self.image)
            self.bt.configure(image = self.image)
            self.check = True
            self.i = 1
            
'''class Checkbar_checkbutton(Button):
    def __init__(self, i, check, lst, *arg):
        super().__init__(*arg)
        self.i = i
        self.check = check
        self.currentPath = os.getcwd()
        self.image = Image.open(self.currentPath + '\\2.png')
        self.image = ImageTk.PhotoImage(self.image)
        self.configure(image = self.image)
        
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
            #print(lst)'''
            
window = Tk()
window.configure(background='white')
Main_GUI(window)
#window.mainloop()