from tkinter import *
import tkinter.messagebox
#from m1 import youtube_downloader
from selenium import webdriver
from time import sleep
import time
import os
#import requests
import re

from bs4 import BeautifulSoup
from pygame import mixer
from PIL import Image
from PIL import ImageTk

class youtube_downloader:
    def __init__(self,url,single_video,playlist):
        self.url = url
        self.single_video = single_video
        self.playlist = playlist
        self.saveDirectory=os.getcwd()
        self.filenum = self.filenumcounter(self.saveDirectory+"\\downloads")
        
        #chrome options config    
        prefs = {
                'profile.default_content_setting_values':
                    {
                        'notifications':2    
                    },
                'download.default_directory':self.saveDirectory+"\\downloads"
                }
                    
        chromedriver = self.saveDirectory+"\\chromedriver"
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_experimental_option('prefs', prefs)
        options.add_argument("disable-infobars")
        self.driver = webdriver.Chrome(chromedriver,options=options)
        
        self.main()
    
    def urlconvert(self,url):
        return url.replace("youtube","youtubeto")
    
    def playlist_to_url(self,url):
        pre = re.match(r"(https?:\/\/www\.youtube\.com[^&]*)",url).group()
        return self.urlconvert(pre)
    def main(self):
        valid = True
        if self.single_video:
            match_url = re.match(r"(https?:\/\/www\.youtube\.com[^&]*)",self.url)
            if match_url==None:
                print("Invalid url, please try again.")
                valid = False
                    
            else:
                url = match_url.group()
                url = self.urlconvert(url)
                self.single_video_download(url)
        
                    
        elif self.playlist:
            match_url = re.match(r"(https?:\/\/www\.youtube\.com).*&?(list=.*)",self.url)
            if match_url==None:
                print("Invalid url or this url doesn't from a playlist, please try again.")
                valid = False
                    
            else:
                playlist_url = match_url.group(1)+"/playlist?"+match_url.group(2)
                self.playlist_download(playlist_url)
                
        
        sleep(3)     
        t = threading.Thread(target = self.is_downloaded)
        t.setDaemon(True)
        t.start()
    
    def single_video_download(self,url,isfirst=True):
            self.driver.get(url)
            sleep(2)
            #print(requests.get(url).text)
            if isfirst:
                self.driver.switch_to.frame("IframeChooseDefault")
                self.driver.find_element_by_id("MP3Format").click()
            
            #driver.find_element_by_id("DownloadMP3_text").click()
            
    def playlist_download(self,url,choose_lst=[5,7,9]): #choose_lst contain urls that users choose to download
            self.driver.get(url)
            sleep(1)
            self.get_playlist_info(url)
            self.choose_download(choose_lst)
            
    def get_playlist_info(self,url):
            self.playlist_title = ""
            self.playlist_video_number = int()
            self.playlist_urls = []
            self.playlist_video_titles = [] 
            self.playlist_thumbnails_source = []
            bs = BeautifulSoup(self.driver.page_source,"html.parser")
            
            title = bs.find("yt-formatted-string",{"class":"style-scope ytd-playlist-sidebar-primary-info-renderer"})
            self.playlist_title = title.find("a").text
            
            video_num = bs.find("div",{"id":"stats"}).find("yt-formatted-string").text
            self.playlist_video_number = int(re.match(r"[0-9]*",video_num).group())
            
            inf = bs.find_all("ytd-playlist-video-renderer")
            
            for information in inf:
                url = information.find("a").get("href")
                self.playlist_urls.append("https://www.youtube.com"+url)
                
                video_title = information.find("span",{"id":"video-title"}).get("title")
                self.playlist_video_titles.append(video_title)
            
            length = self.playlist_video_number
            count = 0
            while count<length:
            
                thumbnail_source = inf[count].find("yt-img-shadow").find("img").get("src")
                if thumbnail_source == None:
                    self.driver.execute_script("window.scrollBy(0,505)")
                    sleep(0.01)
                    bs = BeautifulSoup(self.driver.page_source,"html.parser") #update website elements
                    inf = bs.find_all("ytd-playlist-video-renderer")
                    continue
                
                else:
                    if thumbnail_source in self.playlist_thumbnails_source:
                        continue
                    else:
                        self.playlist_thumbnails_source.append(thumbnail_source)
                        count+=1
                #print(count)
            #print(len(self.playlist_thumbnails_source))
            #print(self.playlist_urls)
            #print(len(self.playlist_video_titles))
    
    def choose_download(self,lst):
        for index in range(len(lst)):
            url = self.playlist_to_url(self.playlist_urls[lst[index]])
            self.single_video_download(url,True if index==0 else False)
            sleep(1)            
            
    def filenumcounter(self,path):
        current_path_tree = os.walk(path)
        count=0
        for file in current_path_tree:
            count+=len(file[2])
        
        return count
    
    def is_downloaded(self):
        a = time.time()
        while True:
            current_filenum = self.filenumcounter(self.saveDirectory+"\\downloads")
            if current_filenum > self.filenum :
                return True
            #print("Download Success, please waiting for download {} {}".format(current_filenum-self.filenum,"file" if current_filenum-self.filenum==1 else "files"))
            else:
                sleep(1)
                
            if time.time() - a < 5:
                return False
            #print("Download fail, maybe try again later")
            
        
#url=input()
#youtube_downloader(url,False,True)
#https://www.youtube.com/watch?v=iXjSxAwVPhY&list=RDiXjSxAwVPhY&start_radio=1
#https://www.youtube.com/watch?v=-P_ZyHiWRxs&list=PLnVSVW7VxYmKINpF7_QYJRM2g0v7I8hs6&index=2&t=0s&fbclid=IwAR2m6bnY8-H2yC_734W6Lij3MtlTrmsxBgpbord2lhzvMmk2ysZSuXcHXIo

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
        self.frame3.pack()
        label2 = Label(self.frame3, text = "Choose URL type: ")
        self.vtype = IntVar()
        rbtSingle = Radiobutton(self.frame3, text = "Single Video", variable = self.vtype, value = 1)
        rbtPlaylist = Radiobutton(self.frame3, text = "Playlist", variable = self.vtype, value = 2)
        label2.grid(row = 1, column = 1)
        rbtSingle.grid(row = 1, column = 2)
        rbtPlaylist.grid(row = 1, column = 3)
        
    def Download_video(self):
        #self.labeltext.set("Download processing...")
        if self.vtype.get() == 1:
            self.ytd = youtube_downloader(self.URL.get(), True, False)
        else:
            self.ytd = youtube_downloader(self.URL.get(), False, True)
        self.Showinfo()
        
    def Showinfo(self):
        if self.ytd.is_downloaded():
            tkinter.messagebox.showinfo("Status", "Download Success!")
        else:
            tkinter.messagebox.showwarning("Status", "Download failed, please try again later")
    
    def Goback(self):
        self.frame0.destroy()
        self.frame1.destroy()
        self.frame2.destroy()
        self.frame3.destroy()
        Main_GUI(self.window)


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
        self.window.geometry("300x350")
        
        self.frame = Frame(self.window)
        self.frame.pack(expand = 1)
        btDownloader = Button(self.frame, text = "Download videos", command = self.toDownloader)
        btPlayer = Button(self.frame, text = "Play music", command = self.toPlayer) 
        btSearch = Button(self.frame, text = "Search videos", command = self.toSearch) 
        btDownloader.pack(fill = BOTH, ipady = 5, pady = 5)
        btSearch.pack(fill = BOTH, ipady = 5, pady = 5)
        btPlayer.pack(fill = BOTH, ipady = 5, pady = 5)
        
    def toDownloader(self):
        self.frame.destroy()
        Downloader_GUI(self.window)
        
    def toSearch(self):
        self.frame.destroy()
        Search_GUI(self.window)
        
    def toPlayer(self):
        self.frame.destroy()
        Player_GUI(self.window)
        
window = Tk()
window.configure(background='white')
Main_GUI(window)
window.mainloop()
