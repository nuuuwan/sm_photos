import argparse
# import os
# import shutil

from sm_photos import (collage, dedupe, filesys, photo_video, photos, readme,
                       summary, text_collage, videos)
from sm_photos._constants import DIR_TWTR_DATA
from sm_photos._utils import log
from sm_photos.twtr import TWTR


def main(hashtag):
    filesys.init()

    twtr = TWTR()
    tweet_info_list = twtr.get_tweet_info_list(hashtag)
    for tweet_info in tweet_info_list:
        filesys.download_and_save(tweet_info)

    videos.backpopulate_video_clips()
    summary.build_summary()

    collage.build_collage()
    base_image_file = 'media/text.sketch.png'
    photo_file_list = dedupe.dedupe_photos(photos.get_photo_file_list())
    text_collage.build_text_collage(base_image_file, photo_file_list)
    text_collage.metarize()
    readme.build_readme()

    try:
        photo_video.build_photo_video_all()
    except Exception as e:
        log.error(str(e))


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--hashtag', type=str)
    return parser.parse_args()


if __name__ == '__main__':
    options = get_options()
    main(options.hashtag)
