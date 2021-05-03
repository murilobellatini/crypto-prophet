import os
import json
import time
import random
import requests
from pathlib import Path
from abc import ABC, abstractmethod

from src.credentials import TWITTER_BEARER_TOKEN
from src.paths import LOCAL_TWITTER_DATA


class Endpoint(ABC):

    @abstractmethod
    def __init__(self, endpoint: str = None):
        pass

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

    @abstractmethod
    def scrape_data(self) -> list:
        pass

    def get_data(self, params:dict) -> requests.Response:

        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'Authorization': f'Bearer {TWITTER_BEARER_TOKEN}'}

        return requests.get(self.url, params=params, headers=headers)

    def safe_get_data(self, params:dict) -> requests.Response:

        sleep_time_s = 60

        while True:
            r = self.get_data(params=params)
            if r.status_code == 200:
                break
            print(
                f'Response code: {r.status_code}. Sleeping for {sleep_time_s} before retry...')
            time.sleep(sleep_time_s)
            sleep_time_s = 2*sleep_time_s

        return r

    def get_local_data_stats(self, tweets:list, filename=None, path: Path = LOCAL_TWITTER_DATA):
        if not filename:
            filename = self.get_filename(tweets)

        output_path = path / filename

        return filename, output_path

    def save_data_locally(self, tweets: list, path: Path = LOCAL_TWITTER_DATA, filename: str = None) -> list:

        filename, output_path = self.get_local_data_stats(tweets, filename, path)
        curr_tweets = self.load_data(output_path)
        merged_data = self.merge_data(tweet_lists=(tweets, curr_tweets))
        self.export_data(merged_data, output_path)
        return merged_data

    def export_data(self, tweets: list, output_path: Path) -> None:
        with open(output_path, mode='w') as f:
            json.dump(tweets, f)

    def load_data(self, path: Path) -> list:
        tweets = []
        if os.path.isfile(path):
            with open(path, mode='r') as f:
                tweets = json.load(f)
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

