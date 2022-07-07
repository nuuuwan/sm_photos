import argparse

from sm_photos import collage, dedupe, filesys, photos, summary, text_collage
from sm_photos.twtr import TWTR


def main(hashtag):
    filesys.init()
    twtr = TWTR()
    tweet_info_list = twtr.get_tweet_info_list(hashtag)
    for tweet_info in tweet_info_list:
        filesys.download_and_save(tweet_info)
    summary.build_summary()
    summary.build_readme()
    collage.build_collage()

    base_image_file = 'media/text.sketch.png'
    photo_file_list = dedupe.dedupe_photos(photos.get_photo_file_list())
    text_collage.build_text_collage(base_image_file, photo_file_list)
    text_collage.metarize()


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--hashtag', type=str)
    return parser.parse_args()


if __name__ == '__main__':
    options = get_options()
    main(options.hashtag)
