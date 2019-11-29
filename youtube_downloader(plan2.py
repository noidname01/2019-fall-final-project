from selenium import webdriver
from time import sleep
import os
import requests
import re
from bs4 import BeautifulSoup

class youtube_downloader:
    def __init__(self,url,single_video,playlist):
        self.url = url
        self.single_video = single_video
        self.playlist = playlist
        self.saveDirectory=os.getcwd()
        self.filenum = self.filenumcounter(self.saveDirectory)
        
        #chrome options config    
        prefs = {
                'profile.default_content_setting_values':
                    {
                        'notifications':2    
                    },
                'download.default_directory':self.saveDirectory
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

    def main(self):

        while True:
            if self.single_video:
                match_url = re.match(r"(https?:\/\/www\.youtube\.com[^&]*)",self.url)
                if match_url==None:
                    print("Invalid url, please try again.")
                else:
                    url = match_url.group()
                    url = self.urlconvert(url)
                    self.single_video_download(url)
                    break
                    
            elif self.playlist:
                match_url = re.match(r"(https?:\/\/www\.youtube\.com).*&?(list=.*)",self.url)
                if match_url==None:
                    print("Invalid url or this url doesn't from a playlist, please try again.")
                else:
                    playlist_url = match_url.group(1)+"/playlist?"+match_url.group(2)
                    self.playlist_download(playlist_url)
                    break
        sleep(3)      
        self.is_downloaded()
            
    def single_video_download(self,url):
            self.driver.get(url)
            sleep(2)
            #print(requests.get(url).text)
            self.driver.switch_to.frame("IframeChooseDefault")
            self.driver.find_element_by_id("MP3Format").click()
            #driver.find_element_by_id("DownloadMP3_text").click()
            
    def playlist_download(self,url):
            self.driver.get(url)
            sleep(2)
            self.get_playlist_info(url)
            
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
            #print(len(self.playlist_urls))
            #print(len(self.playlist_video_titles))
                
            
    def filenumcounter(self,path):
        current_path_tree = os.walk(path)
        count=0
        for file in current_path_tree:
            count+=len(file[2])
        
        return count
    
    def is_downloaded(self):
        current_filenum = self.filenumcounter(self.saveDirectory)
        if current_filenum > self.filenum :
            print("Download Success, please waiting for download {} {}".format(current_filenum-self.filenum,"file" if current_filenum-self.filenum==1 else "files"))
        else:
            print("Download fail, maybe try again later")
        
url=input()
youtube_downloader(url,False,True)
#https://www.youtube.com/watch?v=iXjSxAwVPhY&list=RDiXjSxAwVPhY&start_radio=1
#https://www.youtube.com/watch?v=-P_ZyHiWRxs&list=PLnVSVW7VxYmKINpF7_QYJRM2g0v7I8hs6&index=2&t=0s&fbclid=IwAR2m6bnY8-H2yC_734W6Lij3MtlTrmsxBgpbord2lhzvMmk2ysZSuXcHXIo