from moviepy.editor import VideoFileClip

from sm_photos._utils import log

MIN_SECONDS_PER_CLIP = 60
MAX_CLIPS = 10


def extract_and_save_clips(video_file_name):
    video = VideoFileClip(video_file_name)
    duration = video.duration
    n_clips = min(
        (int)(video.duration / MIN_SECONDS_PER_CLIP),
        MAX_CLIPS,
    )
    log.debug(f'{video_file_name}: {duration=}, {n_clips=}')

    video_clip_file_list = []
    for i_clip in range(0, n_clips + 1):
        t = (int)(duration * i_clip / (n_clips + 1))
        video_clip_file = video_file_name + f'.clip.{i_clip:02d}.png'
        video.save_frame(video_clip_file, t=t)
        log.info(f'Wroted {video_clip_file}')
        video_clip_file_list.append(video_clip_file)
    return video_clip_file_list
