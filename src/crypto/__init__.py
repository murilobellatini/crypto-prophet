import json
from pathlib import Path

from src.paths import LOCAL_GLOBAL_DATA

class Coin:

    def __repr__(self):
        return f"<Coin id:`{self.id}` symbol:`{self.symbol}` name:`{self.name}`>"

    def read_dict(self, dict_:dict):
        self.id = dict_.get('id')
        self.symbol = dict_.get('symbol')
        self.name = dict_.get('name')
        return self
        
    def get_dict(self) -> dict:
        return {
            'id': self.id,
            'symbol': self.symbol,
            'name': self.name
        }

class CryptoCatalog:

    def __init__(self, json_path:Path=LOCAL_GLOBAL_DATA / 'coins.json') -> None:

        with open(json_path, mode='r') as fp:
            coins = json.load(fp)
            
        self.coins = self.load_coins(coins)


    def load_coins(self, coins:list) -> list:
        seen = set()
        self.coins = []
        for c in coins:
            coin = Coin().read_dict(c)
            if coin.id not in seen:
                self.coins.append(coin)
                seen.add(coin.id)


        return self.coins
        
    