#!/usr/bin/env python3
#New file created
Here's a Python script that follows the given instructions:
import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score
import alpaca_trade_api as tradeapi

# Load API credentials from environment variables
API_KEY = os.environ.get('ALPACA_API_KEY')
API_SECRET = os.environ.get('ALPACA_API_SECRET')
BASE_URL = 'https://paper-api.alpaca.markets'  # Change to live URL if needed

def fetch_historical_data(api, symbol, timeframe, limit):
    """Fetch historical 1-minute chart data for a specified stock"""
    try:
        barset = api.get_barset(symbol, timeframe, limit=limit)
        bars = barset[symbol]
        df = pd.DataFrame([{'time': bar.t, 'open': bar.o, 'high': bar.h, 'low': bar.l, 'close': bar.c} for bar in bars])
        return df
    except Exception as e:
        print(f"Failed to retrieve historical data: {e}")
        return None

def prepare_data(df):
    """Prepare the data for machine learning"""
    try:
        df['target'] = np.where(df['close'].shift(-1) > df['close'], 1, 0)  # 1 if price goes up, 0 if price goes down
        df.dropna(inplace=True)
        features = df[['open', 'high', 'low', 'close']]
        target = df['target']
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        return features_scaled, target
    except Exception as e:
        print(f"Failed to prepare data: {e}")
        return None, None

def train_model(features, target):
    """Train a Random Forest Classifier model"""
    try:
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        return model, X_test, y_test
    except Exception as e:
        print(f"Failed to train model: {e}")
        return None, None, None

def evaluate_model(model, X_test, y_test):
    """Evaluate the model's performance"""
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}, Precision: {precision:.2f}, Recall: {recall:.2f}")
    except Exception as e:
        print(f"Failed to evaluate model: {e}")

def make_prediction(model, features):
    """Make a prediction using the trained model"""
    try:
        prediction = model.predict(features)
        return prediction
    except Exception as e:
        print(f"Failed to make prediction: {e}")
        return None

def main():
    api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL)
    symbol = 'AAPL'
    timeframe = '1Min'
    limit = 1000
    df = fetch_historical_data(api, symbol, timeframe, limit)
    features, target = prepare_data(df)
    model, X_test, y_test = train_model(features, target)
    if model:
        evaluate_model(model, X_test, y_test)
        # Example usage: Make a prediction using the last row of features
        last_row = features[-1].reshape(1, -1)
        prediction = make_prediction(model, last_row)
        print(f"Prediction: {prediction}")

if __name__ == "__main__":
    main()
Explanation:
This script fetches historical 1-minute chart data for a specified stock, prepares the data for machine learning, trains a Random Forest Classifier model, evaluates the model's performance, and makes predictions using the trained model.
The script consists of several functions:
fetch_historical_data(): Fetches historical 1-minute chart data for a specified stock using Alpaca API.
prepare_data(): Prepares the data for machine learning by handling missing values and normalizing features.
train_model(): Trains a Random Forest Classifier model using the prepared data.
evaluate_model(): Evaluates the model's performance using metrics such as accuracy, precision, and recall.
make_prediction(): Makes a prediction using the trained model.
In the main() function, we call these functions in sequence to fetch data, prepare data, train model, evaluate model, and make prediction.
