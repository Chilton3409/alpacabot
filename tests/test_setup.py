#!/usr/bin/env python3
#New file created
from alpaca.trading import TradingClient

from dotenv import load_dotenv
import asyncio
import os
load_dotenv()
import time
import datetime
import asyncio
import logging



class AlpacaBotLink():
    def __init__(self, api_key, api_secret,):
        #create restclient ref
        self.client = TradingClient(api_key=api_key, secret_key=api_secret, paper=False)
        
        

async def main():
    api_key = os.environ.get("API_KEY")
    api_secret = os.environ.get("API_SECRET")
    return

if __name__=='__main__':
    asyncio.run(main())