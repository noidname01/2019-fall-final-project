from pytube import YouTube
url = input()
yt=YouTube(url)
yt.streams.first().download()