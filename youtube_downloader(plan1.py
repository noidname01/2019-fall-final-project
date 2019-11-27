import requests
import urllib.parse
import shutil
import re
import os
from time import sleep
url = input()
res = requests.get(url)
res.encoding="unicode"

keys = re.findall(r'https?%3A%2F%2Fr[^,\\]+', res.text)
#print(keys)
title = re.search(r'<title>([^<]+)', res.text)
name = title.group(1)
realname=""
for i in name:
    if i.isalnum() or i.isspace():
        realname+=i
#print(realname)
a= urllib.parse.unquote(keys[-1], encoding='utf-8', errors='replace')
res2 = requests.get(a, stream=True)
with open("{}.mp3".format(realname),"wb") as f:
    shutil.copyfileobj(res2.raw,f)
sleep(2)
if os.path.getsize("{}.mp3".format(realname))==0:
    print("Fail")
else:
    print("Success")