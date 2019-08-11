import time

import tweepy

from MentionStream import MentionStream
from helper import (
    fetch, random_word, _delete_tweets, api, auth, post_random_word
)

class MentionStreamListener(tweepy.StreamListener):

    def process_tweet(self, raw_status):
        print("Processing...")
        tweet_by = raw_status.author.screen_name
        try:
            raw_tweet = raw_status.extended_tweet['full_text']
        except AttributeError:
            raw_tweet = raw_status.text
        tweet_text = raw_tweet.lower().replace('@dict_bot', '').strip()
        reply_id = raw_status.id
        definition = fetch(tweet_text)[0]
        eg = fetch(tweet_text)[1]
        status = \
            f"@{tweet_by} {tweet_text}: {definition}" if definition \
                else f"@{tweet_by} Cannot find that word in the dictionary..."
        try:
            print('Sending definition...')
            latest_status = api.update_status(
                status=status,
                in_reply_to_status_id=reply_id,
            )   
            print('Definition tweeted!')
            print('Sending example...')
            api.update_status(
                status=f"@{tweet_by} {eg}",
                in_reply_to_status_id=latest_status.id,
            )
            print('Example tweeted!')
            print('Successfully replied!')

        except tweepy.error.TweepError: 
            # avoid duplicate statuses
            pass
        finally:
            time.sleep(5)

    def on_status(self, status):
        self.process_tweet(status)

    def on_error(self, status_code):
        # stop stream if too many HTTP requests
        if status_code == 420 or status_code == 429:
            return False