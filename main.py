from src.twitter.api import TwitterApiWrapper

if __name__ == '__main__':
    api = TwitterApiWrapper()
    api.scrape_tweets()
