from __future__ import unicode_literals
from yt_dlp import *



class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    # 'format': 'bestvideo[ext=mp4]',
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
    'nocheckcertificate' : True,
    'verbose': 1,
    # 'outtmpl': 'output/%(title)s.%(ext)s',
    'getcomments': True,
    'writeinfojson': True
}

def download(video):
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.tiktok.com/@neginira2'])

download('suffix')
