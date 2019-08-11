import tweepy

class MentionStream():

    def __init__(self, auth, listener):
        self.stream = tweepy.Stream(
            auth=auth, 
            listener=listener, 
            tweet_mode='extended',
        )
    
    def start(self, keyword_list):
        self.stream.filter(track=keyword_list, is_async=True)