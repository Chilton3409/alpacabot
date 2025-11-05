# alpacabot
AI Trading System
Project Description
This project is an automated AI-driven trading system built in Python. It leverages the Alpaca Trading API for market interaction and integrates with the Meta AI API for real-time market sentiment analysis. The system automatically identifies market movers, analyzes sentiment from news and technical indicators, and executes trades based on a proprietary buying and selling logic. It is designed to be highly configurable and operates on a paper trading account for safe testing.
Features
AI-Powered Analysis: Utilizes Meta AI for sentiment analysis of market news and technical indicators to inform trading decisions.
Market Surveillance: Automatically identifies and monitors top market movers to find trading opportunities.
Customizable Strategy: Allows users to configure key trading parameters, including:
Amount of cash to hold back (self.hold_amount)
Take-profit and stop-loss thresholds (self.take_profit_threshold, self.stop_loss_threshold)
Position averaging thresholds (self.average_up_threshold)
Shares per trade (self.trade_amount)
Automated Trade Execution: Places buy and sell orders based on the AI's analysis and predefined logic.
Paper Trading Mode: Operates on an Alpaca paper trading account, enabling risk-free testing and strategy development.
Portfolio Management: Tracks and analyzes existing positions to inform selling decisions.
Prerequisites
Before you begin, ensure you have the following set up:
A Python 3.x environment.
An Alpaca Trading API account (paper trading is sufficient for testing).
Access to the Meta AI API.
