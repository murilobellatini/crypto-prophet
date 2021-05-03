from src.crypto import CryptoCatalog
from src.twitter.scrapper import UserTimeline

if __name__ == '__main__':
    scrapper = UserTimeline()
    scrapper.scrape_data()
    
    cc = CryptoCatalog()
    for c in cc.coins:
        print(c)
