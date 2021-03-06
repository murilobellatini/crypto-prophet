import os
import json
import time
import random
import requests
from pathlib import Path

from src.credentials import TWITTER_BEARER_TOKEN
from src.paths import LOCAL_TWITTER_DATA
from src.helpers import drop_null_values


class Endpoint:

    @staticmethod
    def get_endpoint(endpoint:str) -> str:
        if endpoint == 'user_timeline':
            return 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        else:
            raise NotImplementedError

    @staticmethod
    def get_filename(tweets: list, based_on: str = 'USER_SCREEN_NAME') -> str:
        if based_on == 'USER_SCREEN_NAME':
            return f"{random.choice(tweets)['user']['screen_name']}.json"
        else:
            raise NotImplementedError

    def get_data(self, params:dict) -> requests.Response:

        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'Authorization': f'Bearer {TWITTER_BEARER_TOKEN}'}

        if 'tweet_mode' not in params.keys():
            params['tweet_mode'] = 'extended'

        params = drop_null_values(params)

        return requests.get(self.url, params=params, headers=headers)

    def safe_get_data(self, params:dict, sleep_time_s:int=60) -> requests.Response:

        while True:
            r = self.get_data(params=params)
            if r.status_code == 200:
                break
            print(
                f'Response code: {r.status_code}. Content: {r.content}\n\nSleeping for {int(sleep_time_s/60)} min before retry...')
            time.sleep(sleep_time_s)
            sleep_time_s = 2*sleep_time_s

        return r
class TwitterScraper(Endpoint):

    def get_local_data_stats(self, tweets:list, filename=None, path: Path = LOCAL_TWITTER_DATA):
        if not filename:
            filename = self.get_filename(tweets)

        output_path = path / filename

        return filename, output_path

    def save_data_locally(self, tweets: list, path: Path = LOCAL_TWITTER_DATA, filename: str = None) -> list:
        print(f'Saving data locally...')
        filename, output_path = self.get_local_data_stats(tweets, filename, path)
        curr_tweets = self.load_data(output_path)
        merged_data = self.merge_data(tweet_lists=(tweets, curr_tweets))
        self.export_data(merged_data, output_path)
        print(f'Data successfully saved `{output_path}`')
        return merged_data

    def export_data(self, tweets: list, output_path: Path) -> None:
        with open(output_path, mode='w') as f:
            json.dump(tweets, f)

    def load_data(self, path: Path) -> list:
        tweets = []
        if os.path.isfile(path):
            try:
                with open(path, mode='r') as f:
                    tweets = json.load(f)
            except Exception as e:
                print(f"path: {path}, error: {e}")
        else:
            print(f'File does not exist at path {path}. Skipping loading...')
        return tweets

    def merge_data(self, tweet_lists: tuple) -> list:
        merged_data = []
    
        for tweets in tweet_lists:
            merged_data.extend(tweets)

        seen = set()

        unique_tweets = []

        for t in merged_data:
            if t['id'] not in seen:
                seen.add(t['id'])
                unique_tweets.append(t)

        return unique_tweets


    def get_oldest_data_id(self, tweets):
        if tweets:
            return min(tweets, key=lambda x:x['id'])['id'] # gets oldest tweet extracted from influencer

    def get_latest_data_id(self, tweets):
        if tweets:
            return max(tweets, key=lambda x:x['id'])['id'] # gets oldest tweet extracted from influencer


class Tweet:
    def __init__(self, tweet_json:dict):

        for k,v in tweet_json:
            setattr(self, k, v)

        self.as_dict = tweet_json