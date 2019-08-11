import time
import os
import string

from urllib.error import HTTPError

from initialize import auth, api, wordAPI, wordsAPI
from settings import INTERVAL, SPACE_REMAINING

def define(word):
    definition = None
    try:
        definition_list = wordAPI.getDefinitions(
                word,
                sourceDictionaries='all',
        )
        raw_def = next(
            d for d in definition_list 
            if d.text and len(d.text) <= SPACE_REMAINING
        )
        definition =  raw_def.text.replace('<xref>', '').replace('</xref>', '')
    except HTTPError as error: 
        # no definitions were found
        if error.code == 404:
            print(f'No definitions were found for {word}.')
            return None
        # too many requests
        if error.code == 429:
            print('Experiencing too many requests in define...')
            time.sleep(30)
    except StopIteration:
        return None
    finally:
        return definition

def example(word):
    while True:
        try:
            example = wordAPI.getExamples(word)
            return next(
                eg.text for eg in example.examples
                if len(eg.text) <= SPACE_REMAINING
            )
        except (TypeError, StopIteration):
            return None
        except HTTPError as error: 
            # no definitions were found
            if error.code == 404:
                print(f'No examples were found for {word}.')
                return None
            # too many requests
            if error.code == 429:
                print('Experiencing too many requests in example...')
                time.sleep(30)
        

def fetch(word):
    definition = None
    eg = None
    cases = iter([word.lower(), string.capwords(word), word.upper()])
    while not definition:
        try:
            current = next(cases)
            definition = define(current)
            eg = example(current)
        except StopIteration:
            return (None, None)
        except HTTPError as error: 
            # no definitions/usage were found
            if error.code == 404:
                print(f'No definitions/usages was found for {word}.')
                return (None, None)
            # too many requests
            if error.code == 429:
                print('Experiencing too many requests in fetch...')
                time.sleep(30)
    return (definition, eg)

def random_word():
    random_word = None
    while not random_word:
        try:
            random_word = wordsAPI.getRandomWord(
                includePartOfSpeech='noun', 
                hasDictionaryDef='true'
            )
            return random_word
        except HTTPError as error: 
            if error.code == 404:
                print('Could not find a random word.')
                return None
            # too many requests
            if error.code == 429:
                print('Experiencing too many requests in random_word...')
                time.sleep(30)


def _delete_tweets(count=20):
    tweets = api.user_timeline(count=count)
    for t in tweets: 
        api.destroy_status(t.id)

def post_random_word():
    while True:
        api.update_status(status=random_word().word)
        time.sleep(INTERVAL)