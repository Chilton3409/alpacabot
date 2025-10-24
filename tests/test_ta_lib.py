#!/usr/bin/env python3
#New file created
Technical Analysis Class
Below is a Python class that uses Alpaca API for fetching stock data and TA-Lib package for performing technical analysis.
import pandas as pd
import talib
from alpaca_trade_api import REST
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TechnicalAnalysis:
    def __init__(self, api_key, api_secret, base_url):
        """
        Initialize the TechnicalAnalysis class.

        Parameters:
        api_key (str): Alpaca API key
        api_secret (str): Alpaca API secret
        base_url (str): Alpaca API base URL
        """
        self.api = REST(api_key, api_secret, base_url)

    def fetch_stock_data(self, symbol, timeframe, limit):
        """
        Fetch stock data from Alpaca API.

        Parameters:
        symbol (str): Stock symbol
        timeframe (str): Timeframe for the data (e.g., '1d', '1h', '5min')
        limit (int): Number of data points to fetch

        Returns:
        pd.DataFrame: Stock data
        """
        try:
            barset = self.api.get_barset(symbol, timeframe, limit=limit)
            data = barset[symbol].df
            return data
        except Exception as e:
            logger.error(f"Failed to fetch stock data: {e}")
            return None

    def calculate_rsi(self, data, period=14):
        """
        Calculate the Relative Strength Index (RSI).

        Parameters:
        data (pd.DataFrame): Stock data
        period (int): RSI period (default=14)

        Returns:
        pd.Series: RSI values
        """
        rsi = talib.RSI(data['close'].values, timeperiod=period)
        return pd.Series(rsi, index=data.index)

    def calculate_bollinger_bands(self, data, period=20, std_dev=2):
        """
        Calculate Bollinger Bands.

        Parameters:
        data (pd.DataFrame): Stock data
        period (int): Moving average period (default=20)
        std_dev (int): Standard deviation (default=2)

        Returns:
        pd.DataFrame: Bollinger Bands
        """
        upper, middle, lower = talib.BBANDS(data['close'].values, timeperiod=period, nbdevup=std_dev, nbdevdn=std_dev)
        bbands = pd.DataFrame({
            'upper': upper,
            'middle': middle,
            'lower': lower
        }, index=data.index)
        return bbands

    def calculate_macd(self, data, fast_period=12, slow_period=26, signal_period=9):
        """
        Calculate the Moving Average Convergence Divergence (MACD).

        Parameters:
        data (pd.DataFrame): Stock data
        fast_period (int): Fast EMA period (default=12)
        slow_period (int): Slow EMA period (default=26)
        signal_period (int): Signal EMA period (default=9)

        Returns:
        pd.DataFrame: MACD values
        """
        macd, macd_signal, macd_hist = talib.MACD(data['close'].values, fastperiod=fast_period, slowperiod=slow_period, signalperiod=signal_period)
        macd_data = pd.DataFrame({
            'macd': macd,
            'signal': macd_signal,
            'hist': macd_hist
        }, index=data.index)
        return macd_data

# Example usage
if __name__ == "__main__":
    api_key = "YOUR_API_KEY"
    api_secret = "YOUR_API_SECRET"
    base_url = "https://paper-api.alpaca.markets"

    ta = TechnicalAnalysis(api_key, api_secret, base_url)
    data = ta.fetch_stock_data('AAPL', '1d', 100)

    if data is not None:
        rsi = ta.calculate_rsi(data)
        bbands = ta.calculate_bollinger_bands(data)
        macd = ta.calculate_macd(data)

        print("RSI:")
        print(rsi.tail())
        print("\nBollinger Bands:")
        print(bbands.tail())
        print("\nMACD:")
        print(macd.tail())
Explanation
This code defines a TechnicalAnalysis class that uses Alpaca API for fetching stock data and TA-Lib package for performing technical analysis. The class has methods for calculating indicators like RSI, Bollinger Bands, and MACD.
Initialization
The __init__ method initializes the TechnicalAnalysis class with Alpaca API credentials.
It sets up a REST client for interacting with the Alpaca API.
Fetching Stock Data
The fetch_stock_data method fetches stock data from Alpaca API.
It takes the stock symbol, timeframe, and limit as parameters.
The method returns a pandas DataFrame containing the stock data.
Calculating Indicators
The calculate_rsi, calculate_bollinger_bands, and calculate_macd methods calculate the RSI, Bollinger Bands, and MACD indicators, respectively.
These methods use TA-Lib functions to perform the calculations.
They return pandas Series or DataFrames containing the calculated indicator values.
Example Usage
The example usage demonstrates how to create an instance of the TechnicalAnalysis class and use its methods to fetch stock data and calculate indicators.
It prints the last few values of each indicator.
Advice
Replace "YOUR_API_KEY" and "YOUR_API_SECRET" with your actual Alpaca API credentials.
You can adjust the parameters for the indicators (e.g., RSI period, Bollinger Bands period, MACD fast and slow periods) to suit your analysis needs.
This code serves as a starting point for building more complex technical analysis applications. You can extend it by adding more indicators, implementing trading strategies, or integrating with other APIs.
