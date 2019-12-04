from selenium import webdriver
from time import sleep
import time
import os
import requests
import re
from bs4 import BeautifulSoup

class Search:
    def __init__(self,keyword):
        self.keyword = keyword
        self.saveDirectory=os.getcwd()
        chromedriver = self.saveDirectory+"\\chromedriver"
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        
        self.driver = webdriver.Chrome(chromedriver,options=options)
        self.search()
        self.information_collector()
        
    def search(self):
        self.driver.get("https://www.youtube.com/")
        sleep(1)
        self.driver.find_element_by_id("search").send_keys(self.keyword)
        self.driver.find_element_by_id("search-icon-legacy").click()
        sleep(1)
        self.driver.find_element_by_xpath("//yt-icon[@class='style-scope ytd-toggle-button-renderer']").click()
        self.driver.find_element_by_xpath("//div[@title='搜尋「視訊」']").click()
        sleep(1)
        self.driver.find_element_by_xpath("//yt-icon[@class='style-scope ytd-toggle-button-renderer']").click()
        self.driver.find_element_by_xpath("//div[@title='按觀看次數排序']").click()
        
    def information_collector(self):
        self.search_result_video_number = 20
        self.search_result_urls = []
        self.search_result_video_titles = [] 
        self.search_result_thumbnails_source = []
        bs = BeautifulSoup(self.driver.page_source,"html.parser")
        
        inf = bs.find_all("ytd-video-renderer")
        inf = inf[:self.search_result_video_number]
        
        length = self.search_result_video_number
        count = 0
        while count<length:
        
            thumbnail_source = inf[count].find("yt-img-shadow").find("img").get("src")
            #print(thumbnail_source)
            
            if thumbnail_source == None:
                sleep(0.01)
                self.driver.execute_script("window.scrollBy(0,276)")
                bs = BeautifulSoup(self.driver.page_source,"html.parser") #update website elements
                inf = bs.find_all("ytd-video-renderer")
                inf = inf[:self.search_result_video_number+1] 
                continue
            else:
                self.search_result_thumbnails_source.append(thumbnail_source)
                count+=1              
            #print(count)
        for information in inf:
            url = information.find("a").get("href")
            self.search_result_urls.append("https://www.youtube.com"+url)
            
            video_title = information.find("a",{"id":"video-title"}).get("title")
            self.search_result_video_titles.append(video_title)
        
        #print(len(self.search_result_thumbnails_source))
        #print(len(self.search_result_urls))
        #print(len(self.search_result_video_titles))
        
        self.search_result = []
        for i in range(self.search_result_video_number):
            self.search_result.append((self.search_result_urls[i],self.search_result_video_titles[i],self.search_result_thumbnails_source[i]))
        
        print(self.search_result)
a=time.time() 
Search("TWICE")
b=time.time()
print(b-a)