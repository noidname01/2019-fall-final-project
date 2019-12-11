from tkinter import *
import tkinter.messagebox
#from m1 import youtube_downloader
from selenium import webdriver
from time import sleep
import time
import os
import requests
import re
from bs4 import BeautifulSoup
from pygame import mixer

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
        a= time.time()
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
        self.is_downloaded()
        b = time.time()
        print(b-a)
            
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
        lst = os.listdir(path)
        count=len(lst)
        
        return count
    
    def is_downloaded(self):
        current_filenum = self.filenumcounter(self.saveDirectory+"\\downloads")
        if current_filenum > self.filenum :
            return True
            #print("Download Success, please waiting for download {} {}".format(current_filenum-self.filenum,"file" if current_filenum-self.filenum==1 else "files"))
        else:
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
        
        self.frame0 = Frame(self.window)
        self.frame0.pack(fill = BOTH)
        btGoback = Button(self.frame0, text = "Go back", command = self.Goback)
        btGoback.pack(side = LEFT)
        
        self.frame1 = Frame(self.window)
        self.frame1.pack(fill = BOTH)
        #self.labeltext = StringVar()
        #self.labeltext.set("paste your URL below")
        self.label1 = Label(self.frame1, text = "Paste your URL below :")
        self.label1.pack()
        
        self.frame2 = Frame(self.window)
        self.frame2.pack(pady = 10)
        self.URL = StringVar()
        entry = Entry(self.frame2, textvariable = self.URL)
        btDownload = Button(self.frame2, text = "Download", command = self.Download_video)
        entry.grid(row = 1, column = 1)
        btDownload.grid(row = 1, column = 2)
        
        self.frame3 = Frame(window)
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
        
class Player_GUI:
    def __init__(self, master = None):
        self.window = master
        self.window.title("Music Player")
        self.window.geometry("800x500")
        
        self.cur_path = os.getcwd()+'\\downloads'
        self.filelist = []
        self.ispause = False
        self.loop_play_times = 0
        self.isloop_play = False
        self.count = 0
        self.is_next_song = False
        self.volume = 0.3
        self.israndom_play = True
        
        mixer.init()
        #self.window = Tk()
        #self.window.geometry("800x380")
        #self.window.title("mp3 player")
        
        self.frame0 = Frame(self.window)
        self.frame0.pack(fill = BOTH)
        
        btGoback = Button(self.frame0, text = "Go back", command = self.Goback)
        btGoback.pack(side = LEFT)
        
        self.frame1 = Frame(self.window)
        self.frame1.pack()
        
        files = os.listdir(self.cur_path)
        #print(file_tree)
        self.filelist = []
        print(self.filelist)
    
        for file_index in range(len(files)):
            self.filelist.append('downloads\\'+ files[file_index])
            
        self.original_filelist = self.filelist+[]
        #print(self.filelist)
        
        self.pause_text = StringVar()
        self.pause_text.set("pause")
        self.loop_text = StringVar()
        self.loop_text.set("loop play")
        self.random_text = StringVar()
        self.random_text.set("random play")
        
        button1 = Button(self.frame1, textvariable =self.pause_text , width = 20 , command = self.pause)
        button1.grid(row = 0, column = 0, padx = 5, pady = 5)
        button2 = Button(self.frame1, textvariable =self.loop_text , width = 20, command = self.loop_play)
        button2.grid(row = 0, column = 1, padx = 5, pady = 5)
        button3 = Button(self.frame1, textvariable = self.random_text , width = 20, command = self.random_play)
        button3.grid(row = 0, column = 2, padx = 5, pady = 5)
        button4 = Button(self.frame1, text = "next song", width = 20, command = self.next_song)
        button4.grid(row = 0, column = 3, padx = 5, pady = 5)
        
        mixer.music.load(self.filelist[self.count])
        mixer.music.play(loops = 0)
        
        self.nowplaying = self.filelist[0]
        
        self.window.protocol("WM_DELETE_WINDOW",self.stop)
        #self.window.mainloop()
        
        
        
        
    def counter(self):
        if self.count == len(self.filelist)-1:
            self.count = 0
        else:
            self.count += 1
    
    def play(self):
        
        if not mixer.music.get_busy() and not self.ispause:
            
            self.next_song()
            
        
        """if self.is_next_song:
            self.is_next_song = False
            
            self.play()
            self.counter()
        else:
            self.counter()"""
            
        
        """if self.isloop_play and not mixer.music.get_busy():
            mixer.music.play(loops = -1)
        else:
            self.counter()"""
    def random_play(self):
        self.random_text.set("order play" if self.israndom_play else "random play")
        
        if self.israndom_play:
            
            random.shuffle(self.filelist)
            self.israndom_play = False
            
        else:
            self.filelist = self.original_filelist
            self.count = self.original_filelist.index(self.nowplaying)
            self.israndom_play = True
        
    def pause(self):
        
        if not self.ispause:
            mixer.music.pause()
            self.ispause = True
        else:
            mixer.music.unpause()
            self.ispause = False
            
        self.pause_text.set("play" if self.ispause else "pause")
    def loop_play(self):
        if self.isloop_play:
            
            if not mixer.music.get_busy() and not self.ispause:
                mixer.music.load(self.filelist[self.count])
                mixer.music.play(loops = -1)
                
            else:
                while not self.is_next_song:
                    if not mixer.music.get_busy() and not self.ispause:
                        mixer.music.load(self.filelist[self.count])
                        mixer.music.play(loops = -1)
                        break
                
        else:
            while not self.is_next_song:
                if not mixer.music.get_busy() and not self.ispause:
                        self.next_song()
                        break
        #self.loop_text.set("single play" if self.isloop_play else "loop play")
    def next_song(self):
        mixer.music.stop()
        self.counter()
        mixer.music.load(self.filelist[self.count])
        mixer.music.play(loops = 0)
        self.nowplaying = self.filelist[self.count]
        print(self.nowplaying)
        
    def set_volume(self,volume):
        mixer.music.set_volume(volume/100)
        
    def stop(self):
        mixer.music.stop()
        self.window.destroy()
        
    def Goback(self):
        self.frame0.destroy()
        self.frame1.destroy()
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
Main_GUI(window)
window.mainloop()
