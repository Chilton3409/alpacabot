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
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_curve


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
        self.crypto_top_gainers = []
        self.ai_api = MetaAI(access_token)
        self.ai_api.access_token = os.environ.get("ACCESS_TOKEN")
        #self.model = joblib.load('stock_predictor.jlib')
        self.features_list = []
        self.labels_list = []
        
        self.take_profit_percent = Decimal('5.00')
        self.stop_loss_percent = Decimal('-20.00')
        
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
        try:
            
            account = self.api.get_account()
            return account
        except Exception as e:
            logging.exception(msg=e)
    
    async def get_wallet_balance(self):
        try:
            account = await self.get_account()
            return account.cash
        
        except Exception as e:
            logging.exception(msg=e)
    async def get_buying_power(self):
        try:
            account = self.api.get_account()
            buying_power = account.buying_power
            return buying_power
        
        
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
            
            add_to_watchlist = self.trading_client.add_asset_to_watchlist_by_id(id, ticker)
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
        
        """this is a function template"""
        try:
            
            pass
        
        except Exception as e:
            logging.exception(msg=e)
    
    async def get_latest_trade_price(self, ticker):
        try:
            latest_trade = self.api.get_latest_trade(symbol=ticker)
            latest_price = latest_trade.price
            return latest_price
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
            
    async def calculate_spread(self, bid_price, ask_price):
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
            
    async def get_crypto_market_movers(self):
        """
        use the screening client to return the top 30 crypto market movers top gainers
        """
        try:
            crypto_market_movers = self.screener_client.get_market_movers(MarketMoversRequest(top=30, market_type='crypto'))
            return crypto_market_movers.gainers
        
        
        except Exception as e:
            logging.exception(msg=e)
            
    async def create_crypto_top_gainer_list(self):
        """
        filter the crypto market movers for percentage change in the last 24 hours
        """
        try:
            market_movers = await self.get_crypto_market_movers()
            for mover in market_movers:
                self.crypto_top_gainers.append(mover.symbol)
            return
        
        except Exception as e:
            logging.exception(msg=e)
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
            watchlists = self.api.get_watchlist_by_name(watchlist_name='meta_watchlist')
            return watchlists
        
        except Exception as e:
            logging.exception(msg=e)
            
    
    async def get_all_positions(self):
        try:
             all_positions = self.api.list_positions()
             
             return all_positions
             
        
        except Exception as e:
            logging.exception(msg=e)
            
    async def get_all_crypto_positions(self):
        pass
    
    
            
    async def get_order(self, order_id:str):
        """
        retrieve an order based on its order id
        """
        try:
            order = self.api.get_order(order_id)
            return order
        
        
        
        except Exception as e:
            logging.exception(msg=e)
            
    async def get_all_orders(self):
        try:
            orders = self.api.list_orders()
            
            return orders
        except Exception as e:
            logging.exception(msg=e)
            

    async def get_snapshot(self, ticker):
        """
        returns a snapshot object for the given ticker to easily extract bar information
        and latest quote information
        
        """
        try:
            snapshot = self.api.get_snapshot(ticker)
            return snapshot.latest_quote
        except Exception as e:
            logging.exception(msg=e)
            
    async def collect_data_for_model(self, tickers: list):
        """
        need to iterate through list of tickers to create optimal threshold to then pass to the actuak
        model 
        
        """
        try:
            for ticker in tickers:
                candles = await self.get_candles(ticker)
                #features array
                features = np.array([candles.candles[0].o, candles.candles[0].h, candles.candles[0].l])
                self.features.append(features)
                
                # Label (e.g., 1 if price increased, 0 otherwise)
                if candles.candles[0].c > candles.candles[0].o:
                    self.labels_list.append(1)
                else:
                    self.labels_list.append(0)
        
        except Exception as e:
            logging.exception(msg=e)
            
    async def calculate_optimal_threshold(self, features_array, labels_array):
        try:
             # Split data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(features_array, labels_array, test_size=0.2, random_state=42)

            # Fit the scaler to the training data
            self.scaler.fit(X_train)
            X_test_scaled = self.scaler.transform(X_test)

            # Calculate optimal threshold
            probabilities = self.model.predict_proba(X_test_scaled)[:, 1]
            precision, recall, thresholds = precision_recall_curve(y_test, probabilities)
             # Calculate F1-score for each threshold
            f1_scores = 2 * (precision * recall) / (precision + recall)
            f1_scores = np.nan_to_num(f1_scores)  # Handle potential NaN values

            optimal_threshold = thresholds[np.argmax(f1_scores)]
            if optimal_threshold < 0 or optimal_threshold > 1:
                logging.warning(f"Optimal threshold {optimal_threshold} is outside the expected range [0, 1]")


            return optimal_threshold

        
        except Exception as e:
            logging.exception(msg=e)
            
            
            
    async def generate_buy_signals(self, tickers, optimal_threshold=.09):
        """
        use the optimal threshold to optimize buy signals generated by the model
        iterate through the tickers list and form a prediction based
        on the latest barset
        if the prediction is higher the the optimal threshold
        a buy signal is generated and an order is placed
        
        """
        try:
            #check the amount of avail settled cash before making predictions
            balance = await self.get_wallet_balance()
            #add a balance check here
            buying_power = await self.get_buying_power()
            
            if balance >= buying_power:
                for ticker in tickers:
                    candles = await self.get_candles(ticker)
                    if candles.candles:
                        features = np.array([[candles.candles[0].o, candles.candles[0].h, candles.candles[0].l]])
                        features_scaled = self.scaler.transform(features)
                        prediction = self.model.predict_proba(features_scaled)
                        print(f"Prediction for {ticker}: {prediction}")
                        if prediction.shape[1] > 1:  # Check if there are multiple classes
                            prediction = prediction[0][1] # 0 is up. 1 is down
                        else:
                            prediction = prediction[0][0]  # If not, use the single class probability
                        if prediction > optimal_threshold:  # Use the optimal threshold
                            print(f"Buy signal generated for {ticker} with prediction value: {prediction}")
                            # create buy order here
                            #trade_amount = await self.trade_amount(ticker=ticker)
                            
                            await self.submit_buy_limit_order(ticker=ticker, qty='1' )
                        else:
                            print(f"Current prediction is too low at {prediction}")
                        
            pass
        
        except Exception as e:
            logging.exception(msg=e)
            
    
    

    async def buy_logic(self ):
        try:
            
            #first we need to check the current settled cash amount
            balance = await self.get_wallet_balance()
            #set a mininmum amount to keep cash back
            #if settled_cash >= hold_amount:
            buying_power = await self.get_buying_power()
            
            if buying_power >= balance:
                
            
                tickers = await self.create_top_gainer_list()
                #call collect data for model to build the features list to form predictions
                await self.collect_data_for_model(tickers=tickers)
                features_array = np.array(self.features_list)
                labels_array = np.array(self.labels_list)
                optimal_threshold = await self.calculate_optimal_threshold(features_array, labels_array)
                print(f"Optimal threshold: {optimal_threshold}")

                await self.generate_buy_signals(tickers, optimal_threshold)
                self.features_list.clear()
                self.labels_list.clear()
                return
            
        except Exception as e:
            logging.exception(msg=e)
            
        
    
    async def sell_logic(self):
        """
        """
        try:
            positions = await self.get_all_positions()
            
            for pos in positions:
                #calculate the pnl
                if pos:
                    #average_entry = pos.average_entry
                    #trade_amount = pos.qty
                    #ticker = pos.symbol
                    await self.take_profits(ticker=pos.symbol, average_entry=pos.average_entry, trade_amount=pos.qty)
                    
         
                    #begin the take profit and stop loss logic
            
        except Exception as e:
            logging.exception(msg=e)
            
    async def cycle(self):
        try:
            await self.buy_logic()
            await self.order_management_logic()
            await self.analyze_trades()
            await self.sell_logic()
            return
        
        
        except Exception as e:
            logging.exception(msg=e)
    async def order_management_logic(self):
        pass
    async def get_trading_history(self):
        try:
            activities = self.api.get_activities()
            return activities 
        
        except Exception as e:
            logging.exception(msg=e)
            
    async def analyze_trades(self):
        """
        use meta ai to analyze recent trades made by the machine learning bot
        
        """
        try:
            #get the most recent trade activity
            history = await self.get_trading_history()
            analyze_trades = self.get_meta_ai_insights(meta_ai_text=f"analyze my machine learning bots most recent trades: {history}")
            return analyze_trades
            
        except Exception as e:
            logging.exception(msg=e)
            
    
            logging.exception(msg=e)
            
    
    async def get_1hour_bars(self, ticker):
        try:
            test = self.api.get_bars_iter(symbol=ticker, timeframe='1Day')
            return test
        
        except Exception as e:
            logging.exception(msg=e)

    async def get_candles(self, ticker):
        # Retrieve 1-minute bar data
       
        try:
            
            bars = self.api.get_latest_bars(ticker)
            await asyncio.sleep(.09)
            return bars
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
        
    async def trade_amount(self, ticker, bid_price):
        try:
            position_size = Decimal(1.25)

            price = Decimal(bid_price)

            trade_amount = position_size / price
            
            trade_amount = round(trade_amount, ndigits=2)
            return trade_amount
        
        except Exception as e:
            logging.exception(msg=e)
            
    
    async def submit_buy_limit_order(self, ticker: str, qty: float):
        order_data = LimitOrderRequest(
            symbol=ticker,
            qty=qty,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY,
            limit_price= await self.get_bid_price(ticker)
        )
    
        try:
            order = self.client.submit_order(order_data=order_data)
            return order
        except Exception as e:
            logging.exception(msg=e)
            return None
        
    async def submit_sell_limit_order(self, ticker: str, qty: float):
        order_data = LimitOrderRequest(
            symbol=ticker,
            qty=qty,
            side=OrderSide.SELL,
            time_in_force=TimeInForce.DAY,
            limit_price=await self.get_ask_price(ticker)
        )
    
        try:
            order = self.client.submit_order(order_data=order_data)
            return order
        except Exception as e:
            logging.exception(msg=e)
            return None
        
    async def take_profits(self, ticker, average_entry, trade_amount):
        try:
            if ticker:
                if average_entry:
                    asset= await self.get_asset()
                    current_price = asset.price
                    average_entry = Decimal(average_entry)
                    change = current_price - average_entry
                    div = change / average_entry
                    percentage_change = div * 100
                    if percentage_change:
                        if percentage_change >= self.take_profit_percent:
                            #create the sell order
                            await self.submit_sell_limit_order(ticker=ticker, qty=trade_amount)
            return 
        except Exception as e:
            logging.exception(msg=e)
        
            
    async def stop_loss(self, ticker, average_entry, trade_amount):
        try:
            if ticker:
                if average_entry:
                    asset= await self.get_asset()
                    current_price = asset.price
                    average_entry = Decimal(average_entry)
                    change = current_price - average_entry
                    div = change / average_entry
                    percentage_change = div * 100
                    if percentage_change:
                        if percentage_change <=self.stop_loss_percent:
                            #create the buy order
                            await self.submit_buy_limit_order(ticker=ticker, qty='1')
                            return
        except Exception as e:
            logging.exception(msg=e)
    
    async def calculate_pnl_percent(self, current_price, average_entry):
        """
        calculate pnl and then convert to a percent
        """
        try:
            current_price = Decimal(current_price)
            average_entry = Decimal(average_entry)
            change = current_price - average_entry
            div = change / average_entry
            percentage_change = div * 100
            if percentage_change:
                return percentage_change
            
        
        except Exception as e:
            logging.exception(msg=e)
            
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
    async def get_crypto_products(self):
        pass
    
    async def get_crypto_price(self, ticker):
        pass
    
    async def get_crypto_snapshot(self, ticker):
        try:
            snapshot = self.api.get_crypto_snapshot(ticker)
            return snapshot
        
        except Exception as e:
            logging.exception(msg=e)
    
    async def get_crypto_orderbook(self, ticker):
        try:
            orderbook = await self.api.get_latest_crypto_orderbook(ticker)
            return orderbook
        
        except Exception as e:
            logging.exception(msg=e)
    
    async def get_latest_crypto_quotes(self, ticker):
        try:
            latest_quotes = self.api.get_latest_crypto_quotes(symbols=[ticker])
            return latest_quotes
        
        
        except Exception as e:
            logging.exception(msg=e)    
    
    async def test(self):
        try:
            pass
        
        except Exception as e:
            logging.exception(msg=e)
            
    async def get_meta_ai_insights(self, meta_ai_text):
        try:
            response = self.ai_api.prompt(message=meta_ai_text, new_conversation=False)
            
            return response['message']
        except Exception as e:
            logging.exception(msg=e)
            return logging.info("theres been a problem getting a response from meta")
        

async def main():
    access_token = os.environ.get("META_AI_TOKEN")
    api_key = os.environ.get("API_KEY")
    api_secret = os.environ.get("API_SECRET")
    client = AlpacaBotLink(api_key, api_secret, paper=True, access_token=access_token)
    
    await client.cycle()
    
        
    return

if __name__=='__main__':
    asyncio.run(main())