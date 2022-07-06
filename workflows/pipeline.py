import argparse

from sm_photos import filesys, photos, summary
from sm_photos.twtr import TWTR


def main(hashtag):
    filesys.init()
    twtr = TWTR()
    tweet_info_list = twtr.get_tweet_info_list(hashtag)
    for tweet_info in tweet_info_list:
        filesys.download_and_save(tweet_info)
    summary.build_summary()
    summary.build_readme()
    photos.build_collage()


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--hashtag', type=str)
    return parser.parse_args()


if __name__ == '__main__':
    options = get_options()
    main(options.hashtag)
