from src.twitter.endpoints import UserTimeline

if __name__ == '__main__':
    api = UserTimeline()
    api.scrape_data()
