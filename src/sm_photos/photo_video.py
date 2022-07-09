import os

import numpy
from moviepy.editor import ImageSequenceClip
from PIL import Image, ImageDraw
from utils import timex, www

from sm_photos import tweet_info_utils
from sm_photos._constants import DIR_DATA, DIR_TWTR_DATA, URL_REMOTE_TWTR_DATA
from sm_photos._utils import log

IMAGE_WIDTH = 640
IMAGE_HEIGHT = (int)(IMAGE_WIDTH * 9 / 16)
TESTING = False
MAX_IMAGES = 10 if TESTING else 2400
FPS = 1


def get_photo_video_info_list(tweet_info_list):
    photo_video_info_list = []
    for tweet_info in tweet_info_list:
        user = tweet_info['user']
        time_create_ut = tweet_info['time_create_ut']
        local_media = tweet_info['local_media']
        image_file_only_list = (
            local_media['photo'] + local_media['video_clip']
        )

        for image_file_only in image_file_only_list:
            photo_video_info_list.append(
                dict(
                    user=user,
                    time_create_ut=time_create_ut,
                    image_file_only=image_file_only,
                )
            )

    photo_video_info_list = sorted(
        photo_video_info_list,
        key=lambda d: -d['time_create_ut'],
    )
    n_photo_video_info_list = len(photo_video_info_list)
    log.info(f'Found {n_photo_video_info_list} clips for photo_video')
    return photo_video_info_list


def get_image(photo_video_info):
    image_file_only = photo_video_info['image_file_only']
    image_file = os.path.join(
        DIR_TWTR_DATA,
        image_file_only,
    )
    if TESTING and not os.path.exists(image_file):
        remote_url = os.path.join(
            URL_REMOTE_TWTR_DATA,
            image_file_only,
        )
        www.download_binary(remote_url, image_file)
        log.debug(f'Downloaded {remote_url} to {image_file}')
    image = Image.open(image_file)
    image = image.resize((IMAGE_WIDTH, IMAGE_HEIGHT))

    time_create_ut = photo_video_info['time_create_ut']
    time_create = timex.format_time(
        time_create_ut,
        timezone=timex.TIMEZONE_OFFSET_LK,
    )
    user = photo_video_info['user']
    text = time_create + " " + user

    draw = ImageDraw.Draw(image)
    draw.rectangle(
        ((0, IMAGE_HEIGHT - 20), (250, IMAGE_HEIGHT)),
        fill="black",
    )
    draw.text(
        (10, IMAGE_HEIGHT - 18),
        text,
        fill="white",
    )

    if image.size != (IMAGE_WIDTH, IMAGE_HEIGHT):
        return None

    return numpy.array(image)


def build_photo_video(photo_video_info_list):
    n_clips = len(photo_video_info_list)

    image_list = list(
        map(
            get_image,
            photo_video_info_list,
        )
    )

    image_list = list(
        filter(
            lambda x: isinstance(x, numpy.ndarray),
            image_list,
        )
    )

    clip = ImageSequenceClip(image_list, fps=FPS)
    photo_video_file = os.path.join(DIR_DATA, 'photo_video.mp4')
    clip.write_videofile(photo_video_file, fps=FPS)
    log.info(f'Wrote {n_clips} clips to {photo_video_file}')


def build_photo_video_all():
    tweet_info_list = tweet_info_utils.load_tweet_info_list_expanded()
    photo_video_info_list = get_photo_video_info_list(tweet_info_list)
    photo_video_info_list = photo_video_info_list[:MAX_IMAGES]
    build_photo_video(photo_video_info_list)


if __name__ == '__main__':
    build_photo_video_all()
