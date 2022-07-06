import os
import time

import tweepy
from utils import logx

log = logx.get_logger('sm_photos.twtr')


class TWTR:
    @staticmethod
    def get_bearer_token():
        return os.environ['TWTR_BEARER_TOKEN']

    def get_client():
        return

    def __init__(self):
        self.client = tweepy.Client(
            bearer_token=TWTR.get_bearer_token(),
        )

    def get_tweet_info_list(self, tag):
        query = f'#{tag} -is:retweet has:media'

        tweets = self.client.search_recent_tweets(
            query=query,
            tweet_fields=['context_annotations', 'created_at'],
            media_fields=['variants', 'url'],
            expansions='attachments.media_keys,author_id',
            max_results=1000,
        )

        media_idx = {m["media_key"]: m for m in tweets.includes['media']}
        user_idx = {u["id"]: u for u in tweets.includes['users']}

        tweet_info_list = []
        for tweet in tweets.data:
            id = tweet.id
            user = user_idx[tweet.author_id].username
            tweet_url = f'https://twitter.com/{user}/status/{id}'

            attachments = tweet.data['attachments']
            media_keys = attachments['media_keys']

            photo_url_list = []
            video_url_list = []
            for media_key in media_keys:
                media = media_idx[media_key]
                media_type = media.type
                if media_type == 'photo':
                    photo_url = media.url
                    photo_url_list.append(photo_url)
                elif media_type == 'video':
                    variants = media.variants
                    for variant in variants:
                        if variant['content_type'] == 'video/mp4':
                            video_url_list.append(variant['url'])
                            break

            tweet_info = dict(
                tweet_url=tweet_url,
                id=id,
                user=user,
                time_create_ut=(int)(
                    time.mktime(tweet.created_at.timetuple())
                ),
                text=tweet.text,
                photo_url_list=photo_url_list,
                video_url_list=video_url_list,
            )
            tweet_info_list.append(tweet_info)

        log.info(f'Found {len(tweet_info_list)} images')
        return tweet_info_list
