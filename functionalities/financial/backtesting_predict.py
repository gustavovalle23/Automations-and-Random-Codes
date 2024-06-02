import yfinance as yf
import pandas as pd
import numpy as np

"""
When to Buy (Long Position)
Buy Signal:
The short moving average (Short_MA) crosses above the long moving average (Long_MA).
The RSI is above 50.
The volatility is below the threshold (e.g., 0.3).

When to Sell (Short Position)
Sell Signal:
The short moving average (Short_MA) crosses below the long moving average (Long_MA).
The RSI is below 50.
The volatility is below the threshold (e.g., 0.3).

Stop Loss
Long Position: Stop loss is set at 1% below the entry price.
Short Position: Stop loss is set at 1% above the entry price.

Take Profit (Optional)
Long Position: Take profit can be set at 2% above the entry price.
Short Position: Take profit can be set at 2% below the entry price.
"""

def get_intraday_data(ticker, interval='15m'):
    stock_data = yf.download(ticker, period='2d', interval=interval)
    return stock_data

def calculate_volatility(data):
    data['Returns'] = data['Close'].pct_change()
    volatility = data['Returns'].rolling(window=10).std() * np.sqrt(252)
    data['Volatility'] = volatility
    return data

def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    data['RSI'] = rsi
    return data

def apply_strategy(data, short_window=9, long_window=21, volatility_threshold=0.3, rsi_threshold=50):
    # Calculate short and long moving averages
    data['Short_MA'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window, min_periods=1).mean()
    
    # Calculate RSI
    data = calculate_rsi(data)
    
    # Create long signals based on moving averages, RSI, and volatility threshold
    data['Long_Signal'] = 0
    data['Long_Signal'][short_window:] = np.where(
        (data['Short_MA'][short_window:] > data['Long_MA'][short_window:]) & 
        (data['RSI'][short_window:] > rsi_threshold) & 
        (data['Volatility'][short_window:] <= volatility_threshold),
        1, 0
    )
    
    # Create short signals based on moving averages, RSI, and volatility threshold
    data['Short_Signal'] = 0
    data['Short_Signal'][short_window:] = np.where(
        (data['Short_MA'][short_window:] < data['Long_MA'][short_window:]) & 
        (data['RSI'][short_window:] < (100 - rsi_threshold)) & 
        (data['Volatility'][short_window:] <= volatility_threshold),
        1, 0
    )
    
    return data

def analyze_tickers(tickers, stop_loss_pct=0.01, take_profit_pct=0.02):
    potential_tickers = []

    for ticker in tickers:
        # Get intraday stock data for the last 2 days
        stock_data = get_intraday_data(ticker)
        
        # Calculate volatility
        stock_data = calculate_volatility(stock_data)
        
        # Apply strategy to get signals
        strategy_data = apply_strategy(stock_data)
        
        # Check the most recent signal
        latest_signal = strategy_data[['Long_Signal', 'Short_Signal']].iloc[-1]
        if latest_signal['Long_Signal'] == 1:
            potential_tickers.append((ticker, 'long'))
        elif latest_signal['Short_Signal'] == 1:
            potential_tickers.append((ticker, 'short'))
    
    return potential_tickers

# List of tickers to analyze
tickers = [
    'CPFE3.SA',
    'NVDA',
    'PBR',
    'EURAUD=X'
]

# Analyze the tickers
potential_operations = analyze_tickers(tickers)

# Print the results
if not potential_operations:
    print("None of the tickers have potential for an operation based on the current strategy.")
else:
    for ticker, operation in potential_operations:
        print(f"{ticker} has a potential {operation} signal based on the current strategy.")
