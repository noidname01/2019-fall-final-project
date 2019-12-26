from selenium import webdriver
from time import sleep
import time
import os
import requests
import re
from bs4 import BeautifulSoup
import re
import os
class Search:
    def __init__(self,keyword):
        self.keyword = keyword
        self.saveDirectory=os.getcwd()
        chromedriver = self.saveDirectory+"\\chromedriver"
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        
        self.driver = webdriver.Chrome(chromedriver,options=options)
        self.search()
        self.information_collector()
        
    def search(self):
        self.driver.get("https://www.youtube.com/")
        sleep(1)
        self.driver.find_element_by_id("search").send_keys(self.keyword)
        sleep(0.5)
        self.driver.find_element_by_id("search-icon-legacy").click()
        sleep(2)
        self.driver.find_element_by_xpath("//yt-icon[@class='style-scope ytd-toggle-button-renderer']").click()
        sleep(0.5)
        self.driver.find_element_by_xpath("//div[@title='搜尋「視訊」']").click()
        sleep(1)
        self.driver.find_element_by_xpath("//yt-icon[@class='style-scope ytd-toggle-button-renderer']").click()
        sleep(0.5)
        self.driver.find_element_by_xpath("//div[@title='按觀看次數排序']").click()
        sleep(1)
        
    def information_collector(self,):
        self.search_result_video_number = 20
        self.search_result_urls = []
        self.search_result_video_titles = [] 
        self.search_result_thumbnails_source = []
        
        for i in range(1,self.search_result_video_number+1):
            element = self.driver.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer["+str(i)+"]/div[1]/div/div[1]/div/h3/a")
            title = element.get_attribute("title")
            self.search_result_video_titles.append(title)
            
            url = element.get_attribute("href")
            self.search_result_urls.append(url)
            id1 = url.replace("https://www.youtube.com/watch?v=","")
            
            thumbnail_source = "https://i.ytimg.com/vi/"+id1+"/hqdefault.jpg?"
            self.search_result_thumbnails_source.append(thumbnail_source)
            
            self.driver.execute_script("window.scrollBy(0,138)")
            sleep(0.01)
            
        
        """
        length = self.search_result_video_number
        count = 0
        while count<length:
        
            thumbnail_source = inf[count].find("yt-img-shadow").find("img").get("src")
            #print(thumbnail_source)
            
            if thumbnail_source == None:
                sleep(0.01)
                self.driver.execute_script("window.scrollBy(0,276)")
                bs = BeautifulSoup(self.driver.page_source,"html.parser") #update website elements
                inf = bs.find("div",{"id":"content"}).find_all("ytd-video-renderer")
                inf = inf[:self.search_result_video_number] 
                continue
            else:
                self.search_result_thumbnails_source.append(thumbnail_source)
                count+=1              
            #print(count)
        """
        """
        for information in inf:
            url = information.find("a").get("href")
            self.search_result_urls.append("https://www.youtube.com"+url)
            
            id1 = url.replace("/watch?v=","")
            thumbnail_source = "https://i.ytimg.com/vi/"+id1+"/hqdefault.jpg?"
            self.search_result_thumbnails_source.append(thumbnail_source)
            
            video_title = information.find("a",{"id":"video-title"}).get("title")
            self.search_result_video_titles.append(video_title)
        """
        
        self.search_result = []
        for i in range(self.search_result_video_number):
            self.search_result.append((self.search_result_urls[i],self.search_result_video_titles[i],self.search_result_thumbnails_source[i]))
        #print(self.search_result)