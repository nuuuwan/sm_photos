import os

from utils import JSONFile

from sm_photos._constants import DIR_TWTR_DATA
from sm_photos._utils import log


def organize_media(file_only_list):
    media = {'photo': [], 'video': [], 'video_clip': []}
    for file_only in file_only_list:

        if file_only[-4:] == '.mp4':
            media_type = 'video'

        if file_only[-4:] in ['.png', '.jpg']:
            if '.clip.' in file_only:
                media_type = 'video_clip'

            else:
                media_type = 'photo'

        media[media_type].append(file_only)
    return media


def get_id_to_media(tweet_info_list):
    id_to_file_only_list = {}
    for file_only in os.listdir(DIR_TWTR_DATA):
        id = file_only.partition('.')[0]

        if id not in id_to_file_only_list:
            id_to_file_only_list[id] = []

        if file_only[-4:] in ['.png', '.jpg', '.mp4']:
            id_to_file_only_list[id].append(file_only)

    return dict(
        list(
            map(
                lambda item: [item[0], organize_media(item[1])],
                id_to_file_only_list.items(),
            )
        )
    )


def expand_tweet_info(tweet_info, id_to_media):
    tweet_info['local_media'] = id_to_media.get(tweet_info['id'], None)
    return tweet_info


def expand_tweet_info_list(tweet_info_list):
    id_to_media = get_id_to_media(tweet_info_list)
    return list(
        map(
            lambda tweet_info: expand_tweet_info(tweet_info, id_to_media),
            tweet_info_list,
        )
    )


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
    return expand_tweet_info_list(tweet_info_list)
