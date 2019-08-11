from helper import post_random_word, auth, _delete_tweets
from MentionStream import MentionStream
from MentionStreamListener import MentionStreamListener

from settings import USERNAME


if __name__ == '__main__':
    listener = MentionStreamListener()
    stream = MentionStream(auth=auth, listener=listener)
    keyword_list = [USERNAME]
    stream.start(keyword_list)
    post_random_word()