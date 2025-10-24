#!/usr/bin/env python3
#New file created
from fastapi import FastAPI
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
import pyttsx3
import talib as ta
from decimal import Decimal 

api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")
client = alpacabot.AlpacaBotLink(api_key=api_key, api_secret=api_secret, paper=False, access_token = os.environ.get("META_AI_TOKEN"))

async def test_indicator():
    try:
        indicator = pass
        
    
    except Exception as e:
        logging.exception(msg=e)



    


async def main():
    products = await client.create_top_gainer_list()
    print(client.top_gainers)
if __name__ == '__main__':
    asyncio.run(main())