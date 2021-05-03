import json
from pathlib import Path

from src.paths import LOCAL_GLOBAL_DATA
from src.helpers import clean_text
class Coin:

    def __repr__(self):
        return f"<Coin id:`{self.id}` symbol:`{self.symbol}` name:`{self.name}`>"

    def read_dict(self, dict_:dict):
        self.id = dict_.get('id')
        self.symbol = dict_.get('symbol')
        self.name = dict_.get('name')
        return self
        
    @property
    def as_dict(self) -> dict:
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

    @property
    def coin2symbol(self):
        return {
            **{c.as_dict['name']: c.as_dict['symbol'] for c in self.coins},
            **{c.as_dict['symbol']: c.as_dict['symbol'] for c in self.coins}
            }

    @property
    def coin2symbol_lower(self):
        return {k.lower(): v for  k,v in self.coin2symbol.items()}
        
    
    @property
    def coin2symbol_norm(self):

        dict_ = {clean_text(k): v for  k,v in self.coin2symbol_lower.items()}

        ignore = {'A','AD','AT','BIT','BLOCK','BUT','DAY','FAITH','FREE','GET','GOOD','IN','IT','ME','NEXT','OF','SEE','THAN','USE','WHEN','WORK','YOU', 'LIKE', 'FOR', 'MAY', 'MAN', 'FANS', 'ONLY', 'CAN', 'FUN', 'MORE', 'ONE', 'OUR', 'NEW', 'UP', 'TIME', 'VIA', '$$$', 'KNOW','OWN', 'GO', 'HELP', 'OPEN', 'LESS', 'HIGH', 'SURE', 'SAY', 'GIVE','PART', 'GOT', 'REAL', 'BIG', 'PAY', 'START', 'READ', 'TALK', 'TEAM','LIVE', 'GOLD', 'TOP', 'WELL', 'DATA', 'SET', 'POST','PUT', 'TRUE', 'LET', 'SEND', 'SHOW', 'COIN', 'CASH', 'KIND', 'GAME','ADD', 'LIFE',  'GUESS', 'NODE',  'HOLD', 'KEY', 'TRUST','FUND', 'SMART', 'CARE',  'TOKEN', 'HUGE', 'SPACE', 'FORK','TOOK', 'BANK', 'GAS', 'PROUD', 'SEED', 'FAIR', 'MIND', 'CARD', 'SUPER','HIT', 'VIEW',  'CAP', 'SENSE', 'LINK', 'WIN', 'MEET','FAST', 'CREDIT',  'CHAT', 'CAR', 'PLAN', 'DOLLAR','PLAY', 'SOLVE', 'WISH', 'NET', 'SAFE', 'DEAL', 'PRO','PLUS','BET', 'HER', 'FIX', 'TYPE', 'PRE', 'SHOP', 'STAKE', 'HOT','AIR', 'BAN', '1ST', 'LED', 'WEALTH', 'DROP','LIGHT', 'RISE', 'PITCH', 'HASH', 'WIDE', 'AT', 'OK', 'WEB', 'CARS', 'PASS', 'MET', 'CITY', 'ETC', 'MUSIC', 'NOR','CUT', 'MIN', 'SHIP', 'EVIL', 'SONG', 'WAGE', 'INFO', 'BEAR','SIX', 'TEN', 'STREAM', 'LIQUID', 'MEME', 'SHE', 'SPOT', 'BLACK','SWAP', 'BLUE', 'U', 'P2P', 'FIT', 'BITS', 'FACE', 'BULL','HAND', 'FOOD', 'ABS', 'RED', 'MOVIE', 'HIRE', 'SKIN', 'UNIT', 'LA','DEV', 'JOBS', 'MOON', 'CROWD', 'JUMP', 'WOMEN', 'ADV',  'RACE','POLL', 'ICE', 'STAR', 'WILD', 'SHIFT', '300', 'OPT', 'UNI', 'GOD','DIG',  'EPIC', 'BEAT', 'KICK', 'HERO', 'PURE',  'TIP','MARKS', 'MEN','MAX', 'RAP',  'MAD', 'LUCKY','AUTO', 'LOG', 'DREAM', 'FUEL', 'UNITS', 'GAP', 'DEL', 'RIDE', 'BID', 'KING', 'HEAT', 'SKILL','NOTE',  'SPEC', 'STORM','DICE',  'GUARD', 'CURE', 'DOT', 'MICRO', 'TIPS', 'BAY', 'CAT', 'ULTRA',  'POP', 'SUN', 'WEED', 'SUB', 'SKY',  'SYNC', 'BITE', 'CAGE', 'BOX', 'ARMS','TAG',  'SWING', 'SEC', 'TROLL', 'GUN', 'ADS', 'WIRE', 'SLOT',  'SNOW',  'INDEX', 'BIO',  'WOKE', 'BOMB','BOT', 'LEND',  'GENE', 'SCORE','KIT', 'FLASH', 'SPRING', 'JOY', 'DASH', 'COW', 'SILK',  'VIBE', 'HYPER', 'RAIN','BEAN','RIPPED', 'TESLA', 'BEVERAGE', 'TWINS','SOAR', 'WAVES', 'RAVE', 'OMG','BEAM', 'SEAL', 'DOCK', 'PIRATE','ONION','COUP','BEE', 'STEEP' ,'GIVE','$$$','SENT'}

        ignore = [i.lower() for i in ignore]

        return {k: v for  k,v in dict_.items() if k not in ignore}