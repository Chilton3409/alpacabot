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

api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")
client = alpacabot.AlpacaBotLink(api_key=api_key, api_secret=api_secret, paper=False, access_token = os.environ.get("META_AI_TOKEN"))
app = FastAPI()

@app.get("{ticker}/{news}")
async def get_latest_news(ticker):
    try:
        news = await client.get_news(ticker)
        return {news:'news'}
    
    except Exception as e:
        logging.exception(msg=e)

@app.get("/candles/{ticker}")
async def get_candles(ticker: str):
    try:
        candles = await client.get_candles(ticker)
        return {"candles": candles}
    except Exception as e:
        return {"error": str(e)}
    
async def get_meta_ai_insights(self, meta_ai_text):
        try:
            response = self.ai_api.prompt(message=meta_ai_text, new_conversation=False)
            
            return response['message']
        except Exception as e:
            logging.exception(msg=e)
            return logging.info("theres been a problem getting a response from meta")
        
@app.post("/generate_advertisement")
async def generate_signals(ticker, candles):
    signals= await client.get_meta_analyze_candles(ticker, candles, news)
    return {"signals": signals}   

async def main():
    await client.create_top_gainer_list()
    
    for ticker in client.top_gainers:
        candles = await get_candles(ticker)
        #print(candles.get('candles'))
        news = await get_latest_news(ticker)
        signals = await client.get_meta_ai_insights(meta_ai_text=f"analyze {ticker} with these candles:{candles} and the latest news: {news} to generate buy and sell signals.")
        await client.write_file(fileaname=ticker + ".txt", text=signals)
        
        
        
if __name__ == '__main__':
    asyncio.run(main())