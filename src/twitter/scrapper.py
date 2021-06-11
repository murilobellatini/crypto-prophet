import yaml
import json
from pathlib import Path

from src.paths import root_path
from src.twitter import TwitterScraper

class UserTimeline(TwitterScraper):

    def __init__(self, endpoint: str = 'user_timeline'):
        self.url = self.get_endpoint(endpoint)

    def scrape_screen_name_tweets_towards_past(self, screen_name:str, loops:int=1, retry_count:int=5) -> list:
        filename, output_path = self.get_local_data_stats([{'user':{'screen_name': screen_name}}])
        tweets = self.load_data(output_path)
        while True:

            params = {
                'screen_name': screen_name,
                'count': self.config['input']['req_count'],
                'max_id': self.get_oldest_data_id(tweets)
            }

            for _ in range(retry_count): #sometimes user_timeline returns no tweets...
                curr_tweets = json.loads(self.safe_get_data(params).content)
                
                if len(curr_tweets) != 0:
                    break
            
            if len(curr_tweets) < 2:
                break
            
            print(f'{len(curr_tweets)} tweets found...')


            tweets = self.merge_data((tweets,curr_tweets))

        print(f'Scrapping done for user `{screen_name}`... {len(tweets)} tweets accumulated...')
        
        self.save_data_locally(tweets)

        return tweets
        

    def scrape_screen_name_tweets_towards_future(self, screen_name:str) -> list:
        filename, output_path = self.get_local_data_stats([{'user':{'screen_name': screen_name}}])
        tweets = self.load_data(output_path)

        since_id = self.get_latest_data_id(tweets)
        max_id = None

        while True:

            params = {
                'screen_name': screen_name,
                'count': self.config['input']['req_count'],
                'since_id': since_id,
                'max_id': max_id
            }

            curr_tweets = json.loads(self.safe_get_data(params).content)

            print(f'{len(curr_tweets)} tweets found...')

            tweets = self.merge_data((tweets,curr_tweets))

            max_id =  self.get_oldest_data_id(curr_tweets)

            scrapped_ids = [t['id'] for t in tweets]


            if (since_id in scrapped_ids) :
                break
            
            if (curr_tweets == []) or (not since_id):
                break


        print(f'Scrapping done for user `{screen_name}`... {len(tweets)} tweets accumulated...')
        
        self.save_data_locally(tweets)

        return tweets
        

    def scrape_data(self, config_file: Path = root_path / 'config.yml') -> None:
        with open(config_file, mode='r') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

        towards_future = self.config['input']['towards_future']
        influencers = self.config['input']['influencers']

        print(f'{len(influencers)} users detected for scrapping...')

        tweets = []
        for influencer in influencers:
            print(f'Starting to scrape data from user `{influencer}`')
            if towards_future:
                tweets.append(self.scrape_screen_name_tweets_towards_future(
                    screen_name=influencer))
            else:
                tweets.append(self.scrape_screen_name_tweets_towards_past(
                    screen_name=influencer, loops=self.config['input']['loops']))

        return tweets
