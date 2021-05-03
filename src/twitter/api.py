import yaml
import json
import time
import requests
import os
import random
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

root_path = Path(os.getcwd())
TWEETS_DATA_PATH = root_path / 'data/tweets'
TWITTER_BEARER_TOKEN = os.environ.get('TWITTER_BEARER_TOKEN')


class TwitterApiWrapper:

    def __init__(self, endpoint: str = None):

        if not endpoint:
            endpoint = self.get_default_endpoint()

        self.url = endpoint

    @staticmethod
    def get_default_endpoint() -> str:
        return 'https://api.twitter.com/1.1/statuses/user_timeline.json'

    @staticmethod
    def get_filename(tweets: list, based_on: str = 'USER_SCREEN_NAME') -> str:
        if based_on == 'USER_SCREEN_NAME':
            return f"{random.choice(tweets)['user']['screen_name']}.json"
        else:
            raise NotImplementedError

    def get_timeline_tweets(self, user_screen_name: str, count: int = 200,
                            since_id: int = None, max_id: int = None) -> requests.Response:
        params = {
            'screen_name': user_screen_name,
            'count': count
        }

        if since_id:
            params['since_id'] = since_id

        if max_id:
            params['max_id'] = max_id

        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'Authorization': f'Bearer {TWITTER_BEARER_TOKEN}'}

        return requests.get(self.url, params=params, headers=headers)

    def safe_get_timeline_tweets(self, user_screen_name: str, count: int = 200,
                                 since_id: int = None, max_id: int = None) -> requests.Response:

        sleep_time_s = 60

        while True:
            r = self.get_timeline_tweets(user_screen_name=user_screen_name,
                                         count=count, since_id=since_id, max_id=max_id)
            if r.status_code == 200:
                break
            print(
                f'Response code: {r.status_code}. Sleeping for {sleep_time_s} before retry...')
            time.sleep(sleep_time_s)
            sleep_time_s = 2*sleep_time_s

        return r

    def get_local_tweets_stats(self, tweets:list, filename=None, path: Path = TWEETS_DATA_PATH):
        if not filename:
            filename = self.get_filename(tweets)

        output_path = path / filename

        return filename, output_path

    def save_tweets_locally(self, tweets: list, path: Path = TWEETS_DATA_PATH, filename: str = None) -> list:

        filename, output_path = self.get_local_tweets_stats(tweets, filename, path)
        curr_tweets = self.load_tweets(output_path)
        merged_tweets = self.merge_tweets(tweet_lists=(tweets, curr_tweets))
        self.export_tweets(merged_tweets, output_path)
        return merged_tweets

    def export_tweets(self, tweets: list, output_path: Path) -> None:
        with open(output_path, mode='w') as f:
            json.dump(tweets, f)

    def load_tweets(self, path: Path) -> list:
        tweets = []
        if os.path.isfile(path):
            with open(path, mode='r') as f:
                tweets = json.load(f)
        else:
            print(f'File does not exist at path {path}. Skipping loading...')
        return tweets

    def merge_tweets(self, tweet_lists: tuple) -> list:
        merged_tweets = []
    
        for tweets in tweet_lists:
            merged_tweets.extend(tweets)

        seen = set()

        unique_tweets = []

        for t in merged_tweets:
            if t['id'] not in seen:
                seen.add(t['id'])
                unique_tweets.append(t)

        return unique_tweets


    def get_oldest_tweet(self, tweets):
        if tweets:
            return min(tweets, key=lambda x:x['id'])['id'] # gets oldest tweet extracted from influencer


    def scrape_influencer_tweets(self, influencer:str, loops:int=1) -> None:
        filename, output_path = self.get_local_tweets_stats([{'user':{'screen_name': influencer}}])
        tweets = self.load_tweets(output_path)
        for _ in range(loops):
            max_id = self.get_oldest_tweet(tweets)
            curr_tweets = json.loads(self.safe_get_timeline_tweets(user_screen_name=influencer, max_id=max_id).content)
            tweets = self.merge_tweets((tweets,curr_tweets))
        self.save_tweets_locally(tweets)
        


    def scrape_tweets(self, config_file: Path = root_path / 'config.yml') -> None:
        with open(config_file, mode='r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        for influencer in config['input']['influencers']:
            self.scrape_influencer_tweets(influencer=influencer, loops=config['input']['loops'])
