from selenium import webdriver
from time import sleep
import os
import requests
import re

def urlconvert(url):
    return url.replace("youtube","youtubeto")



while True:
    url=input()
    url = re.match(r"(https?:\/\/www\.youtube\.com[^&]*)",url)
    
    if url ==None:
        print("invalid url, try again.")
    else:
        url = url.group()
        url = urlconvert(url)
        break
#chrome options config
saveDirectory=os.getcwd()
prefs = {
        'profile.default_content_setting_values':
            {
                'notifications':2    
            },
        'download.default_directory':saveDirectory
        }
            
chromedriver = saveDirectory+"\\chromedriver"
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_experimental_option('prefs', prefs)
options.add_argument("disable-infobars")
driver = webdriver.Chrome(chromedriver,options=options)
#main
driver.get(url)
sleep(2)
#print(requests.get(url).text)
driver.switch_to.frame("IframeChooseDefault")
driver.find_element_by_id("MP3Format").click()
#driver.find_element_by_id("DownloadMP3_text").click()
 
#https://www.youtube.com/watch?v=iXjSxAwVPhY&list=RDiXjSxAwVPhY&start_radio=1
#https://www.youtube.com/watch?v=-P_ZyHiWRxs&list=PLnVSVW7VxYmKINpF7_QYJRM2g0v7I8hs6&index=2&t=0s&fbclid=IwAR2m6bnY8-H2yC_734W6Lij3MtlTrmsxBgpbord2lhzvMmk2ysZSuXcHXIo