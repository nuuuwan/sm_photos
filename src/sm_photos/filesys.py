import os

from utils import File, Git, JSONFile, logx, timex, www

URL_GIT_REPO = 'https://github.com/nuuuwan/sm_photos'
DIR_DATA = '/tmp/sm_photos.data'
DIR_TWTR_DATA = os.path.join(DIR_DATA, 'twtr_data')

log = logx.get_logger('sm_photos.filesys')


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
            else:
                log.info(f'Wrote {file_name} exists. Not downloading')


def download_and_save_data(tweet_info):
    file_name = get_file_prefix(tweet_info) + '.data.json'
    JSONFile(file_name).write(tweet_info)
    log.info(f'Wrote {file_name}')


def download_and_save(tweet_info):
    download_and_save_data(tweet_info)
    download_and_save_media(tweet_info)


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


def build_summary():
    tweet_info_list = load_tweet_info_list()
    tweet_info_list_file = os.path.join(DIR_DATA, 'tweet_info_list.json')
    JSONFile(tweet_info_list_file).write(tweet_info_list)
    log.info(f'Wrote {tweet_info_list_file}')


def render_tweet_info(tweet_info):
    tweet_info['id']
    user = tweet_info['user']
    text = tweet_info['text']

    media_url = None
    video_url_list = tweet_info['video_url_list']
    photo_url_list = tweet_info['photo_url_list']

    if video_url_list:
        media_url = video_url_list[0]
    elif photo_url_list:
        media_url = photo_url_list[0]

    tweet_url = tweet_info['tweet_url']
    time_str = timex.format_time(
        tweet_info['time_create_ut'],
        timezone=timex.TIMEZONE_OFFSET_LK,
    )
    return [
        f'{time_str} by [{user}]({tweet_url})',
        f'{len(video_url_list)} videos, {len(photo_url_list)} photos',
        '```',
        text,
        '```',
        f'![image]({media_url}=x100)',
        '---',
    ]


def build_readme():
    N = 10
    tweet_info_list = load_tweet_info_list()
    rendered_last_n_tweets = []
    for tweet_info in tweet_info_list[:N]:
        rendered_last_n_tweets += render_tweet_info(tweet_info)

    lines = [
        '# Social Media Photos',
        f'*{len(tweet_info_list)} tweets*',
        f'## {N} latest tweets',
    ] + rendered_last_n_tweets
    md_file = os.path.join(DIR_DATA, 'README.md')
    File(md_file).write('\n\n'.join(lines))
    log.info(f'Wrote {md_file}')
