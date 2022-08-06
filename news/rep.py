from re import sub
from youtube import search_by_text, download

from moviepy.editor import *
from moviepy.video.fx.resize import resize

OUTPUT = "output/"
VIDEOS = "videos"

# pool = Semaphore(6)
segment = 0
sub_duration = 0
clip_start = 0
def delete_folder(folder):
    print('Clean the folder: ' + str(folder))
    for file in os.listdir(folder):
        os.remove(str(folder) + '/' + file)
def compose_fr_video(part, title, file_name):
    title = str(title) + "_P" + str(part + 1)
    try:
        VIDEO_SIZE = (1080, 1920)
        clips = []
        videof = VideoFileClip(filename= file_name)

        clip_end = clip_start + sub_duration

        print("start at:", clip_start, clip_end)

        w, h = videof.size

        ratio = VIDEO_SIZE[0] / w

        resized = videof.fx(resize, ratio)
        clips.append(resized.subclip(clip_start, clip_end).set_start(0).set_position("center").crossfadein(1))

        top_title = TextClip(title, fontsize=50, size=(
            VIDEO_SIZE[0]/2, None), bg_color='white', method='caption',  align='center')
        configed_title = top_title.set_start(0).set_position(("center", 0.4)).set_duration(
            sub_duration).margin(top=200, opacity=0)

        clips.append(configed_title)

        water_mark = TextClip(title, fontsize=30, size=(
            VIDEO_SIZE[0]/2, None), bg_color='white', align='center')
        configed_title = top_title.set_position((w - 100, h-100)).set_start(0).set_position(("center", 0.4)).set_duration(
            sub_duration).margin(top=200, opacity=0)

        clips.append(configed_title)

        clip = CompositeVideoClip(clips, VIDEO_SIZE).set_duration(sub_duration)

        clip.write_videofile(str(OUTPUT) + str(title) +
                            ".mp4", fps=24, audio_codec='aac')
    except:
        print("error at ", clip_start, clip_end)
    # finally:
    #     pool.release()               

if __name__ == "__main__":
    result = search_by_text("Review phim")[0]
    print (result)
    url = result['url_suffix']
    title = result['title']

    delete_folder(VIDEOS)
    # download('/watch?v=jBp6IG8DjqY')
    download(url)

    last_v = os.listdir('videos')[0]
    print('video file' + last_v)
    if last_v is not None:
        # compose_fr_video("title", 'videos/' + last_v)
        file_name = 'videos/' + last_v
        if segment == 0:
            videof = VideoFileClip(filename= file_name)
            video_duration = videof.duration

            segment = video_duration // 60

            sub_duration = video_duration / segment
        
        part = 0
        while True:
            # pool.acquire()
            # p = Process(target=compose_fr_video, args=(part, "title", 'videos/' + last_v)).start()
            print("=============" + str(part+1) + "=============")
            clip_start = sub_duration * part
            compose_fr_video(part, title, 'videos/' + last_v)
            part += 1
            if part == segment:
                break
    else:
        print('Not any video file!')