import os

from utils import JSONFile

from sm_photos import tweet_info_utils
from sm_photos._constants import DIR_DATA
from sm_photos._utils import log


def build_summary():
    tweet_info_list = tweet_info_utils.load_tweet_info_list()
    try:
        tweet_info_list = tweet_info_utils.expand_tweet_info_list(
            tweet_info_list
        )
    except Exception as e:
        log.error(str(e))

    tweet_info_list_file = os.path.join(DIR_DATA, 'tweet_info_list.json')
    JSONFile(tweet_info_list_file).write(tweet_info_list)
    log.info(f'Wrote {tweet_info_list_file}')
