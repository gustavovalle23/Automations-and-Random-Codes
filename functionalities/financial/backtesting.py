import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_intraday_data(ticker, date, interval='1m'):
    start_date = pd.Timestamp(date) - pd.Timedelta(days=1)
    end_date = pd.Timestamp(date) + pd.Timedelta(days=1)
    stock_data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    print(stock_data)
    # stock_data = stock_data.loc[date]
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

def day_trade_strategy(data, short_window=9, long_window=21, volatility_threshold=0.3, rsi_threshold=50, stop_loss_pct=0.01):
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
    
    # Generate positions
    data['Position'] = 0
    data['Position'] = data['Long_Signal'] - data['Short_Signal']
    
    # Track entry price and stop loss levels
    data['Entry_Price'] = np.where(data['Position'] != 0, data['Close'], np.nan)
    data['Entry_Price'] = data['Entry_Price'].ffill()
    data['Stop_Loss'] = np.where(data['Position'] == 1, data['Entry_Price'] * (1 - stop_loss_pct), data['Entry_Price'] * (1 + stop_loss_pct))
    
    return data

def backtest_day_trade_strategy(data, initial_capital=100):
    positions = pd.DataFrame(index=data.index).fillna(0.0)
    positions['Stock'] = data['Position']
    
    portfolio = positions.multiply(data['Close'], axis=0)
    pos_diff = positions.diff()
    
    portfolio['holdings'] = (positions.multiply(data['Close'], axis=0)).sum(axis=1)
    portfolio['cash'] = initial_capital - (pos_diff.multiply(data['Close'], axis=0)).sum(axis=1).cumsum()
    portfolio['total'] = portfolio['cash'] + portfolio['holdings']
    
    portfolio['returns'] = portfolio['total'].pct_change()
    
    # Apply stop loss
    stop_loss_hits = ((data['Position'] == 1) & (data['Close'] <= data['Stop_Loss'])) | ((data['Position'] == -1) & (data['Close'] >= data['Stop_Loss']))
    if stop_loss_hits.any():
        stop_loss_indices = data.index[stop_loss_hits]
        for index in stop_loss_indices:
            if positions['Stock'].loc[index] != 0:
                portfolio['cash'].loc[index:] = portfolio['cash'].loc[index] + positions['Stock'].loc[index] * data['Close'].loc[index]
                portfolio['holdings'].loc[index:] = 0
                portfolio['total'].loc[index:] = portfolio['cash'].loc[index]
                positions['Stock'].loc[index:] = 0
    
    return portfolio

def generate_backtesting(ticker):
  date = '2024-05-30'
  short_window = 9
  long_window = 21
  volatility_threshold = 0.3
  rsi_threshold = 50
  stop_loss_pct = 0.01  # 1% stop loss
  initial_capital = 100

  # Get intraday stock data for the specific date
  stock_data = get_intraday_data(ticker, date)

  # Calculate volatility
  stock_data = calculate_volatility(stock_data)

  # Apply day trading strategy
  strategy_data = day_trade_strategy(stock_data, short_window, long_window, volatility_threshold, rsi_threshold, stop_loss_pct)

  # Backtest the strategy
  portfolio = backtest_day_trade_strategy(strategy_data, initial_capital)

  # Plot results
  # plt.figure(figsize=(12, 8))
  # plt.plot(portfolio['total'], label='Total Portfolio Value')
  # plt.plot(strategy_data['Close'], label='Stock Price')
  # plt.legend(loc='best')
  # plt.title(f'Momentum Day Trading Strategy Backtest for {date}')
  # plt.xlabel('Time')
  # plt.ylabel('Value')
  # plt.show()

  # Print final portfolio value and performance metrics
  print(f"Final Portfolio Value: ${portfolio['total'].iloc[-1]:.2f}")
  print(f"{ticker} Total Return: {(portfolio['total'].iloc[-1] - initial_capital) / initial_capital * 100:.2f}%")


generate_backtesting("EURUSD=X")
