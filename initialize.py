import os

from wordnik import swagger, WordApi, WordsApi
import tweepy

import secret

TWITTER_CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
TWITTER_CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
TWITTER_ACCESS_KEY = os.environ['TWITTER_ACCESS_KEY']
TWITTER_ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']
auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

WORDNIK_ACCESS_URL = 'https://api.wordnik.com/v4'
WORDNIK_ACCESS_KEY = os.environ['WORDNIK_ACCESS_KEY']
client = swagger.ApiClient(WORDNIK_ACCESS_KEY, WORDNIK_ACCESS_URL)
wordAPI = WordApi.WordApi(client)
wordsAPI = WordsApi.WordsApi(client)