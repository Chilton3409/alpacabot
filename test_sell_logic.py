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

async def get_positions():
    positions = client.api.list_positions()
    return positions

async def analyze_portfolio(positions):
    """
    send the open positions to meta ai to analyze and send back a python list of positons to sell
    """
    analysis = await client.get_meta_ai_insights(meta_ai_text=f"analyze my current positions and determine which positons to sell: {positions}. Please only return a python list so I can use it in a function")
    return analysis


async def sell_logic():
    positions = await get_positions()
    tickers = await analyze_portfolio(positions)
    for ticker in tickers:
        print(ticker)
        #create sell order here
        
    
    


async def main():
   positions = await get_positions()
   print(positions)
   ai_test = await analyze_portfolio(positions)
   print(ai_test)

    
    
    
if __name__ == '__main__':
    asyncio.run(main())