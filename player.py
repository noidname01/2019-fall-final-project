from pygame import mixer
from tkinter import *
from PIL import Image
from PIL import ImageTk
import os
import random
import threading
import sys
from time import sleep

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
        import threading
        import random
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
        self.back_button = Button(self.background, image = self.back_png, command = None, relief = FLAT, bg = "#347B36", bd = 0 , activebackground = "#347B36", highlightthickness = 0)
        self.background.create_window(835,410,window = self.back_button)
        """
        self.valueBar = Scale(self.background,command = self.set_volume, from_= 100 , to = 0 , orient = "vertical", bg = "#FFFFFF", bd= 0 ,highlightthickness = 0 ,troughcolor="#000000", sliderrelief=SUNKEN, showvalue =0 )
        self.background.create_window(850,600,window = self.valueBar)
        self.valueBar.configure(width = 20)
        self.valueBar.set(self.volume)
        """
        self.slider_y = 680-self.volume/100*130
        self.background.create_image(860,self.slider_y, image = self.slider_png, tags="slider")
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
                self.slider_y = event.y_root
                
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
        
    """def Goback(self):
        self.background.destroy()
        mixer.music.stop()
        Main_GUI(self.window)
    """    
window = Tk()
Player_GUI(window)
window.mainloop()
