#!/usr/bin/env python3
#New file created
from alpaca.trading import TradingClient, OrderRequest, OrderSide, OrderType, TimeInForce
from alpaca.data.historical import StockHistoricalDataClient
#dont forget to implement this
from alpaca.data.requests import StockBarsRequest, StockLatestQuoteRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.requests import OrderRequest, GetAssetsRequest, GetOrdersRequest, LimitOrderRequest, GetCorporateAnnouncementsRequest
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.trading.requests import GetAssetsRequest


from alpaca.data.requests import NewsRequest

from alpaca.data.historical.screener import ScreenerClient
from alpaca.data.requests import MarketMoversRequest, MostActivesRequest
import alpacabot
from dotenv import load_dotenv
import asyncio
import os
load_dotenv()
import time
import datetime
import asyncio
import logging

api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")
client = alpacabot.AlpacaBotLink(api_key=api_key, api_secret=api_secret, paper=False)

async def test_get_asset(ticker: str):
    """
    returns the info for a single ticker
    
    """
    try:
        
        symbol = client.trading_client.get_asset(symbol_or_asset_id="AREB")
        return symbol    
    except Exception as e:
        logging.error(f"an error occured in the get asset function")
        return
async def test_get_all_assets():
    try:
        
        assets = client.client.get_all_assets(filter=GetAssetsRequest(
            asset_class='us_uquity'
        ))
    
        return assets
    except Exception as e:
        logging.error(f"an error occured in the get all assets function: {e}")
        

async def test_get_tradeable_assets():
    assets = await test_get_all_assets()
    # Filter for tradable assets
    tradable_assets = [asset for asset in assets if asset.tradable]
    return tradable_assets

async def test_get_market_movers():
    """
    return the top market movers of the day
    """
    try:
        
        market_movers =  client.screener_client.get_market_movers(request_params=MarketMoversRequest())
        return market_movers
    except Exception as e:
        logging.error(f"an error occured in the get marker movers function.")
        return
    
async def test_get_most_active():
    """
    returns the most actively traded tickers by volume I am assuming
    """
    try:
        
        most_active = client.screener_client.get_most_actives(MostActivesRequest(top=10, by=MostActivesBy.VOLUME))
    
        return most_active
    except Exception as e:
        logging.error(f"an error occured in the get most active function")
        return
    
async def test_get_corporate_announcements():
    """
    returns all corporate announcements of the day for splits, mergers, and spinoffs
    """
    try:
        
        announcements = client.trading_client.get_corporate_announcements(filter=GetCorporateAnnouncementsRequest(
            ca_types=['merger', 'spinoff','split'], since=client.today, until=client.today
                                                                                                              ))
        return announcements
    except Exception as e:
        logging.error(f"an error occured in the get corpo announcments functiion")
        return
    
async def test_get_position_as_percent(ticker: str) -> str:
    """
    get the position for a single ticker
    returns the unrealized gain or loss on a single position
    
    """
    try:
        pos = client.client.get_open_position(ticker)
        as_percent = pos.unrealized_plpc
        
        return as_percent
    except Exception as e:
        logging.error(f"an error occured in the get single posiiton function: {e}")
        return None
    
async def test_get_all_positions() -> list: 
    """
    returns a list off all current open positions
    
    """
    try:
        
        all_positions = client.client.get_all_positions()
        return all_positions
    except Exception as e:
        logging.error(f"an error occured in the get all positions function")
        return
    
async def test_create_quote_request(ticker: str) -> StockLatestQuoteRequest | None:
    
    """
    create a quote object that can be used to get a bid
    or asking price for a single ticker
    
    """
    try:
        
        quote_request = StockLatestQuoteRequest(symbol_or_symbols=([ticker]))
        
        return quote_request
    except Exception as e:
        logging.error(f"an error has occured in the test create quote function: {e}")
        return None

async def test_get_bid_price(ticker: str) -> str:
    """
    return the bid price for a single ticker
    
    """
    quote = await test_create_quote_request(ticker=ticker)
    
    pass

async def test_get_ask_price(ticker: str) -> str:
    """
    return the ask price for a single ticker
    
    """
    
    pass
 
async def test_get_orders():
    """
    returns a list of all open orders
    """
    try:
        
        orders = client.client.get_orders(filter=GetOrdersRequest(
        
        ))
        return orders
    except Exception as e:
        logging.error(f"an error occured in the get open orders function")
        return
async def test_firesale() -> list:
    """
    closes all open positions and returns a list of closed positions 
    """
    try:
        
        firesale = client.client.close_all_positions(cancel_orders=True)
        return firesale
    except Exception as e:
        logging.error(f"an error occured in the firesale function")
        return
    
async def test_get_portfolio_history():
    """
    need account uuid and union str to get portfolio history
    """
    portfolio_history = client.client.get_portfolio_history()
    return portfolio_history

async def test_get_most_active_news():
    """
    sends a news request for the most actively traded tickers
    """
    try:
        
        news = client.news_client.get_news(NewsRequest(
            start=client.today,
            
           
        ))
        return news
    except Exception as e:
        logging.error(f"an error occured in the get news on most active function")
        return

    
async def test_get_market_data():
    market_data = client.screener_client._get_marketdata()
    return market_data


      
async def main():
    test = await client.get_market_movers()
    
    
    
    
    print(test)
    
    
if __name__ == '__main__':
    asyncio.run(main())