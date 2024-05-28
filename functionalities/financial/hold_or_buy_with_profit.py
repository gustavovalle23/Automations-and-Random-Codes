import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import ta

# Load the CSV file with today's data
ticker = 'AMD'

end_date = datetime.now()
start_date = end_date - timedelta(days=6)

# Download 15-minute interval data
data = yf.download(tickers=ticker, period='1d', interval='5m')

# Save the data to a CSV file
file_path = f'today.csv'
data.to_csv(file_path)

file_path_today = f'today.csv'
today_data = pd.read_csv(file_path_today)

# Ensure Datetime is in datetime format
today_data['Datetime'] = pd.to_datetime(today_data['Datetime'])

# Calculate moving averages
today_data['5_MA'] = today_data['Close'].rolling(window=5).mean()
today_data['20_MA'] = today_data['Close'].rolling(window=20).mean()

# Calculate additional indicators
today_data['RSI'] = ta.momentum.rsi(today_data['Close'], window=14)
today_data['STOCH_K'] = ta.momentum.stoch(today_data['High'], today_data['Low'], today_data['Close'], window=9, smooth_window=6)
today_data['STOCHRSI'] = ta.momentum.stochrsi_k(today_data['Close'], window=14)
today_data['MACD'] = ta.trend.macd_diff(today_data['Close'], window_slow=26, window_fast=12)
today_data['ADX'] = ta.trend.adx(today_data['High'], today_data['Low'], today_data['Close'], window=14)
today_data['Williams %R'] = ta.momentum.williams_r(today_data['High'], today_data['Low'], today_data['Close'], lbp=14)
today_data['CCI'] = ta.trend.cci(today_data['High'], today_data['Low'], today_data['Close'], window=14)
today_data['ATR'] = ta.volatility.average_true_range(today_data['High'], today_data['Low'], today_data['Close'], window=14)
today_data['Highs_Lows'] = ta.trend.stc(today_data['Close'], window_slow=50, window_fast=23, cycle=10)
today_data['Ultimate_Oscillator'] = ta.momentum.ultimate_oscillator(today_data['High'], today_data['Low'], today_data['Close'])
today_data['ROC'] = ta.momentum.roc(today_data['Close'], window=12)
today_data['Bull_Bear_Power'] = today_data['Close'] - ta.trend.ema_indicator(today_data['Close'], window=13)

# Implement the strategy and calculate profit
today_data['Signal'] = ''
today_data['Profit'] = 0.0
buy_signal = False
buy_price = 0.0
investment = 100  # USD

def classify_signals(row):
    signals = []
    
    if row['RSI'] > 70:
        signals.append('Overbought')
    elif row['RSI'] < 30:
        signals.append('Oversold')
    
    if row['STOCH_K'] > 80:
        signals.append('Overbought')
    elif row['STOCH_K'] < 20:
        signals.append('Oversold')
    
    if row['STOCHRSI'] > 80:
        signals.append('Overbought')
    elif row['STOCHRSI'] < 20:
        signals.append('Oversold')
    
    if row['MACD'] > 0:
        signals.append('Buy')
    else:
        signals.append('Sell')
    
    if row['ADX'] > 25:
        signals.append('Buy')
    
    if row['Williams %R'] > -20:
        signals.append('Overbought')
    elif row['Williams %R'] < -80:
        signals.append('Oversold')
    
    if row['CCI'] > 100:
        signals.append('Buy')
    elif row['CCI'] < -100:
        signals.append('Sell')
    
    if row['ATR'] < today_data['ATR'].mean():
        signals.append('Less Volatility')
    
    if row['Highs_Lows'] > 0:
        signals.append('Buy')
    elif row['Highs_Lows'] < 0:
        signals.append('Sell')
    
    if row['Ultimate_Oscillator'] > 70:
        signals.append('Overbought')
    elif row['Ultimate_Oscillator'] < 30:
        signals.append('Oversold')
    
    if row['ROC'] > 0:
        signals.append('Buy')
    else:
        signals.append('Sell')
    
    if row['Bull_Bear_Power'] > 0:
        signals.append('Buy')
    else:
        signals.append('Sell')
    
    return signals

today_data['Combined_Signals'] = today_data.apply(classify_signals, axis=1)

for i in range(len(today_data)):
    signals = today_data.loc[i, 'Combined_Signals']
    buy_signals = signals.count('Buy')
    sell_signals = signals.count('Sell')
    overbought_signals = signals.count('Overbought')
    oversold_signals = signals.count('Oversold')
    
    if buy_signals >= 6:
        today_data.loc[i, 'Signal'] = 'Strong Buy'
    elif buy_signals >= 3:
        today_data.loc[i, 'Signal'] = 'Buy'
    elif sell_signals >= 6:
        today_data.loc[i, 'Signal'] = 'Strong Sell'
    elif sell_signals >= 3:
        today_data.loc[i, 'Signal'] = 'Sell'
    else:
        today_data.loc[i, 'Signal'] = 'Neutral'

    if today_data.loc[i, 'Signal'] == 'Strong Buy' and not buy_signal:
        buy_signal = True
        buy_price = today_data.loc[i, 'Close']
        shares_bought = investment / buy_price
    elif (today_data.loc[i, 'Signal'] == 'Strong Sell' or today_data.loc[i, 'Signal'] == 'Sell') and buy_signal:
        buy_signal = False
        sell_price = today_data.loc[i, 'Close']
        profit = shares_bought * (sell_price - buy_price)
        today_data.loc[i, 'Profit'] = profit

# Calculate total profit
total_profit = today_data['Profit'].sum()

# Save the updated dataframe to a new CSV file
today_data.to_csv(f'15min_with_signals_and_profit.csv', index=False)

# Display the result
print(f"Total Profit: {total_profit}")
print(today_data[['Datetime', 'Close', '5_MA', '20_MA', 'RSI', 'Signal', 'Profit']])
