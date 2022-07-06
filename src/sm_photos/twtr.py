import os
import time

import tweepy
from utils import logx, timex

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
            media_fields=['preview_image_url'],
            expansions='attachments.media_keys,author_id',
            max_results=100,
        )

        media = {m["media_key"]: m for m in tweets.includes['media']}
        users = {u["id"]: u for u in tweets.includes['users']}

        tweet_info_list = []
        for tweet in tweets.data:
            attachments = tweet.data['attachments']
            media_keys = attachments['media_keys']
            if media[media_keys[0]].preview_image_url:
                image_url = media[media_keys[0]].preview_image_url

                id = tweet.id
                user = users[tweet.author_id].username
                tweet_url = f'https://twitter.com/{user}/status/{id}'

                tweet_info = dict(
                    tweet_url=tweet_url,
                    id=id,
                    user=user,
                    time_create_ut=(int)(
                        time.mktime(tweet.created_at.timetuple())
                    ),
                    text=tweet.text,
                    image_url=image_url,
                )
                tweet_info_list.append(tweet_info)

        log.info(f'Found {len(tweet_info_list)} images')
        return tweet_info_list
