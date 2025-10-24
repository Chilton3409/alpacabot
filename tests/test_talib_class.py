#!/usr/bin/env python3
#New file created
#!/usr/bin/env python3
import asyncio
from alpacabot import AlpacaBotLink
from dotenv import load_dotenv
import os
import talib
import pandas as pd
import logging
import numpy as np

load_dotenv()
access_token = os.environ.get("META_AI_TOKEN")
api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")
class TechnicalAnalysis:
    def __init__(self, api_key, api_secret, access_token):
        self.client = AlpacaBotLink(api_key, api_secret, paper=True, access_token=access_token)
        self.data = {}
    async def test(self):
        print('hello world')
        # You can use self.client to access Alpaca API functionality here
        # For example:
        # account = await self.client.get_account()
        # print(account)
        
    async def fetch_stock_data(self, symbol):
        try:
            barset = self.client.get_1hour_bars(symbol)
            data = barset[symbol].df
            data = data.rename(columns={'o': 'open', 'h': 'high', 'l': 'low', 'c': 'close', 'v': 'volume'})
            data = self.data
            return data
        except Exception as e:
            logging.exception(msg=e)
            
    async def calculate_rsi(self, data, period=14):
        try:
            pass
        
        except Exception as e:
            logging.exception(msg=e)
            
    async def calculate_bollinger_bands(self, data, period=20, std_dev=2):
        try:
            pass
        
        except Exception as e:
            logging.exception(msg=e)
            
    async def calculate_macd(self, data, fast_period=12, slow_period=26, signal_period=9):
        try:
            pass
        
        except Exception as e:
            logging.exception(msg=e)
            
    async def calculate_keltner_channels(self, period=20, multiplier=2):
        try:
            middle = self.data['close'].ewm(span=period, adjust=False).mean()
            atr = talib.ATR(self.data['high'].values, self.data['low'].values, self.data['close'].values, timeperiod=period)
            upper = middle + multiplier * atr
            lower = middle - multiplier * atr

            kc = pd.DataFrame({
                'upper': upper,
                'middle': middle,
                'lower': lower
            }, index=self.data.index)
            return kc
        except Exception as e:
            logging.error(f"Failed to calculate Keltner Channels: {e}")
            return None

    async def calculate_cmo(self, period=14):
        """
        Calculate the Chande Momentum Oscillator (CMO).

        Parameters:
        period (int): CMO period (default=14)

        Returns:
        pd.Series: CMO values
        """
        try:
            cmo = talib.CMO(self.data['close'].values, timeperiod=period)
            return pd.Series(cmo, index=self.data.index)
        except Exception as e:
            logging.error(f"Failed to calculate CMO: {e}")
            return None

    async def calculate_vortex_indicator(self, period=14):
        
        """
        Calculate the Vortex Indicator (VI).

        Parameters:
        period (int): VI period (default=14)

        Returns:
        pd.DataFrame: VI values
        """
        try:
            high_low = self.data['high'] - self.data['low']
            high_close = np.abs(self.data['high'] - self.data['close'].shift(1))
            low_close = np.abs(self.data['low'] - self.data['close'].shift(1))

            tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
            tr_sum = tr.rolling(window=period).sum()

            plus_vm = np.abs(self.data['high'] - self.data['low'].shift(1))
            minus_vm = np.abs(self.data['low'] - self.data['high'].shift(1))

            plus_di = plus_vm.rolling(window=period).sum() / tr_sum
            minus_di = minus_vm.rolling(window=period).sum() / tr_sum

            vi = pd.DataFrame({
                'plus_di': plus_di,
                'minus_di': minus_di
            }, index=self.data.index)
            return vi
        except Exception as e:
            logging.error(f"Failed to calculate Vortex Indicator: {e}")
            return None
    
    async def calculate_kama(self, period=10):
        """
        Calculate Kaufman's Adaptive Moving Average (KAMA).

        Parameters:
        period (int): KAMA period (default=10)

        Returns:
        pd.Series: KAMA values
        """
        try:
            volatility = self.data['close'].diff().abs().rolling(window=period).mean()
            change = self.data['close'].diff(period).abs()
            er = change / volatility
            sc = (er * (2 / (2 + 1) - 2 / (30 + 1)) + 2 / (30 + 1)) ** 2
            kama = self.data['close'].copy()
            for i in range(1, len(kama)):
                kama.iloc[i] = kama.iloc[i-1] + sc.iloc[i] * (self.data['close'].iloc[i] - kama.iloc[i-1])
            return kama
        except Exception as e:
            logging.error(f"Failed to calculate KAMA: {e}")
            return None
    
    async def calculate_fisher_transform(self, period=10):
        """
        Calculate Fisher Transform.

        Parameters:
        period (int): Fisher Transform period (default=10)

        Returns:
        pd.DataFrame: Fisher Transform values
        """
        try:
            high = self.data['high'].rolling(window=period).max()
            low = self.data['low'].rolling(window=period).min()
            x = (self.data['close'] - low) / (high - low) * 2 - 1
            fisher = (np.exp(2 * x) - 1) / (np.exp(2 * x) + 1)
            signal = fisher.rolling(window=9).mean()
            ft = pd.DataFrame({
                'fisher': fisher,
                'signal': signal
            }, index=self.data.index)
            return ft
        except Exception as e:
            logging.error(f"Failed to calculate Fisher Transform: {e}")
            return None
        
    async def calculate_elder_impulse_system(self, short_period=13, long_period=26):
        """
        Calculate Elder Impulse System.

        Parameters:
        short_period (int): Short EMA period (default=13)
        long_period (int): Long EMA period (default=26)

        Returns:
        pd.DataFrame: Elder Impulse System values
        """
        try:
            short_ema = self.data['close'].ewm(span=short_period, adjust=False).mean()
            long_ema = self.data['close'].ewm(span=long_period, adjust=False).mean()
            macd = short_ema - long_ema
            signal = macd.ewm(span=9, adjust=False).mean()
            histogram = macd - signal
            eis = pd.DataFrame({
                'macd': macd,
                'signal': signal,
                'histogram': histogram
            }, index=self.data.index)
            return eis
        except Exception as e:
            logging.error(f"Failed to calculate Elder Impulse System: {e}")
            return None
    
    async def calculate_indicators(self, symbol):
        # Fetch data using Alpaca API
        # Calculate technical indicators here
        
        pass
    async def collect_data(self):
        """
        I need to collect the market movers 
        calculate the indicators along with each one and write the
        barset and the indicators to a file for each market mover
        then I need the ai to read each text file and analyze all of the marker movers
        
    
        
        """
        pass
async def main():
    ta = TechnicalAnalysis(api_key, api_secret, access_token)
    





if __name__=='__main__':
    asyncio.run(main())