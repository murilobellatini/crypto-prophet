from src.twitter.scrapper import UserTimeline

if __name__ == '__main__':
    scrapper = UserTimeline()
    scrapper.scrape_data()
