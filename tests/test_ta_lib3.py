#!/usr/bin/env python3
#New file created
Modified Code to Use Alpaca API
Below is the modified code that uses Alpaca API for fetching stock data instead of yfinance.
import pandas as pd
import talib
import numpy as np
import logging
import alpaca_trade_api as tradeapi

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdditionalTechnicalIndicators:
    def __init__(self, data):
        """
        Initialize the AdditionalTechnicalIndicators class.

        Parameters:
        data (pd.DataFrame): Stock data with 'high', 'low', and 'close' columns
        """
        self.data = data

    def calculate_keltner_channels(self, period=20, multiplier=2):
        """
        Calculate the Keltner Channels.

        Parameters:
        period (int): Moving average period (default=20)
        multiplier (int): ATR multiplier (default=2)

        Returns:
        pd.DataFrame: Keltner Channels values
        """
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
            logger.error(f"Failed to calculate Keltner Channels: {e}")
            return None

    def calculate_cmo(self, period=14):
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
            logger.error(f"Failed to calculate CMO: {e}")
            return None

    def calculate_vortex_indicator(self, period=14):
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
            logger.error(f"Failed to calculate Vortex Indicator: {e}")
            return None

def fetch_stock_data(api_key, api_secret, base_url, symbol, timeframe, limit):
    """
    Fetch stock data from Alpaca API.

    Parameters:
    api_key (str): Alpaca API key
    api_secret (str): Alpaca API secret
    base_url (str): Alpaca API base URL
    symbol (str): Stock symbol
    timeframe (str): Timeframe for the data (e.g., '1d', '1h', '5min')
    limit (int): Number of data points to fetch

    Returns:
    pd.DataFrame: Stock data
    """
    try:
        api = tradeapi.REST(api_key, api_secret, base_url)
        barset = api.get_barset(symbol, timeframe, limit=limit)
        data = barset[symbol].df
        data = data.rename(columns={'o': 'open', 'h': 'high', 'l': 'low', 'c': 'close', 'v': 'volume'})
        return data
    except Exception as e:
        logger.error(f"Failed to fetch stock data: {e}")
        return None

# Example usage
if __name__ == "__main__":
    api_key = "YOUR_API_KEY"
    api_secret = "YOUR_API_SECRET"
    base_url = "https://paper-api.alpaca.markets"
    symbol = "AAPL"
    timeframe = "1d"
    limit = 365

    data = fetch_stock_data(api_key, api_secret, base_url, symbol, timeframe, limit)
    ati = AdditionalTechnicalIndicators(data)

    kc = ati.calculate_keltner_channels()
    cmo = ati.calculate_cmo()
    vi = ati.calculate_vortex_indicator()

    print("Keltner Channels:")
    print(kc.tail())
    print("\nChande Momentum Oscillator (CMO):")
    print(cmo.tail())
    print("\nVortex Indicator (VI):")
    print(vi.tail())
Explanation
The modified code uses the fetch_stock_data function to fetch stock data from Alpaca API. The function takes the API key, API secret, base URL, symbol, timeframe, and limit as parameters and returns a pandas DataFrame with the stock data.
The AdditionalTechnicalIndicators class remains the same as before. The example usage demonstrates how to fetch stock data using the fetch_stock_data function and then create an instance of the AdditionalTechnicalIndicators class to calculate the technical indicators.
Advice
Replace "YOUR_API_KEY" and "YOUR_API_SECRET" with your actual Alpaca API credentials.
You can adjust the parameters for the indicators (e.g., Keltner Channels period, CMO period, VI period) to suit your code needs.
This code serves as a starting point for building more complex technical analysis applications. You can extend it by adding more indicators, implementing trading strategies, or integrating with other APIs.
