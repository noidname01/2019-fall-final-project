from selenium import webdriver
from time import sleep
import os
import requests

class Search:
    def __init__(self,keyword,canvas):
        self.keyword = keyword
        self.saveDirectory=os.getcwd()
        chromedriver = self.saveDirectory+"\\chromedriver"
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(chromedriver,options=options)
        self.result_display = canvas
    
    def main(self):
        self.search()
        self.information_collector()
        self.thumbnail_getter()
        self.driver.quit()
        
    def search(self):
        self.driver.get("https://www.youtube.com/results?search_query="+self.keyword)
        sleep(1)
        self.result_display.create_arc(450,320,540,410,fill = "#367B34", tags = "loading", start = 90, extent = -24,outline="white")
        self.result_display.create_arc(470,340,520,390,fill = "white", tags = "loading",start = 90, extent = -24,outline="white")
        self.driver.find_element_by_xpath("//yt-icon[@class='style-scope ytd-toggle-button-renderer']").click()
        sleep(0.5)
        self.result_display.delete("loading")
        self.result_display.create_arc(450,320,540,410,fill = "#367B34", tags = "loading", start = 90, extent = -36,outline="white")
        self.result_display.create_arc(470,340,520,390,fill = "white", tags = "loading",start = 90, extent = -36,outline="white")
        self.driver.find_element_by_xpath("//div[@title='搜尋「視訊」']").click()
        sleep(1)
        self.result_display.delete("loading")
        self.result_display.create_arc(450,320,540,410,fill = "#367B34", tags = "loading", start = 90, extent = -60,outline="white")
        self.result_display.create_arc(470,340,520,390,fill = "white", tags = "loading",start = 90, extent = -60,outline="white")
        self.driver.find_element_by_xpath("//yt-icon[@class='style-scope ytd-toggle-button-renderer']").click()
        sleep(0.5)
        self.result_display.delete("loading")
        self.result_display.create_arc(450,320,540,410,fill = "#367B34", tags = "loading", start = 90, extent = -72,outline="white")
        self.result_display.create_arc(470,340,520,390,fill = "white", tags = "loading",start = 90, extent = -72,outline="white")
        self.driver.find_element_by_xpath("//div[@title='按觀看次數排序']").click()
        sleep(1)
        self.result_display.delete("loading")
        self.result_display.create_arc(450,320,540,410,fill = "#367B34", tags = "loading", start = 90, extent = -96,outline="white")
        self.result_display.create_arc(470,340,520,390,fill = "white", tags = "loading",start = 90, extent = -96,outline="white")
        
    def information_collector(self):
        self.result_display.delete("loading")
        self.result_display.create_arc(450,320,540,410,fill = "#367B34", tags = "loading", start = 90, extent = -100,outline="white")
        self.result_display.create_arc(470,340,520,390,fill = "white", tags = "loading",start = 90, extent = -100,outline="white")
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
            self.result_display.delete("loading")
            self.result_display.create_arc(450,320,540,410,fill = "#367B34", tags = "loading", start = 90, extent = -(100+6.5*i),outline="white")
            self.result_display.create_arc(470,340,520,390,fill = "white", tags = "loading",start = 90, extent = -(100+6.5*i),outline="white")
        
        self.search_result = []
        for i in range(self.search_result_video_number):
            self.search_result.append((self.search_result_urls[i],self.search_result_video_titles[i],self.search_result_thumbnails_source[i]))
        #print(self.search_result)
        
    def thumbnail_downloader(self,url,title):
        import cv2
        import numpy as np
        #import requests
        
        resp = requests.get(url, stream=True).raw
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        cv2.imwrite('search\\'+title+'.png', image)
        print(title+'.png Success!')
        
    def thumbnail_getter(self):
        for i in range(len(self.search_result)):
            url = self.search_result[i][2]
            #title = self.playlist_information[i][1]
            self.thumbnail_downloader(url,str(i))
            self.result_display.delete("loading")
            self.result_display.create_arc(450,320,540,410,fill = "#367B34", tags = "loading", start = 90, extent = -(230+6.5*(i+1)),outline="white")
            self.result_display.create_arc(470,340,520,390,fill = "white", tags = "loading",start = 90, extent = -(230+6.5*(i+1)),outline="white")
            