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
api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")
client = alpacabot.AlpacaBotLink(api_key=api_key, api_secret=api_secret, paper=False, access_token = os.environ.get("META_AI_TOKEN"))

async def get_news(ticker, limit):
    if ticker:
        news = await client.get_news(ticker, limit)
        return news
async def get_market_movers(top):
    market_movers = await client.get_market_movers(top)
    
    return market_movers

async def sentiment_analysis(news, candles):
    sentiment = await client.get_meta_ai_insights(meta_ai_text=f"Conduct a sentiment analysis on this news: {news} with these candles: {candles}")
    return sentiment
async def write_file(filename, text):
    pass

async def process_data(tickers):
    pass

async def ai_top_picks():
    picks = await client.get_meta_ai_insights(meta_ai_text=f"based on the stocks you have reviewed, what are your top picks? Please only return a python list I need it in a function")
    return picks 

async def buy_logic():
    try:
        
        movers = await get_market_movers(top=10)
        for mover in movers:
            print(mover.symbol)
            if mover.price >= Decimal('1.00') and mover.price <= Decimal('10.00'):
                news = await get_news(ticker=mover.symbol, limit=2)
            
                candles = await client.get_candles(ticker=mover.symbol)
                analysis = await sentiment_analysis(news, candles)  
                print(analysis)
        ticker_list = await ai_top_picks()
        for ticker in ticker_list:
            #create buy order
            print(ticker)
            pass
    
    except Exception as e:
        logging.exception(msg=e)
        
async def main():
   await buy_logic()
    
    
    
    
if __name__ == '__main__':
    asyncio.run(main())