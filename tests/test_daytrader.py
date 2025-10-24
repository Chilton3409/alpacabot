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
    

@app.post("/generate_signals")
async def generate_signals(ticker, candles, news):
    signals= await client.get_meta_ai_insights(f"conduct a sentiment analysis for ticker:{ticker} here are the latest candles: {candles}with this news data: {news} to generate buy or signals with a confidence rating")
    return {"signals": signals} 
  
@app.get("{ticker}/{news}/voice")
async def synthesize_voice(text):
    await client.syn_voice(text=text)
    return text

async def main():
    await client.create_top_gainer_list()
    ticker = await client.get_user_input()
    candles = await get_candles(ticker=ticker)
    
    news = await client.get_news(ticker.upper(), limit=10)
    print(news)
    sentiment_analysis = await generate_signals(ticker=ticker, candles=candles, news=news)
    print(sentiment_analysis['signals'])
        
        
if __name__ == '__main__':
    asyncio.run(main())