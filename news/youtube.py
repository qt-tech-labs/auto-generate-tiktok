from __future__ import unicode_literals
import json
from youtube_search import YoutubeSearch
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
    'format': 'bestvideo[ext=mp4]',
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
    'nocheckcertificate' : True,
    'verbose': 1,
    'outtmpl': 'output/%(title)s.%(ext)s',
    'getcomments': True,
    'writeinfojson': True,
    'postprocessors': [
        {
            'key': 'SponsorBlock', 
            'categories': ['sponsor']
        },
        {
            'key': 'ModifyChapters', 
            'remove_sponsor_segments': ['sponsor']
        }
    ]
}

def search_by_text(text, max = 2):
    results = YoutubeSearch(text, max_results=max).to_dict()
    return results

def download(video):
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com' + video])
        # info = ydl.extract_info('https://www.youtube.com' + video, download=False)

        # ℹ️ ydl.sanitize_info makes the info json-serializable
        # print(json.dumps(ydl.sanitize_info(info)))

if __name__ == '__main__':

    # For test
    result = search_by_text('gap nhau cuoi tuan')[0]

    suffix = result['url_suffix']

    download(suffix)
