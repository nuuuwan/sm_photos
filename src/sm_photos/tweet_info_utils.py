import os

from utils import JSONFile

from sm_photos._constants import DIR_TWTR_DATA
from sm_photos._utils import log


def load_tweet_info_list():
    tweet_info_list = []
    for file_name_only in os.listdir(DIR_TWTR_DATA):
        if file_name_only[-5:] != '.json':
            continue
        tweet_info = JSONFile(
            os.path.join(DIR_TWTR_DATA, file_name_only)
        ).read()
        tweet_info_list.append(tweet_info)
    log.info(f'Loaded {len(tweet_info_list)} tweet infos')

    tweet_info_list = sorted(
        tweet_info_list,
        key=lambda tweet_info: -tweet_info['time_create_ut'],
    )
    return tweet_info_list
