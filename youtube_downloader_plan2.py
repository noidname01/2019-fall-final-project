import os
from selenium import webdriver
import requests
import re
from time import sleep
from bs4 import BeautifulSoup
import threading
import shutil
import tkinter.messagebox

class youtube_downloader:
    def __init__(self,url = None,single_video = None,playlist = None,progressbar = None):
        self.url = url
        self.single_video = single_video
        self.playlist = playlist
        self.progressbar = progressbar
        self.saveDirectory=os.getcwd()
        self.filenum = self.filenumcounter(self.saveDirectory+'\\downloads')
        self.is_downloaded = False
        self.thread = []
        
        #chrome options config    
        prefs = {
                'profile.default_content_setting_values':
                    {
                        'notifications':2    
                    },
                'download.default_directory':self.saveDirectory+'\\downloads'
                }
                    
        chromedriver = self.saveDirectory+"\\chromedriver"
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_experimental_option('prefs', prefs)
        options.add_argument("disable-infobars")
        self.driver = webdriver.Chrome(chromedriver,options=options)
    
    def urlconvert(self,url):
        return url.replace("youtube","youtubeto")
    
    def playlist_to_url(self,url):
        pre = re.match(r"(https?:\/\/www\.youtube\.com[^&]*)",url).group()
        return self.urlconvert(pre)
    
    def single_video_download(self,url,isfirst=True):
            while not self.is_downloaded:
                self.driver.get(url)
                sleep(1)
                #print(requests.get(url).text)
                if isfirst:
                    self.driver.switch_to.frame("IframeChooseDefault")
                    self.driver.find_element_by_id("MP3Format").click()
                break
            #driver.find_element_by_id("DownloadMP3_text").click()
            
    def playlist_download(self,url): #choose_lst contain urls that users choose to download
            self.driver.get(url)
            sleep(1)
            self.progressbar["value"] = 20
            self.get_playlist_info(url)
            
    def get_playlist_info(self,url):
            self.stage = 1
            self.playlist_title = ""
            self.playlist_video_number = int()
            self.playlist_urls = []
            self.playlist_video_titles = [] 
            self.playlist_thumbnails_source = []
            bs = BeautifulSoup(self.driver.page_source,"html.parser")
            
            title = bs.find("yt-formatted-string",{"class":"style-scope ytd-playlist-sidebar-primary-info-renderer"})
            self.playlist_title = title.find("a").text
            
            video_num = bs.find("div",{"id":"stats"}).find("yt-formatted-string").text
            #print(video_num)
            self.playlist_video_number = int(re.findall(r"([0-9]+)",video_num)[0])
            #print(self.playlist_video_number)
            inf = bs.find_all("ytd-playlist-video-renderer")
            
            length = self.playlist_video_number
            count = 0
            while count<length:
                if count%100 == 0 and count!=0:
                    sleep(2)
                    bs = BeautifulSoup(self.driver.page_source,"html.parser") #update website elements
                    inf = bs.find_all("ytd-playlist-video-renderer")
                    
                video_title = inf[count].find("span",{"id":"video-title"}).get("title")
                if video_title == "[已刪除影片]" or video_title == "[私人影片]" :
                    self.driver.execute_script("window.scrollBy(0,101)")
                    count  += 1
                    continue
                
    
                self.playlist_video_titles.append(video_title)  
                    
                
                url = inf[count].find("a").get("href")
                if not url in self.playlist_urls:
                    self.playlist_urls.append("https://www.youtube.com"+url)
                    id1 = re.search(r"\/watch\?v=(.+)&list",url).group(1)
                    thumbnail_source = "https://i.ytimg.com/vi/"+id1+"/hqdefault.jpg?"
                    self.playlist_thumbnails_source.append(thumbnail_source)
                    count+=1
                self.driver.execute_script("window.scrollBy(0,101)")
                sleep(0.01)
                
                self.progressbar["value"] = 20 + (20/length)*count
                #thumbnail_source = inf[count].find("yt-img-shadow").find("img").get("src")
            #print(len(self.playlist_thumbnails_source))
            #print(len(self.playlist_urls))
            #print(len(self.playlist_video_titles))
            self.playlist_information = []
            for i in range(len(self.playlist_thumbnails_source)):
                self.playlist_information.append((self.playlist_urls[i],self.playlist_video_titles[i],self.playlist_thumbnails_source[i]))
            self.progressbar["value"] = 50
            self.thumbnail_getter()
            #print(self.playlist_information)
    def choose_download(self,lst):
        t = threading.Thread(target = self.is_downloadedChecker)
        t.setDaemon(True)
        t.start()
        
        for i in range(len(lst)):
            url = lst[i]
            self.single_video_download(url,True if i == 0 else False)
            sleep(5)
            self.progressbar["value"] += 100/len(lst)
        """
        for index in range(len(lst)):
            url = self.playlist_to_url(self.playlist_urls[lst[index]])
            self.single_video_download(url,True if index == 0 else False)
            sleep(2)            
         """  
    def filenumcounter(self,path):
        current_path_tree = os.walk(path)
        count=0
        for file in current_path_tree:
            count += len(file[2])
        
        return count
    
    def is_downloadedChecker(self):
        while True:
            current_filenum = self.filenumcounter(self.saveDirectory+'downloads')
            if current_filenum > self.filenum :
                self.filenum = current_filenum
                self.is_downloaded = True
            else:
                self.is_downloaded = False
            
            sleep(3)
        
    def thumbnail_downloader(self,url,title):
        import cv2
        import numpy as np
        #import requests
        
        resp = requests.get(url, stream=True).raw
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        cv2.imwrite('playlist\\'+title+'.png', image)
        print(title+'.png Success!')
        
    def thumbnail_getter(self):
        for i in range(len(self.playlist_information)):
            url = self.playlist_information[i][2]
            #title = self.playlist_information[i][1]
            self.thumbnail_downloader(url,str(i))
            self.progressbar["value"] = 50 + (50/len(self.playlist_information))*(i+1)
            """
            self.thread.append(threading.Thread(target = self.thumbnail_downloader, args=(url,str(i),)))
            self.thread[i].start()
            self.thread[i].join()
            """
        
    def clear(self):
        shutil.rmtree(self.saveDirectory+"\\playlist")
        os.mkdir(self.saveDirectory+"\\playlist")
                
    """     main program starting here   """""
    def main(self):
        self.progressbar["value"]= 10
        while True:
            if self.single_video:
                match_url = re.match(r"(https?:\/\/www\.youtube\.com[^&]*)",self.url)
                if match_url==None:
                    tkinter.messagebox.showwarning("Status","Invalid url, please try again.")
                    break
                else:
                    url = match_url.group()
                    url = self.urlconvert(url)
                    self.single_video_download(url)
                    self.progressbar["value"] = 20
                    for i in range(4):
                        self.progressbar["value"] = 40 + i*20
                        sleep(0.5)
                    
            elif self.playlist:
                match_url = re.match(r"(https?:\/\/www\.youtube\.com).*&?(list=.*)",self.url)
                if match_url==None:
                    tkinter.messagebox.showwarning("Status","Invalid url or this url doesn't from a playlist, please try again.")
                    break
                else:
                    playlist_url = match_url.group(1)+"/playlist?"+match_url.group(2)
                    self.playlist_download(playlist_url)
                    break
        
        t = threading.Thread(target = self.is_downloadedChecker)
        t.setDaemon(True)
        t.start()
        