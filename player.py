from pygame import mixer
from tkinter import *
from PIL import Image
from PIL import ImageTk
import os
import random
import threading
import sys
from time import sleep

class Music_Player:
    def __init__(self):
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
        self.window = Tk()
        self.window.geometry("1200x800")
        self.window.title("mp3 player")
        self.window.configure(background = "#367B34")
        
        self.pause_png = Image.open(self.button_src+"\\pause.png" )
        self.pause_png = ImageTk.PhotoImage(self.pause_png)
        self.next_song_png = Image.open(self.button_src+"\\next_song.png")
        self.next_song_png = ImageTk.PhotoImage(self.next_song_png)
        self.previous_song_png = Image.open(self.button_src+"\\previous_song.png")
        self.previous_song_png = ImageTk.PhotoImage(self.previous_song_png)
        self.play_png = Image.open(self.button_src+"\\play.png")
        self.play_png = ImageTk.PhotoImage(self.play_png)
        self.loop_play_png = Image.open(self.button_src+"\\loop_play.png" )
        self.loop_play_png = ImageTk.PhotoImage(self.loop_play_png)
        self.random_play_png = Image.open(self.button_src+"\\random_play.png" )
        self.random_play_png = ImageTk.PhotoImage(self.random_play_png)
        
        frame1 = Frame(self.window, bg="#367B34")
        frame1.pack()
        
        file_tree = os.walk(self.cur_path)
        #print(file_tree)
        for i,j,files in file_tree:
            self.filelist = files
        
        print(self.filelist)
    
        for file_index in range(len(self.filelist)):
            self.filelist[file_index] = 'downloads\\'+ self.filelist[file_index]
            
        self.playlist = self.filelist+[]
        #print(self.filelist)
        
        """self.pause_text = StringVar()
        self.pause_text.set("play" if self.ispause else "pause")
        self.loop_text = StringVar()
        self.loop_text.set("single play" if self.isloop_play else "loop play")
        self.random_text = StringVar()
        self.random_text.set("order play" if self.israndom_play else "random play")
        """
        
        self.label_text = StringVar()
        self.volume = 30
        
        
        
        self.button1 = Button(frame1, image = self.pause_png  , command = self.pause, bg="#367B34")
        self.button1.grid(row = 0, column = 0, padx = 5, pady = 5)
        button2 = Button(frame1, image = self.loop_play_png , command = self.loop_play, bg="#367B34")
        button2.grid(row = 0, column = 1, padx = 5, pady = 5)
        button3 = Button(frame1, image = self.random_play_png , command = self.random_play, bg="#367B34")
        button3.grid(row = 0, column = 2, padx = 5, pady = 5)
        button4 = Button(frame1, image = self.next_song_png , command = self.next_song, bg="#367B34")
        button4.grid(row = 0, column = 3, padx = 5, pady = 5)
        button5 = Button(frame1, image = self.previous_song_png , command = self.previous_song, bg="#367B34")
        button5.grid(row = 0, column = 4, padx = 5, pady = 5)
        
        frame2 = Frame(self.window, bg="#367B34")
        frame2.pack()
        label = Label(frame2,textvariable = self.label_text)
        label.pack()
        
        frame3 = Frame(self.window, bg="#367B34")
        frame3.pack()
        valueBar = Scale(frame3,command = self.set_volume, from_= 0 , to = 100 , orient = "horizontal")
        valueBar.set(self.volume)
        valueBar.pack()
        
        mixer.music.load(self.playlist[self.count])
        mixer.music.set_volume(self.volume/100)
        mixer.music.play(loops = 0)
        self.nowplaying = self.playlist[self.count]
        self.label_text.set(self.nowplaying.replace("downloads\\",""))
        
        t = threading.Thread(target = self.play)
        t.setDaemon(True)
        t.start()
        
        self.window.protocol("WM_DELETE_WINDOW",self.stop)
        self.window.mainloop()
        
    
            
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
    
    def random_play(self):
        if not self.israndom_play:
            
            random.shuffle(self.playlist)
            self.label_text.set(self.nowplaying)
            self.israndom_play = True
            
        else:
            self.playlist = self.filelist
            self.count = self.playlist.index(self.nowplaying)
            self.israndom_play = False
        
        #self.random_text.set("order play" if self.israndom_play else "random play")
        
    def pause(self):
        if self.is_next_song:
            self.is_next_song = False
        
        if not self.ispause:
            mixer.music.pause()
            self.ispause = True
            self.button1.configure(image = self.play_png)
        else:
            mixer.music.unpause()
            self.ispause = False
            self.button1.configure(image = self.pause_png)
            
        self.button1.configure(image = self.play_png if self.ispause else self.pause_png)
        
        
    def next_song(self):
        self.ispause = False
        self.button1.configure(image = self.play_png if self.ispause else self.pause_png)
        mixer.music.stop()
        self.counter()
        mixer.music.load(self.playlist[self.count])
        mixer.music.play(loops = 0)
        self.nowplaying = self.playlist[self.count]
        self.label_text.set(self.nowplaying.replace("downloads\\",""))
        
    def previous_song(self):
        self.ispause = False
        self.button1.configure(image = self.play_png if self.ispause else self.pause_png)
        mixer.music.stop()
        self.decounter()
        mixer.music.load(self.playlist[self.count])
        mixer.music.play(loops = 0)
        self.nowplaying = self.playlist[self.count]
        self.label_text.set(self.nowplaying.replace("downloads\\",""))
        
    def loop_play(self):
        if self.isloop_play:
            self.playlist = self.filelist
            self.count = self.playlist.index(self.nowplaying)
            self.isloop_play = False
        else:
            self.playlist = [self.nowplaying]
            self.isloop_play = True
        
        #self.loop_text.set("single play" if self.isloop_play else "loop play")
        
    def set_volume(self,volume):
        mixer.music.set_volume(int(volume)/100)
        
    def stop(self):
        mixer.music.stop()
        self.window.destroy()
        sys.exit()
        
    def play(self):
        while True:
            if not mixer.music.get_busy() and not self.ispause:
                self.next_song()
            sleep(0.25)
        
Music_Player()
