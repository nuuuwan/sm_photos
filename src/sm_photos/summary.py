import os

from utils import File, JSONFile, timex

from sm_photos import tweet_info_utils
from sm_photos._constants import DIR_DATA
from sm_photos._utils import log


def build_summary():
    tweet_info_list = tweet_info_utils.load_tweet_info_list()
    tweet_info_list_file = os.path.join(DIR_DATA, 'tweet_info_list.json')
    JSONFile(tweet_info_list_file).write(tweet_info_list)
    log.info(f'Wrote {tweet_info_list_file}')


def render_tweet_info(tweet_info):
    tweet_info['id']
    user = tweet_info['user']
    text = tweet_info['text']
    tweet_url = tweet_info['tweet_url']
    time_str = timex.format_time(
        tweet_info['time_create_ut'],
        timezone=timex.TIMEZONE_OFFSET_LK,
    )

    media_url = None
    video_url_list = tweet_info['video_url_list']
    photo_url_list = tweet_info['photo_url_list']

    line_media = ''
    if photo_url_list:
        media_url = photo_url_list[0]
        line_media = f'![image]({media_url})'

    return [
        f'{time_str} by [{user}]({tweet_url})',
        f'{len(video_url_list)} videos, {len(photo_url_list)} photos',
        '```',
        text,
        '```',
        line_media,
        '---',
    ]


def build_readme():
    N = 100
    tweet_info_list = tweet_info_utils.load_tweet_info_list()
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
