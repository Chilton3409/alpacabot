#!/usr/bin/env python3
#New file created
from dotenv import load_dotenv
from alpaca.trading import TradingClient, TradeActivity
from alpaca.data import ScreenerClient
from alpaca.data.historical.news import NewsClient
from alpaca.data.requests import NewsRequest
from alpaca.data.requests import MarketMoversRequest, MostActivesRequest
from alpaca.trading.requests import LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
import asyncio
import os
load_dotenv()
import time
import datetime
import asyncio
import logging
import datetime
from decimal import Decimal
from meta_ai_api import MetaAI
import aiofiles
import uuid

import pyttsx3
class AlpacaBotLink():
    def __init__(self, api_key, api_secret, paper, access_token):
        #create restclient ref
        self.trading_client = TradingClient(api_key=api_key, secret_key=api_secret, paper=False)
        self.screener_client = ScreenerClient(api_key=api_key, secret_key=api_secret)
        self.news_client = NewsClient(api_key=api_key, secret_key=api_secret)
        BASE_URL = 'https://api.alpaca.markets'
        self.api = tradeapi.REST(api_key, api_secret, BASE_URL)
        self.today = datetime.date.today().isoformat()
        self.top_gainers = []
        my_tickers = {}
        self.ai_api = MetaAI(access_token)
        self.ai_api.access_token = os.environ.get("ACCESS_TOKEN")
        self.engine = pyttsx3.init()
    async def init(self):
        self.client = TradingClient(api_key=self.api_key, api_secret=self.api_secret)
        self.screener_client= ScreenerClient(api_key=self.api_key, api_secret=self.api_secret)
    
    async def get_all_tradeable_stocks(self):
        try:
            products = self.api.list_assets(status='active', asset_class='us_equity')
            return products
        
        except Exception as e:
            logging.exception(msg=e)
            
    async def get_account(self):
        account = self.api.get_account()
        
        return account
    
    async def get_wallet_balance(self):
        try:
            account = await self.get_account()
            return account.cash
        
        except Exception as e:
            logging.exception(msg=e)
    
    async def get_latest_quote(self, ticker):
        try:
            latest_quote = self.api.get_latest_quote(ticker)
            return latest_quote
        
        except Exception as e:
            logging.exception(msg=e)
        
        
        return latest_quote
    
    async def get_clock(self):
        try:
            clock_stuff = self.client.get_clock()
            return clock_stuff
        
        except Exception as e:
            logging.exception(msg=e)
            
    async def add_ticker_to_watchlist(self, id, ticker):
        try:
            
            add_to_watchlist = self.client.add_asset_to_watchlist_by_id(id, ticker)
            return add_to_watchlist
        
        except Exception as e:
            logging.exception(msg=e)
            
    async def get_corpo_announcements(self, ticker):
        
        """return a list of corporate announcments"""
        try:
            
            corpo_announcements = self.client.get_corporate_announcements(filter=ticker)
            return corpo_announcements
        
        except Exception as e:
            logging.exception(msg=e)
            
    async def remove_from_watchlist(self, id, ticker):
        
        """return a list of corporate announcments"""
        try:
            
            remove_from_watchlist = self.client.remove_asset_from_watchlist_by_id(id, ticker)
            return remove_from_watchlist
        except Exception as e:
            logging.exception(msg=e)
            
    async def test(self, ticker):
        
        """return a list of corporate announcments"""
        try:
            
            pass
        
        except Exception as e:
            logging.exception(msg=e)
            
    async def get_bid_price(self, ticker):
        try:
            quote = await self.get_latest_quote(ticker)
            return quote.bp
        except Exception as e:
            logging.exception(msg=e)
            
    async def get_ask_price(self, ticker):
        try:
            
            quote = await self.get_latest_quote(ticker)
            return quote.ap
        except Exception as e:
            logging.exception(msg=e)
            
    async def calculate_spread(self,bid_price, ask_price):
        try:
            spread = Decimal(bid_price) - Decimal(ask_price)
            
            return spread
        
        except Exception as e:
            logging.exception(msg=e)
    
    async def get_asset(self, ticker: str):
        """
        returns information for a single ticker
        """
        try:
            ticker = self.trading_client.get_asset(symbol_or_asset_id=ticker)
            return ticker
        except Exception as e:
            logging.error(f"an error occured in the get asset function: {e}")
            
    
    async def get_news(self, ticker, limit):
        
        """
        retrieve the news for a single ticker
        """
        try:
            news = self.api.get_news(symbol=ticker, limit=limit, include_content=True, exclude_contentless=True)
            if news:
                
                for content in news:
                    if content.content:
                        return content.content
                        
                    else:
                        return logging.info(f"no news available for: {ticker}")
            
        except Exception as e:
            logging.exception(msg=e)
            
    async def get_market_movers(self):
        """
        returns the latest marker movers
        """
        try:
            market_movers = self.screener_client.get_market_movers(request_params=MarketMoversRequest(top=50))
            
            return market_movers.gainers

        except Exception as e:
            logging.error(f"an error occured in the get market movers function: {e}")
    async def create_top_gainer_list(self):
        try:
            #extract
            market_movers = await self.get_market_movers()
            
            for mover in market_movers:
                if mover.price > Decimal('1.00'):
                    
                    self.top_gainers.append(mover.symbol)
                
            return
        except Exception as e:
            logging.exception(msg=e)
            
    async def create_watchlist(self):
        """
        create a new watchlist
        """
        try:
            watchlist = self.api.create_watchlist(watchlist_name='meta_watchlist')
            return watchlist
        
        except Exception as e:
            logging.exception(msg=e)
            
    async def get_watchlist(self):
        """
        get watchlist and return watchlist id
        """
        try:
            watchlists = self.api.get_watchlists(watchlist_name='meta_watchlist')
            return watchlists
        
        except Exception as e:
            logging.exception(msg=e)
            
    
    async def get_most_active():
        pass
    
    async def get_all_open_positions(self):
        try:
             all_positions = self.api.list_positions()
             return all_positions
             
        
        except Exception as e:
            logging.exception(msg=e)
            
    async def get_all_orders(self):
        try:
            orders = self.api.list_orders()
            return orders
        except Exception as e:
            logging.exception(msg=e)
            
    async def get_trades(self):
        """
        get a history of the most recent trades
        """
        pass
    
    async def get_snapshot(self, ticker):
        """
        get a snapshot of the current ticker, whatever that means
        """
        try:
            snapshot = self.api.get_snapshot(ticker)
            return snapshot
        
        except Exception as e:
            logging.exception(msg=e)
    
    
            
    async def portfolio_history(self):
        """
        retrieve recent portfolio history,
        could be useful to have meta analze the results
        """
        try:
            portfolio_history = self.client.get_portfolio_history()
            return portfolio_history
        
        except Exception as e:
            logging.error(msg=e)
            
    async def buy_logic(self ):
        #first we need to gather the the top gainers
        
        #pass the top gainers tickers into the top gainers list
        
        #get the barset for each ticker and pass it to the machine learning model
        #when buy signals are generated, create a limit buy order
        #then we need to do the same thing for crypto
        #gather the crypto top gainers
        #store them in the crypto top gainers list
        #get the barset for each ticker and pass it to the machine learning model
        #to generate buy signals
        #then create a buy order when buy signals are generated
        #then use meta to evaluate the portfolio for potential optimizartions 
        #acrross different asset classes
        
        
    
        pass

    async def get_candles(self, ticker):
        # Retrieve 1-minute bar data
       
        try:
            
            bars = self.api.get_latest_bars(ticker)
            return bars
        except Exception as e:
            logging.exception(msg=e)
    #put all of the self.api function calls here
    async def get_latest_crypto_bars(self, ticker):
        try:
            latest_bars = self.api.get_latest_crypto_bars(ticker)
            return latest_bars
        
        except Exception as e:
            logging.exception(msg=e)
    async def list_assets(self, ticker):
        try:
            assets = self.api.list_assets()
            return assets
        
        except Exception as e:
            logging.exception(msg=e)
    
    
    async def test(self, ticker):
        try:
            pass
        
        except Exception as e:
            logging.exception(msg=e)
        
    
    #begin meta ai functions 
    async def optimize_portfolio(self, my_tickers:dict):
        """
        use meta ai api to analyze portfolio unrealized gaines and losses
        for potential dollar cost averaging oppurtunities, and to maximize potential
        gains within the my tickers dict{symbol:pnl}
        
        """
        pass
    
    
    async def sell_logic():
        
        pass
    async def create_limit_buy_order(self, ticker):
        try:
            time_in_force = 'day'
            limit_price = await self.get_bid_price(ticker)
            qty = await self.trade_amount(ticker=ticker)
            
            order_id = uuid.uuid4()
            
            pass
        except Exception as e:
            logging.exception(msg=e)
            
    async def trade_amount(self, ticker, bid_price):
        try:
            position_size = Decimal(1.25)

            
            price = Decimal(bid_price)

            trade_amount = position_size / price


            trade_amount = round(trade_amount, ndigits=2)
            return trade_amount
        
        except Exception as e:
            logging.exception(msg=e)
            
    
    async def submit_buy_limit_order(self, ticker: str, qty: float, limit_price: float):
        order_data = LimitOrderRequest(
            symbol=ticker,
            qty=await self.trade_amount(),
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY,
            limit_price=await self.get_bid_price(ticker)
        )
    
        try:
            order = self.client.submit_order(order_data=order_data)
            return order
        except Exception as e:
            logging.exception(msg=e)
            return None
        
    async def submit_sell_limit_order(self, ticker: str, qty: float, limit_price: float):
        order_data = LimitOrderRequest(
            symbol=ticker,
            qty=qty,
            side=OrderSide.SELL,
            time_in_force=TimeInForce.DAY,
            limit_price=limit_price
        )
    
        try:
            order = self.client.submit_order(order_data=order_data)
            return order
        except Exception as e:
            logging.exception(msg=e)
            return None
        
    async def close_position(self, ticker):
        try:
            test = self.client.close_position(symbol_or_asset_id=ticker,close_options=[1, 100])
        except Exception as e:
            logging.exception(msg=e)
        
    async def firesale(self):
        """
        careful this will liquidate the entire portfolio
        may have to do this sometimes
        """
        try:
            firesale = self.client.close_all_positions(cancel_orders=True)
            return firesale
        except Exception as e:
            logging.exception(msg=e)
            
    async def get_meta_ai_insights(self, meta_ai_text):
        try:
            response = self.ai_api.prompt(message=meta_ai_text, new_conversation=False)
            
            return response['message']
        except Exception as e:
            logging.exception(msg=e)
            return logging.info("theres been a problem getting a response from meta")

    async def syn_voice(self, text:str):
        try:
            
            if self.engine:
                self.engine.say(text)
                self.engine.runAndWait()
                return
         
        except Exception as e:
            logging.exception(msg=e)
        
        
            
    
    async def read_file(self, filename:str) -> str:
        """
        read the contents of a file
        """
        try:
            async with aiofiles.open(filename, 'r') as f:
                await f.read()
                return
            
        except Exception as e:
            logging.exception(msg=e)
    
    async def append_file(self, filename:str, text: str):
        try:
            async with aiofiles.open(filename, 'a') as f:
                await f.write("\n")
                await f.write(str(text))
        
        except Exception as e:
            logging.exception(msg=e)
        
    async def write_file(self, filename: str, text: str) -> str:
        try:
            async with aiofiles.open(filename, 'w') as f:
                await f.write(str(text))
                logging.info(f"writing to file: {filename}")
            return
                
        
        except Exception as e:
            logging.exception(msg=e)
            
    async def get_user_input(self):
        user_input = input("Please enter a ticker you want to analyze: ")
        return user_input
    
    async def create_filename(self):
        try:
            task = input("create a name for the file: \n")
            return task
        except Exception as e:
            logging.exception(msg=e)
async def main():
    access_token = os.environ.get("META_AI_TOKEN")
    api_key = os.environ.get("API_KEY")
    api_secret = os.environ.get("API_SECRET")
    client = AlpacaBotLink(api_key, api_secret, paper=True, access_token=access_token)
    
    await client.create_top_gainer_list()
    for ticker in client.top_gainers:
        candles = await client.get_candles(ticker)
        print(candles)
        
        await asyncio.sleep(5.00)
       
    return

if __name__=='__main__':
    asyncio.run(main())