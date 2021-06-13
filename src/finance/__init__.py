import datetime
import numpy as np
import pandas as pd
from yahooquery import Ticker
import matplotlib.pyplot as plt


class AssetAdvisor:

  def __init__(self, symbol_pair:str):
    self.symbol_pair = symbol_pair

  def __repr__(self):
    return f"CryptoAdvisor(symbol_pair='{self.symbol_pair}')"

  def extract_data(self, time_range_days:int, interval:str='1m', source:str='yahoo'):

    self.time_range_days = time_range_days
    self.interval = interval

    if source == 'yahoo':

      ticker = Ticker(self.symbol_pair)
      data = ticker.all_modules
      start_dt = datetime.datetime.now() - datetime.timedelta(days=self.time_range_days)

      self.DataFrame = ticker.history(start=start_dt, interval=self.interval).reset_index().drop('symbol', axis=1).set_index('date')
    
    else:
      raise NotImplementedError(f'`source` "{source}" not implemented')

  def calc_stats(self, ma_periods:tuple):

    if not hasattr(self, 'DataFrame'):
      raise Exception('`DataFrame` attribute note avaiable. Run `extract_data` first to generate attribute.')

    stats_cols = []

    for ma in ma_periods:
      column_name = f"ma_{ma}_periods"
      stats_cols.append(column_name)
      self.DataFrame[column_name] = self.DataFrame['close'].rolling(ma).mean()

    self.DataFrame['ma_delta'] = self.DataFrame.apply(
        lambda row: row[stats_cols[0]] - row[stats_cols[1]]
        if not np.isnan(row[stats_cols[1]])
        else np.nan, axis=1)
    self.DataFrame['ma_delta_norm'] = self.DataFrame.apply(
        lambda row: row['ma_delta'] / row['close'], axis=1)
      
    self.stats_cols = stats_cols

  def generate_orders(self, strategy:str='ma', threshold:float=.0035):

    self.threshold = threshold

    if strategy == 'ma':

      raw_orders = self.DataFrame.reset_index().set_index('date').ma_delta_norm.apply(
          lambda x: 'BUY' if x >= threshold
          else 'SELL' if x <= -threshold
          else np.nan).dropna()
      # self.orders = raw_orders.loc[raw_orders.shift(1) != raw_orders]
      self.orders = self.clear_repeated_orders(raw_orders)
    else:
      raise NotImplementedError(f'`strategy` "{strategy}" not implemented')

  def clear_repeated_orders(self, raw_orders:pd.DataFrame):
    return raw_orders.loc[raw_orders.shift(1) != raw_orders]

  def plot_evolution(self):

    for attr in ['DataFrame', 'stats_cols']:
      if not hasattr(self, attr):
        raise Exception(f'`{attr}` attribute note avaiable. Run `extract_data` and `calc_stats` first to generate attribute.')

    _ = self.DataFrame.reset_index().set_index('date')[['close'] + self.stats_cols].plot(
    figsize=(16,6), alpha=1, linewidth=1, color=['lightgray', 'red', 'darkblue'],
    title=f'{self.symbol_pair} statistics (previous {self.time_range_days} days)')

  def plot_ma_delta(self, normalized:bool=True):

    for attr in ['DataFrame', 'stats_cols']:
      if not hasattr(self, attr):
        raise Exception(f'`{attr}` attribute note avaiable. Run `extract_data` and `calc_stats` first to generate attribute.')

    col = 'ma_delta_norm' if normalized else 'ma_delta'
    title = f'{self.symbol_pair} statistics (normalized based on close price)' if normalized else f'{self.symbol_pair} statistics (absolute values)'
    _ = self.DataFrame.reset_index().set_index('date')[[col]].fillna(0).plot(
        figsize=(16,6), alpha=1, linewidth=1,
        title=title)
    _ = plt.axhline(0, color='red', label='y = 0', alpha=0.5, linestyle='--')
    _ = plt.legend(loc='upper left')

  def plot_validation_orders(self, strategy:str='ma'):

    if not hasattr(self, 'threshold'):
      raise Exception('`threshold` attribute note avaiable. Run `generate_orders` first to generate attribute.')

    if strategy == 'ma':

      _ = self.DataFrame.reset_index().set_index('date').apply(
          lambda row: row['ma_delta'] / row['close'], axis=1).fillna(0).plot(
          kind='line', figsize=(16,6), alpha=1, linewidth=1,
          title=f'{self.symbol_pair} statistics (normalized based on close price) - buy/sell threshold of {self.threshold}')
      _ = plt.axhline(0, color='gray', label='y = 0', alpha=0.5, linestyle='--')

      _ = plt.axhline(self.threshold, color='black', label=f'positive threshold', alpha=0.5, linestyle='--')
      _ = plt.axhline(-self.threshold, color='black', label=f'negative threshold', alpha=0.5, linestyle='--')

      for i, (dt, advise) in enumerate(self.orders.to_dict().items()):
        _ = plt.axvline(dt, color='red' if advise == 'SELL'
        else 'green', label=advise if i < 2
        else None, alpha=0.5, linestyle='-')
      _ = plt.legend(loc='best')
    
    else:
      raise NotImplementedError(f'`strategy` "{strategy}" not implemented')

  def plot_evolution_with_orders(self, strategy:str='ma'):

    if not hasattr(self, 'threshold'):
      raise Exception('`threshold` attribute note avaiable. Run `generate_orders` first to generate attribute.')

    if strategy == 'ma':

      _ = self.DataFrame.reset_index().set_index('date')[['close'] 
                                            + self.stats_cols
                                            ].plot(
          figsize=(16,6), alpha=1, linewidth=1, color=['lightgray', 'red', 'darkblue'],
          title=f'{self.symbol_pair} statistics (previous {self.time_range_days} days)')

      for i, (dt, advise) in enumerate(self.orders.to_dict().items()):
        _ = plt.axvline(dt, color='darkred' if advise == 'SELL' else 'darkgreen',
                        label=advise if i < 2 else None, alpha=0.5, linestyle='-')
      _ = plt.legend(loc='best')
    
    else:
      raise NotImplementedError(f'`strategy` "{strategy}" not implemented')

  def calc_profitability(self, trading_fee:float=(0.1 / 100)):
    start_volume = 100
    last_src_symbol = src_symbol = start_volume
    last_dst_symbol = dst_symbol = 0 
    output = []

    # compute trade based on orders list
    for i, (dt, advise) in enumerate(self.orders.to_dict().items()):
      curr_price = self.DataFrame.loc[dt].close 

      if advise == 'BUY':
        dst_symbol += (src_symbol / curr_price) * (1-trading_fee)
        src_symbol -= src_symbol
        is_win = dst_symbol > last_dst_symbol
        profit = dst_symbol / last_dst_symbol - 1
        last_dst_symbol = dst_symbol
      elif advise == 'SELL':
        src_symbol += (dst_symbol * curr_price) * (1-trading_fee)
        is_win = src_symbol > last_src_symbol
        profit = src_symbol / last_src_symbol - 1
        last_src_symbol = src_symbol
        dst_symbol -= dst_symbol

      prof = src_symbol / start_volume - 1

      stats = {
          'dt': dt,
          'advise': advise,
          'curr_price': curr_price,
          'is_win': is_win,
          'profit': profit,
          'src_symbol_amt': src_symbol,
          'dst_symbol_amt': dst_symbol,
      }

      output.append(stats)

    if advise == 'BUY':
      last_price = self.DataFrame.close.iloc[-1]
      src_symbol += (dst_symbol * last_price) * (1-trading_fee)
      dst_symbol -= dst_symbol

    self.prof = src_symbol / start_volume - 1
    self.o_df = pd.DataFrame(output)
    self.win_rate = self.o_df.iloc[2:].is_win.mean()
    self.prof_do_nothing = (start_volume / self.DataFrame.close.iloc[0]) * (1-trading_fee) * self.DataFrame.close.iloc[-1] * (1-trading_fee) / start_volume - 1

  def print_orders_balance(self):
        
    print('TRADE BALANCE')
    print(35*'=')

    print(f'symbols: {self.symbol_pair}')
    print(f'threshold: {self.threshold}')

    print(35*'-')

    print(f'strategy win rate           : {self.win_rate:.2%}')
    print(f'profitability strategy      : {self.prof:.2%}')
    print(f'profitability do-nothing    : {self.prof_do_nothing:.2%}')
    print(f'strategy / do-nothing ratio : {self.prof / self.prof_do_nothing:.2%}')