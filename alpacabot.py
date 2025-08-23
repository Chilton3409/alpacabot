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
        
        self.ai_api = MetaAI(access_token)
        self.ai_api.access_token = os.environ.get("ACCESS_TOKEN")
        
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
    
    async def get_asset(self, ticker: str):
        """
        returns information for a single ticker
        """
        try:
            ticker = self.trading_client.get_asset(symbol_or_asset_id=ticker)
            return ticker
        except Exception as e:
            logging.error(f"an error occured in the get asset function: {e}")
            
    async def get_last_price(self, ticker):
        try:
            pass
        
        except Exception as e:
            logging.exception(msg=e)
            
    async def get_news(self, ticker):
        
        """
        retrieve the news for a single ticker
        """
        try:
            news = self.api.get_news(symbol=ticker, limit=1, include_content=True, exclude_contentless=True)
            if news:
                
                for content in news:
                    if content:
                        #use meta ai to analyze the content
                        information = content.content
                        await asyncio.sleep(5.0)    
                        sentiment_analysis = await self.get_meta_ai_insights(f"analyze this news article to generate buy and sell signals for ticker: {ticker}: {information}. Return Buy or Pass")
                        await asyncio.sleep(5.0)                 
                        return sentiment_analysis
                    else:
                        return logging.info(f"no news available for: {ticker}")
            
        except Exception as e:
            logging.exception(msg=e)
    
            
    async def get_market_movers(self):
        """
        returns the latest marker movers
        """
        try:
            market_movers = self.screener_client.get_market_movers(request_params=MarketMoversRequest(top=30))
            return market_movers.gainers

        except Exception as e:
            logging.error(f"an error occured in the get market movers function: {e}")
    async def create_top_gainer_list(self):
        try:
            #extract
            test = await self.get_market_movers()
            
            for t in test:
                
                self.top_gainers.append(t.symbol)
            
            return
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
        pass
    
    async def get_snapshot(self, ticker):
        pass
    
    
            
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
            
    async def buy_logic(self):
        #first we need to gather the the top gainers
        #pass the top gainers tickers into the top gainers list
        await self.create_top_gainer_list()
    
        #get the barset for each ticker and pass it to the machine learning model
        for ticker in self.top_gainers:
            candles = await self.get_candles(ticker=ticker)
            print(candles)
            news = await self.get_news(ticker=ticker)
            print(news)
            #when buy signals are generated, create a limit buy order
            
            #then we need to do the same thing for crypto
            #create a crypto buy_logic cycle
            
            #gather the crypto top gainers
            #store them in the crypto top gainers list
            #get the barset for each ticker and pass it to the machine learning model
            #to generate buy signals
            #then create a buy order when buy signals are generated
            #then use meta to evaluate the portfolio for potential optimizartions 
            #acrross different asset classes
            
        
        
      
        
        return

    async def get_candles(self, ticker):
        # Retrieve 1-minute bar data
       

        test = self.api.get_latest_bars(ticker)
        return test
        
    
    
    async def optimize_portfolio(self):
        pass
    
    
    async def sell_logic():
        
        pass
    async def create_order(self):
        try:
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
            qty=qty,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY,
            limit_price=limit_price
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
            return None
        
    
    
async def main():
    access_token = os.environ.get("META_AI_TOKEN")
    api_key = os.environ.get("API_KEY")
    api_secret = os.environ.get("API_SECRET")
    client = AlpacaBotLink(api_key, api_secret, paper=True, access_token=access_token)
    #add the below code to the buy logic cycle
    await client.buy_logic()
    
    
   
    return

if __name__=='__main__':
    asyncio.run(main())