import yaml
import json
from pathlib import Path

from src.paths import root_path
from src.twitter import Endpoint

class UserTimeline(Endpoint):

    def __init__(self, endpoint: str = 'user_timeline'):
        self.url = self.get_endpoint(endpoint)


    def scrape_screen_name_tweets(self, screen_name:str, loops:int=1) -> None:
        filename, output_path = self.get_local_data_stats([{'user':{'screen_name': screen_name}}])
        tweets = self.load_data(output_path)
        for _ in range(loops):
            max_id = self.get_oldest_data_id(tweets)
            params = {
                'screen_name': screen_name,
                'count': self.config['input']['req_count'],
                'max_id': max_id
            }
            curr_tweets = json.loads(self.safe_get_data(params).content)
            tweets = self.merge_data((tweets,curr_tweets))
        self.save_data_locally(tweets)
        


    def scrape_data(self, config_file: Path = root_path / 'config.yml') -> None:
        with open(config_file, mode='r') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

        for influencer in self.config['input']['influencers']:
            self.scrape_screen_name_tweets(screen_name=influencer, loops=self.config['input']['loops'])
