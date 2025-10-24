#!/usr/bin/env python3
#New file created
Here's an updated Python script that includes the additional functions:
import os
import alpaca_trade_api as tradeapi

# Load API credentials from environment variables
API_KEY = os.environ.get('ALPACA_API_KEY')
API_SECRET = os.environ.get('ALPACA_API_SECRET')
BASE_URL = 'https://paper-api.alpaca.markets'  # Change to live URL if needed

def authenticate_api(api_key, api_secret, base_url):
    """Authenticate with Alpaca API"""
    try:
        api = tradeapi.REST(api_key, api_secret, base_url)
        return api
    except Exception as e:
        print(f"Authentication failed: {e}")
        return None

def fetch_account_info(api):
    """Fetch account information"""
    try:
        account = api.get_account()
        print("Account Information:")
        print(f"Buying Power: {account.buying_power}")
        print(f"Cash: {account.cash}")
        print(f"Equity: {account.equity}")
    except Exception as e:
        print(f"Failed to fetch account info: {e}")

def retrieve_positions(api):
    """Retrieve a list of positions"""
    try:
        positions = api.list_positions()
        print("Positions:")
        for position in positions:
            print(f"Symbol: {position.symbol}, Quantity: {position.qty}")
    except Exception as e:
        print(f"Failed to retrieve positions: {e}")

def place_limit_order(api, symbol, qty, side, limit_price):
    """Place a limit order for a specified stock"""
    try:
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type='limit',
            limit_price=limit_price,
            time_in_force='gtc'
        )
        print(f"Limit order placed for {symbol}")
    except Exception as e:
        print(f"Failed to place limit order: {e}")

def get_all_orders(api):
    """Get a list of all orders"""
    try:
        orders = api.list_orders(status='all', limit=100)
        print("All Orders:")
        for order in orders:
            print(f"Order ID: {order.id}, Symbol: {order.symbol}, Status: {order.status}")
    except Exception as e:
        print(f"Failed to retrieve orders: {e}")

def cancel_order(api, order_id):
    """Cancel an open order by ID"""
    try:
        api.cancel_order(order_id)
        print(f"Order {order_id} canceled")
    except Exception as e:
        print(f"Failed to cancel order: {e}")

def fetch_market_data(api, symbol):
    """Fetch the current market data for a specified stock"""
    try:
        barset = api.get_barset(symbol, '1min', limit=1)
        bars = barset[symbol]
        print(f"Market Data for {symbol}:")
        print(f"Open: {bars[0].o}, High: {bars[0].h}, Low: {bars[0].l}, Close: {bars[0].c}")
    except Exception as e:
        print(f"Failed to retrieve market data: {e}")

def get_trading_history(api):
    """Get the account's trading history"""
    try:
        activities = api.get_activities()
        print("Trading History:")
        for activity in activities:
            print(f"Activity Type: {activity.activity_type}, Symbol: {activity.symbol}, Quantity: {activity.qty}")
    except Exception as e:
        print(f"Failed to retrieve trading history: {e}")

def close_all_positions(api):
    """Close all positions"""
    try:
        positions = api.list_positions()
        for position in positions:
            api.submit_order(
                symbol=position.symbol,
                qty=position.qty,
                side='sell' if position.side == 'long' else 'buy',
                type='market',
                time_in_force='gtc'
            )
            print(f"Closed position for {position.symbol}")
    except Exception as e:
        print(f"Failed to close positions: {e}")

def main():
    api = authenticate_api(API_KEY, API_SECRET, BASE_URL)
    if api:
        fetch_account_info(api)
        retrieve_positions(api)
        get_all_orders(api)
        # Example usage: Place a limit order for AAPL
        place_limit_order(api, 'AAPL', '1', 'buy', '150.00')
        # Example usage: Fetch market data for AAPL
        fetch_market_data(api, 'AAPL')
        # Example usage: Get trading history
        get_trading_history(api)
        # Example usage: Close all positions
        # close_all_positions(api)

if __name__ == "__main__":
    main()
Explanation:
This updated script includes the following additional functions:
get_all_orders(): Retrieves a list of all orders, including filled, open, and canceled orders.
`cancel_order()
