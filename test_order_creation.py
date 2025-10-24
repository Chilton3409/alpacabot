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
client = alpacabot.AlpacaBotLink(api_key=api_key, api_secret=api_secret, paper=True, access_token = os.environ.get("META_AI_TOKEN"))

async def test_create_buy_order(ticker):
    pass

async def test_create_sell_order(ticker):
    pass



async def main():
   pass
   
    
    
    
if __name__ == '__main__':
    asyncio.run(main())