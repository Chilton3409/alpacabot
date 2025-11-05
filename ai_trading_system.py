#!/usr/bin/env python3
#New file created
from alpaca.trading import TradingClient
import alpacabot
from dotenv import load_dotenv
import asyncio
import os
load_dotenv()
import time
import datetime
import asyncio
import logging
from decimal import Decimal
import ast
import re
class AITradingSystem():
    def __init__(self):
        self.api_key = os.environ.get("API_KEY")
        self.api_secret = os.environ.get("API_SECRET")
        self.client =  alpacabot.AlpacaBotLink(api_key=self.api_key, api_secret=self.api_secret, paper=True, access_token = os.environ.get("META_AI_TOKEN")) 
        self.hold_amount = Decimal('0.00') # amount of cash to hold back from buying power
        self.take_profit_threshold = Decimal('10.00') #expressed as a percent
        self.stop_loss_threshold = Decimal('20.00')#expressed as a percent
        self.average_up_threshold = Decimal('5.00')
        self.trade_amount = float('1')# amount of shares per trade, buying only
        self.market_mover_count = float('50')#amount of tickers to search in market movers function
        self.news_count = float('2')#amount of news articles to search for
        
        
    async def get_account(self):
        account = await self.client.get_account()
        return account
    async def get_cash_amount(self,account):
        return account.cash

    async def beginning_day_trade_balance(self,account):
        return account.bod_dtbp

    async def daytrade_count(self,account):
        return account.daytrade_count

    async def current_buying_power(self,account):
        return account.buying_power

    async def current_daytrade_buying_power(self,account):
        return account.daytrade_buying_power

    async def current_effective_buying_power(self,account):
        return account.effective_buying_power

    async def current_equity(self,account):
        return account.equity

    async def get_account_id(self,account):
        return account.id

    async def current_portfolio_value(self,account):
        return account.portfolio_value

    async def portfolio_hypervisor(self, account):
        """
        take the account object and print or write everything to get 
        an overview of the accounts current financial landscape
        
        """
        try:
            
       
            portfolio_value = await self.current_portfolio_value(account)
            id = await self.get_account_id(account)
            buying_power = await self.current_buying_power(account)
            equity = await self.current_equity(account)
            daytrades = await self.daytrade_count(account)
            cash = await self.get_cash_amount(account)
            
            overview = f"""
            
            here is the overview of current portfolio\n
            value = {portfolio_value}\n
            with a current buying power of: {buying_power}\n
            current daytrade count is at: {daytrades}\n
            current cash is at: {cash}\n
            

            """
            return overview
        except Exception as e:
            logging.exception(msg=e)
            
    async def get_news(self, ticker, limit):
        """
        retrieve the news for the given ticker
        limit: can configure the amount of news articles to retrieve
        """
        try:
            
            if ticker:
                news = await self.client.get_news(ticker, limit)
                if news:
                    
                    return news
        except Exception as e:
            logging.exception(msg=e)
            
        
    async def get_market_movers(self, top):
        """
        get the top market movers in real time
        top: Configure the amount of tickers to retrieve from sorted by percentage change
        
        """
        try:
            
            market_movers = await self.client.get_market_movers(top)
            if market_movers:
                
                return market_movers
        except Exception as e:
            logging.exception(msg=e)
    
    async def sentiment_analysis(self, news, candles):
        """
        use the meta ai api to analyze news and candles for a given ticker
        """
        sentiment = await self.client.get_meta_ai_insights(meta_ai_text=f"Conduct a sentiment analysis on this news: {news} with these candles: {candles}")
        return sentiment
    
    async def ai_top_picks(self, ) -> list:
        """
        retrive the meta ai api's top picks and filter the response
        to retrive a python list of tickers
        """
        picks = await self.client.get_meta_ai_insights(meta_ai_text=f"based on the stocks you have reviewed, what are your top picks? Return a list of top picks in the format ['pick1', 'pick2', ...]. Only the list so I can use it in a function")
        tickers = re.findall(r"'(.*?)'", picks)
        
        print(tickers)
        return tickers
    async def market_surveillance(self, movers:list):
        try:
            if movers:
                for mover in movers:
                    print(mover.symbol)
                    if mover.price >= Decimal('1.00') and mover.price <= Decimal('100.00'):
                        news = await self.get_news(ticker=mover.symbol, limit=2)
                    
                        candles = await self.client.get_candles(ticker=mover.symbol)
                        analysis = await self.sentiment_analysis(news, candles)  
                        
            
        except Exception as e:
            logging.exception(msg=e)
            
    async def buy_logic(self, buying_power, day_trades):
        """
        create buy logic based on current buying power and current day trades
        
        """
        try:
            if buying_power:
                
                
                buying_power = Decimal(buying_power)
                
                if buying_power >= self.hold_amount:
                
                    movers = await self.get_market_movers(top=50)
                    market_surveillance = await self.market_surveillance(movers=movers)
                    
                
                    #turn this into a function
                    ticker_list = await self.ai_top_picks()
                    
                    # i need to filter the list and extract the tickers
                    for ticker in ticker_list:
                        #create buy order
                        print(f"this is in the buying logic ticker: {ticker}")
                        await self.create_buy_order(ticker, qty=1)
                        
        except Exception as e:
            logging.exception(msg=e)
    
    async def get_positions(self):
        try:
            positions = await self.client.get_positions()
            if positions:
                return positions
            
        
        except Exception as e:
            logging.exception(msg=e)
            
    async def get_average_entry(self, position):
        if position:
            
            return position.avg_entry_price
    async def get_current_price(self, position):
        try:
            if position:
                
                current_price = position.current_price
                return current_price
        
        except Exception as e:
            logging.exception(msg=e)
            
    async def calculate_pnl_percent(self, current_price:Decimal, average_entry:Decimal) -> Decimal: 
        """
        express current pnl as a percent
        current price
        average entry
        
        """
        try:
            
            change = current_price - average_entry
            div = change / average_entry
            percentage_change = div * 100
            percentage_change = round(percentage_change, ndigits=2)
            return percentage_change
        except Exception as e:
            logging.exception(msg=e)
            
    async def analyze_portfolio(self, positions):
        """
        send the open positions to meta ai to analyze and send back a python list of positons to sell
        """
        try:
            
            if positions:
                
                analysis = await self.client.get_meta_ai_insights(meta_ai_text=f"analyze my current positions and determine which positons to sell: {positions}. Please only return a python list.")
                sell_list = re.findall(r"'(.*?)'", analysis)
                return sell_list
        except Exception as e:
            logging.exception(msg=e)
    
    async def stop_loss(self, pnl, ticker):
        """
        compare pnl to stop loss threshold
        if below stop loss threshold
        create a sell order
        
        """
        try:
            if pnl:
                if pnl <= self.stop_loss_threshold:
                    #create sell order here
                    #await self.create_sell_order(ticker=ticker, qty=1)
                    print(f"stop loss triggered on: {ticker}")
                
                
        
        except Exception as e:
            logging.exception(msg=e)
            
    async def average_up(self, ticker, pnl):
        """
        if pnl above average up threshold
        create a sell order
        
        """
        try:
            if ticker:
                if pnl:
                    if pnl >= self.average_up_threshold:
                        #create buy order here
                        #await self.create_buy_order(ticker=ticker ,qty=1)
                        print(f"average up triggered on: {ticker}")
        except Exception as e:
            logging.exception(msg=e)    
    async def take_profits(self, pnl ,ticker):
        """
        compare the current pnl to the take profit threshold
        if above the profit taking threshold, create a sell order
        
        """
        try:
            if pnl:
                if pnl >= self.take_profit_threshold:
                    #create a sell order here
                    #await self.create_sell_order(ticker=ticker, qty=1)
                    print(f"take profit triggered on {ticker}")
                
        except Exception as e:
            logging.exception(msg=e)
            
    
    async def sell_logic(self):
        """
        create sell logic with current positions as a parameter
        
        
        """
        try:
            positions = await self.get_positions()
        
            ai_sell_list = await self.analyze_portfolio(positions)
            
            for ticker in ai_sell_list:
                print(ticker)          
                #create sell order here
                #await self.create_sell_order(ticker=ticker, qty=1)
                
        except Exception as e:
            logging.exception(msg=e)
            
    
    async def create_buy_order(self, ticker: str, qty: float):
        """
        easy way to submit a buy order for the given ticker
        abstracts away getting the bid price and creating the order data
        args: ticker you want to buy
        qty: amount of shares
        """
        try:
            
            limit_price = await self.client.get_bid_price(ticker)
            order = await self.client.submit_buy_limit_order(ticker, qty, limit_price=float(limit_price))
        
            print(f'creating buy order for: {ticker}')
        
            return order
        except Exception as e:
            logging.exception(msg=e)
    async def create_sell_order(self, ticker, qty):
        try:
            
            limit_price = await self.client.get_ask_price(ticker)
            order = await self.client.submit_sell_limit_order(ticker, qty, limit_price=float(limit_price))
            return order
        except Exception as e:
            logging.exception(msg=e)
            
    async def cycle():
        """
        Combine the buy logic and sell logic and use the account gfunctions to manage cash hold
        trading amount, day trades, and more
        
        """
        try:
            pass
        
        except Exception as e:
            logging.exception(msg=e)
async def main():
    ai_trading_system = AITradingSystem()
    await ai_trading_system.buy_logic()
    await ai_trading_system.sell_logic()
    
    
    
    
        
    
if __name__ == '__main__':
    asyncio.run(main())