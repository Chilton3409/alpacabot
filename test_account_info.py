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

async def get_account():
    account = await client.get_account()
    return account
async def get_cash_amount(account):
    return account.cash

async def beginning_day_trade_balance(account):
    return account.bod_dtbp

async def daytrade_count(account):
    return account.daytrade_count

async def current_buying_power(account):
    return account.buying_power

async def current_daytrade_buying_power(account):
    return account.daytrade_buying_power

async def current_effective_buying_power(account):
    return account.effective_buying_power

async def current_equity(account):
    return account.equity

async def get_account_id(account):
    return account.id

async def current_portfolio_value(account):
    return account.portfolio_value

async def portfolio_hypervisor():
    account = await get_account()
    portfolio_value = await current_portfolio_value(account)
    id = await get_account_id(account)
    buying_power = await current_buying_power(account)
    equity = await current_equity(account)
    daytrades = await daytrade_count(account)
    cash = await get_cash_amount(account)
    
    overview = f"""
    
    here is the overview of current portfolio\n
    value = {portfolio_value}\n
    with a current buying power of: {buying_power}\n
    current daytrade count is at: {daytrades}\n
    current cash is at: {cash}\n
    

    """
    return overview
    

    

async def main():
   overview = await portfolio_hypervisor()
   print(overview)
   
    
    
    
if __name__ == '__main__':
    asyncio.run(main())