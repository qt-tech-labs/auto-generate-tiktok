from pydoc import cli
import newspaper
import nltk
import ssl

from gtts import gTTS

from moviepy.editor import *
from moviepy.video.fx.resize import resize

import requests
import os

from youtube import search_by_text, download

OUTPUT = "output/"
IMAGES = "images"
VIDEOS = "videos"

LINKS = [
    "https://vnexpress.net/nghi-pham-khai-len-ke-hoach-am-sat-ong-abe-tu-mot-nam-truoc-4486605.html",
    "https://vnexpress.net/doi-an-ninh-bao-ve-ong-abe-la-ai-4485632.html",
    "https://vnexpress.net/qua-khu-han-thu-cua-nghi-pham-am-sat-ong-abe-4486052.html",
    "https://vnexpress.net/chien-binh-nuoc-ngoai-vo-mong-o-ukraine-4484866.html"
]


def log(str):
    print(str)


def delete_images(folder):
    log('Clean the folder: ' + str(folder))
    for file in os.listdir(folder):
        if file not in ['catnews.jpg', 'catnews_bg.jpg']:
            os.remove(str(folder) + '/' + file)


def save_image(url):
    try:
        substring = 'logo'
        log('Saving img: ' + str(url))
        filename = url.split('/')[-1]
        if filename != None and substring in filename.lower():
            print("Logo!")
            return None
        img_data = requests.get(url).content
        full_path = str('images/') + str(filename)+'.jpg'
        with open(full_path, 'wb') as handler:
            handler.write(img_data)

        return full_path
    except:
        print("Save image failed!")
        return None


def get_summary_of_page(url = None):
    if url is None or url == "":
        url = input("Enter the url: ")
    page = newspaper.Article(url, language='vi')
    page.download()
    page.parse()

    page.nlp()

    return (page.title, page.images, page.movies, page.summary, page.keywords)


def text_to_speak(str):
    tts = gTTS(str, lang='vi')
    tts.save('audios/news.mp3')


def compose_video(title, images):

    BLACK = (0, 0, 0)
    VIDEO_SIZE = (1080, 1920)

    image_len = len(images)

    # clip = ImageSequenceClip(images, 2)

    audio = AudioFileClip("audios/news.mp3").fx(vfx.speedx, 1.25)

    audio_duration = audio.duration

    frame_duration = audio_duration / image_len

    image_frames = []

    # bg clip

    # bg_clip = ImageClip("images/catnews.jpg", duration=0.1)
    # bg_clip = bg_clip.set_start(0).set_position("center")

    # # end_clip.set_audio(end_sound)
    # image_frames.append(bg_clip)

    for idx, img in enumerate(images):
        im_clip = ImageClip(img, duration=frame_duration)
        w, h = im_clip.size

        ratio = VIDEO_SIZE[0] / w

        resized = im_clip.fx(resize, ratio).set_start(
            idx * frame_duration).set_position("center").crossfadein(1)
        image_frames.append(resized)

    end_sound = AudioFileClip("audios/end.mp3")
    end_duration = end_sound.duration
    end_clip = ImageClip("images/catnews.jpg", duration=end_duration)
    end_clip = end_clip.set_start(
        audio_duration).set_position("center").crossfadein(1)
    # end_clip.set_audio(end_sound)
    image_frames.append(end_clip)

    top_title = TextClip(title, fontsize=50, size=(
        VIDEO_SIZE[0]/2, None), bg_color='white', method='caption',  align='center')
    configed_title = top_title.set_position(("center", 0.4)).set_duration(
        audio_duration).margin(top=200, opacity=0)

    image_frames.append(configed_title)

    clip = CompositeVideoClip(image_frames, VIDEO_SIZE)

    full_audio = CompositeAudioClip(
        [audio, end_sound.set_start(audio_duration)])

    aclip = clip.set_audio(full_audio)

    aclip.write_videofile(str(OUTPUT) + str(title) +
                          ".mp4", fps=24, audio_codec='aac')

def compose_fr_video(title, file_name):
    VIDEO_SIZE = (1080, 1920)
    clips = []
    videof = VideoFileClip(filename= file_name, audio=False)

    video_duration = videof.duration

    audio = AudioFileClip("audios/news.mp3")

    audio_duration = audio.duration


    end_sound = AudioFileClip("audios/end.mp3")
    end_duration = end_sound.duration

    full_audio = CompositeAudioClip([audio, end_sound.set_start(audio_duration)])

    buff = 0
    if audio_duration < video_duration:
        videof = videof.subclip(0, audio_duration)
    else:
        buff = audio_duration - video_duration
        # if buff / 2 > 2:
        #     # add image to it
        #     image_len = len(images)

        #     audio_duration = audio.duration

        #     frame_duration = audio_duration / image_len

        #     image_frames = []

        #     for idx, img in enumerate(images):
        #         im_clip = ImageClip(img, duration=frame_duration)
        #         w, h = im_clip.size

        #         ratio = VIDEO_SIZE[0] / w

        #         resized = im_clip.fx(resize, ratio).set_start(
        #             idx * frame_duration).set_position("center").crossfadein(1)
        #         image_frames.append(resized)
        # Do above later

    clips.append(videof.set_start(0).set_position("center").crossfadein(1))
    end_clip = ImageClip("images/catnews.jpg", duration=end_duration + buff)
    end_clip = end_clip.set_start(
        audio_duration + buff).set_position("center").crossfadein(1)
    # end_clip.set_audio(end_sound)
    clips.append(end_clip)

    

    # top_title = TextClip(title, fontsize=50, size=(
    #     VIDEO_SIZE[0]/2, None), bg_color='white', method='caption',  align='center')
    # configed_title = top_title.set_position(("center", 0.4)).set_duration(
    #     audio_duration).margin(top=200, opacity=0)

    # clips.append(configed_title)

    clip = CompositeVideoClip(clips, VIDEO_SIZE)

    aclip = clip.set_audio(full_audio)

    aclip.write_videofile(str(OUTPUT) + str(title) +
                          ".mp4", fps=24, audio_codec='aac')

def generate(url):
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    nltk.download('punkt')
    title, images, videos, summary, keywords = get_summary_of_page(url)
    log("Text to speak")
    text_to_speak(summary)

    delete_images(IMAGES)
    delete_images(VIDEOS)
    log("Save images")
    imgs = []
    for img in images:
        path = save_image(img)
        if path is not None:
            imgs.append(path)
    log("Images to video")

    # not enough to create a video from images
    if len(imgs) < 0:
        # load video from yt
        text_search = ' '.join(keywords)
        result = search_by_text(text_search)[0]

        url = result['url_suffix']

        download(url)

        last_v = os.listdir('videos')[0]
        log('video file' + last_v)
        if last_v is not None:
            compose_fr_video(title, 'videos/' + last_v)
        else:
            log('Not any video file!')
    else:
        # 変更しない
        compose_video(title, imgs)                          

if __name__ == '__main__':

    for link in LINKS:
        generate(link)