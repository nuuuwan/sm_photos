import os

from moviepy.editor import ImageSequenceClip

from sm_photos import tweet_info_utils
from sm_photos._constants import DIR_DATA, DIR_TWTR_DATA
from sm_photos._utils import log

VIDEO_DURATION = 120


def get_photo_video_info_list(tweet_info_list):
    photo_video_info_list = []
    for tweet_info in tweet_info_list:
        time_create_ut = tweet_info['time_create_ut']
        local_media = tweet_info['local_media']
        image_file_only_list = (
            local_media['photo'] + local_media['video_clip']
        )

        for image_file_only in image_file_only_list:
            photo_video_info_list.append(
                dict(
                    time_create_ut=time_create_ut,
                    image_file_only=image_file_only,
                )
            )

    photo_video_info_list = sorted(
        photo_video_info_list,
        key=lambda d: d['time_create_ut'],
    )
    return photo_video_info_list


def build_photo_video(photo_video_info_list):
    n_clips = len(photo_video_info_list)

    image_file_list = list(
        map(
            lambda photo_video_info: os.path.join(
                DIR_TWTR_DATA,
                photo_video_info['image_file_only'],
            ),
            photo_video_info_list,
        )
    )

    fps = max(1, n_clips / VIDEO_DURATION)
    clip = ImageSequenceClip(image_file_list, fps=fps)
    photo_video_file = os.path.join(DIR_DATA, 'photo_video.mp4')
    clip.write_videofile(photo_video_file, fps=fps)
    log.info(f'Wrote {n_clips} clips to {photo_video_file}')


def build_photo_video_all(tweet_info_list):
    tweet_info_list = tweet_info_utils.load_tweet_info_list_expanded()
    photo_video_info_list = get_photo_video_info_list(tweet_info_list)
    build_photo_video(photo_video_info_list)


if __name__ == '__main__':
    import json

    photo_video_info_list = [
        dict(time_create_ut=i, image_file_only=f'test.{i + 1:05d}.png')
        for i in range(8)
    ]
    print(json.dumps(photo_video_info_list, indent=2))
    build_photo_video(photo_video_info_list)
