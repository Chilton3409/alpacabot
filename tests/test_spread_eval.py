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

api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")
client = alpacabot.AlpacaBotLink(api_key=api_key, api_secret=api_secret, paper=False, access_token = os.environ.get("META_AI_TOKEN"))

    

async def main():
    ticker='OPEN'
    bid_price = await client.get_bid_price(ticker)
    ask_price = await client.get_ask_price(ticker)
    
    spread = await client.calculate_spread(bid_price, ask_price)
    print(spread)
    return spread
    
    
    
    
if __name__ == '__main__':
    asyncio.run(main())