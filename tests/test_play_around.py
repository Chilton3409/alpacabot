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

async def test_get_account():
    """
    this returns an account object with lots of useful information
    """
    account = await client.get_account()
    return account

async def test_get_open_positions():
    asset = await client.get_all_positions()
    return asset

async def test_snapshot():
    snapsot = await client.get_snapshot(ticker='OPEN')
    return snapsot

async def test_create_watchlist():
    watchlist = await client.create_watchlist()
    return watchlist

async def test_add_to_watchlist(ticker, watchlist_id):
    """
    use watchlist by name to get the id from the object
    then use that id to add a new ticker to the watchlist
    
    """
    test = await client.add_ticker_to_watchlist(id=id, ticker=ticker)
    return test

async def test_get_watchlist():
    
    watchlist = await client.get_watchlist()
    return watchlist

async def test_get_current_price(ticker):
    latest_trade = client.api.get_latest_trade(symbol=ticker)
    print(latest_trade)
    current_price = latest_trade.price
    return current_price


async def test_get_asset():
    asset = await client.get_asset(ticker='OPEN')
    return asset
async def main():
    t = await test_get_current_price('OPEN')
    
    print(t)


    
    
    
if __name__ == '__main__':
    asyncio.run(main())