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
from alpacabot import AlpacaBotLink
access_token = os.environ.get("META_AI_TOKEN")
api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")
client = AlpacaBotLink(api_key, api_secret, paper=True, access_token=access_token)

async def test_all_positions():
    positions = client.api.get_all_positions()
    return positions



async def main():

    positions = await test_all_positions()
    print(positions)
    
        
    return

if __name__=='__main__':
    asyncio.run(main())