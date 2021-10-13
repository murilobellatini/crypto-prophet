import os
from tqdm import tqdm
import pandas as pd
from pathlib import Path

from src.text import clean_text
from src.crypto import CryptoCatalog
from src.paths import LOCAL_TWITTER_DATA
 

cc = CryptoCatalog()
tqdm.pandas()


def select_closest(list_: list, target_value: float, key: str):
    """
    Assumes `list_` as a list of dicts and not sorted.
    Returns closest value to `target_value` from `key`.
    """
    return min(list_, key=lambda x: abs(x[key]-target_value))


def load_df_tweets(data_path:Path=LOCAL_TWITTER_DATA):

    df = pd.DataFrame()
    tweet_paths = [data_path / f for f in os.listdir(data_path) if f.endswith('json')]

    for t in tqdm(tweet_paths):
        df = df.append(pd.read_json(t))

    df['user_screen_name'] = df.user.apply(lambda x: x['screen_name'])   
    df['words'] = df.full_text.progress_apply(txt2words)

    return df

def get_mentioned_coins(words:list, cc:CryptoCatalog=cc) -> list:
    words = pd.Series(words)
    return list(words.map(cc.coin2symbol_norm).dropna())


def txt2words(txt:str) -> list:
    return clean_text(txt).lower().split(' ')

def drop_null_values(d:dict):
    return {k: v for k, v in d.items() if v is not None}

def get_valorization(df, col='close', periods=-60, perc=True):
    change = df[col].shift(periods=periods) - df[col]
    if perc:
        change = change / df[col]
    return change.rename(f'{col}_change_{abs(periods)}periods{("_perc" if perc else "")}')


