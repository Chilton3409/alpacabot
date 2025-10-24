#!/usr/bin/env python3
#New file created
Advanced Technical Indicators
Below is a Python class that implements advanced technical indicators using TA-Lib, including Stochastic Oscillator, Ichimoku Cloud, Average Directional Index (ADX), and Commodity Channel Index (CCI).
import pandas as pd
import talib
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedTechnicalIndicators:
    def __init__(self, data):
        """
        Initialize the AdvancedTechnicalIndicators class.

        Parameters:
        data (pd.DataFrame): Stock data with 'high', 'low', and 'close' columns
        """
        self.data = data

    def calculate_stochastic_oscillator(self, fastk_period=14, slowk_period=3, slowd_period=3):
        """
        Calculate the Stochastic Oscillator.

        Parameters:
        fastk_period (int): Fast %K period (default=14)
        slowk_period (int): Slow %K period (default=3)
        slowd_period (int): Slow %D period (default=3)

        Returns:
        pd.DataFrame: Stochastic Oscillator values
        """
        try:
            slowk, slowd = talib.STOCH(self.data['high'].values, self.data['low'].values, self.data['close'].values,
                                       fastk_period=fastk_period, slowk_period=slowk_period, slowd_period=slowd_period)
            stoch = pd.DataFrame({
                'slowk': slowk,
                'slowd': slowd
            }, index=self.data.index)
            return stoch
        except Exception as e:
            logger.error(f"Failed to calculate Stochastic Oscillator: {e}")
            return None

    def calculate_ichimoku_cloud(self, conversion_period=9, base_period=26, span_b_period=52):
        """
        Calculate the Ichimoku Cloud.

        Parameters:
        conversion_period (int): Conversion line period (default=9)
        base_period (int): Base line period (default=26)
        span_b_period (int): Span B period (default=52)

        Returns:
        pd.DataFrame: Ichimoku Cloud values
        """
        try:
            high9 = self.data['high'].rolling(window=conversion_period).max()
            low9 = self.data['low'].rolling(window=conversion_period).min()
            conversion_line = (high9 + low9) / 2

            high26 = self.data['high'].rolling(window=base_period).max()
            low26 = self.data['low'].rolling(window=base_period).min()
            base_line = (high26 + low26) / 2

            span_a = ((conversion_line + base_line) / 2).shift(base_period)
            high52 = self.data['high'].rolling(window=span_b_period).max()
            low52 = self.data['low'].rolling(window=span_b_period).min()
            span_b = ((high52 + low52) / 2).shift(base_period)

            ichimoku = pd.DataFrame({
                'conversion_line': conversion_line,
                'base_line': base_line,
                'span_a': span_a,
                'span_b': span_b
            }, index=self.data.index)
            return ichimoku
        except Exception as e:
            logger.error(f"Failed to calculate Ichimoku Cloud: {e}")
            return None

    def calculate_adx(self, period=14):
        """
        Calculate the Average Directional Index (ADX).

        Parameters:
        period (int): ADX period (default=14)

        Returns:
        pd.Series: ADX values
        """
        try:
            adx = talib.ADX(self.data['high'].values, self.data['low'].values, self.data['close'].values, timeperiod=period)
            return pd.Series(adx, index=self.data.index)
        except Exception as e:
            logger.error(f"Failed to calculate ADX: {e}")
            return None

    def calculate_cci(self, period=14):
        """
        Calculate the Commodity Channel Index (CCI).

        Parameters:
        period (int): CCI period (default=14)

        Returns:
        pd.Series: CCI values
        """
        try:
            cci = talib.CCI(self.data['high'].values, self.data['low'].values, self.data['close'].values, timeperiod=period)
            return pd.Series(cci, index=self.data.index)
        except Exception as e:
            logger.error(f"Failed to calculate CCI: {e}")
            return None

# Example usage
if __name__ == "__main__":
    import yfinance as yf

    data = yf.download('AAPL', period='1y')
    ati = AdvancedTechnicalIndicators(data)

    stoch = ati.calculate_stochastic_oscillator()
    ichimoku = ati.calculate_ichimoku_cloud()
    adx = ati.calculate_adx()
    cci = ati.calculate_cci()

    print("Stochastic Oscillator:")
    print(stoch.tail())
    print("\nIchimoku Cloud:")
    print(ichimoku.tail())
    print("\nADX:")
    print(adx.tail())
    print("\nCCI:")
    print(cci.tail())
Explanation
This code defines an AdvancedTechnicalIndicators class that implements advanced technical indicators using TA-Lib.
Initialization
The __init__ method initializes the AdvancedTechnicalIndicators class with stock data.
The data should be a pandas DataFrame with 'high', 'low', and 'close' columns.
Stochastic Oscillator
The calculate_stochastic_oscillator method calculates the Stochastic Oscillator.
It uses the TA-Lib STOCH function to calculate the slow %K and slow %D lines.
The method returns a pandas DataFrame with the Stochastic Oscillator values.
Ichimoku Cloud
The calculate_ichimoku_cloud method calculates the Ichimoku Cloud.
It calculates the conversion line, base line, span A, and span B using rolling window calculations.
The method returns a pandas DataFrame with the Ichimoku Cloud values.
Average Directional Index (ADX)
The calculate_adx method calculates the ADX.
It uses the TA-Lib ADX function to calculate the ADX values.
The method returns a pandas Series with the ADX values.
Commodity Channel Index (CCI)
The calculate_cci method calculates the CCI.
It uses the TA-Lib CCI function to calculate the CCI values.
The method returns a pandas Series with the CCI values.
Example Usage
The example usage demonstrates how to create an instance of the AdvancedTechnicalIndicators class and use its methods to calculate the advanced technical indicators.
It prints the last few values of each indicator.
Advice
You can adjust the parameters for the indicators (e.g., Stochastic Oscillator periods, Ichimoku Cloud periods, ADX period, CCI period) to suit your analysis needs.
This code serves as a starting point for building more complex technical analysis applications. You can extend it by adding more indicators, implementing trading strategies, or integrating with other APIs.
