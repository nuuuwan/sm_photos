import os

from moviepy.editor import VideoFileClip

from sm_photos._constants import DIR_TWTR_DATA
from sm_photos._utils import log

MIN_SECONDS_PER_CLIP = 20
MAX_CLIPS = 10


def get_video_file_list():
    video_file_list = []
    for file_only in os.listdir(DIR_TWTR_DATA):
        ext = file_only.split('.')[-1]
        if ext not in ['mp4']:
            continue
        video_file_list.append(os.path.join(DIR_TWTR_DATA, file_only))
    video_file_list = list(reversed(list(sorted(video_file_list))))
    return video_file_list


def extract_and_save_clips(video_file):
    video = VideoFileClip(video_file)
    duration = video.duration
    n_clips = min(
        (int)(video.duration / MIN_SECONDS_PER_CLIP),
        MAX_CLIPS,
    )
    log.debug(f'{video_file}: {duration=}, {n_clips=}')

    video_clip_file_list = []
    for i_clip in range(0, n_clips + 1):
        t = (int)(duration * i_clip / (n_clips + 1))
        video_clip_file = video_file + f'.clip.{i_clip:02d}.png'
        video.save_frame(video_clip_file, t=t)
        log.info(f'Wrote {video_clip_file}')
        video_clip_file_list.append(video_clip_file)
    return video_clip_file_list


def backpopulate_video_clips():
    video_file_list = get_video_file_list()
    for video_file in video_file_list:
        first_video_clip_file = video_file + '.clip.00.png'

        if os.path.exists(first_video_clip_file):
            log.info(f'Clips already downloaded for {video_file}.')
        else:
            log.info(f'No clips for {video_file}. Extracting...')
            extract_and_save_clips(video_file)
