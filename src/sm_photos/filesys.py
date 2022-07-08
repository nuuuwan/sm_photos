import os

from utils import Git, JSONFile, www

from sm_photos import videos
from sm_photos._constants import DIR_DATA, DIR_TWTR_DATA, URL_GIT_REPO
from sm_photos._utils import log


def init():
    git = Git(URL_GIT_REPO)
    git.clone(DIR_DATA, force=True)
    git.checkout('data')

    if not os.path.exists(DIR_TWTR_DATA):
        os.mkdir(DIR_TWTR_DATA)


def get_file_prefix(tweet_info):
    return os.path.join(DIR_TWTR_DATA, str(tweet_info['id']))


def download_and_save_media(tweet_info):
    file_prefix = get_file_prefix(tweet_info)

    for media_type in ['photo', 'video']:
        k = f'{media_type}_url_list'
        for i, url in enumerate(tweet_info[k]):
            ext = url.split('.')[-1]
            file_name = f'{file_prefix}.{media_type}.{i:02d}.{ext}'

            if not os.path.exists(file_name):
                www.download_binary(url, file_name)
                log.info(f'Downloaded {url} to {file_name}')

                if media_type == 'video':
                    videos.extract_and_save_clips(file_name)

            else:
                log.info(f'{file_name} exists. Not downloading')


def download_and_save_data(tweet_info):
    file_name = get_file_prefix(tweet_info) + '.data.json'
    JSONFile(file_name).write(tweet_info)
    log.info(f'Wrote {file_name}')


def download_and_save(tweet_info):
    download_and_save_media(tweet_info)
    download_and_save_data(tweet_info)
