import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# Load the CSV file with today's data
ticker = 'AAPL'
file_path_today = f'{ticker}_today.csv'
gold_today_data = pd.read_csv(file_path_today)

# Ensure Datetime is in datetime format
gold_today_data['Datetime'] = pd.to_datetime(gold_today_data['Datetime'])

# Calculate moving averages
gold_today_data['5_MA'] = gold_today_data['Close'].rolling(window=5).mean()
gold_today_data['20_MA'] = gold_today_data['Close'].rolling(window=20).mean()

# Calculate RSI
def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

gold_today_data['RSI'] = calculate_rsi(gold_today_data)

# Implement the strategy and calculate profit
gold_today_data['Signal'] = ''
gold_today_data['Profit'] = 0.0
buy_signal = False
buy_price = 0.0
investment = 100  # USD

for i in range(len(gold_today_data)):
    if not buy_signal:
        if (gold_today_data.loc[i, 'Close'] > gold_today_data.loc[i, '5_MA']) and \
           (gold_today_data.loc[i, 'Close'] > gold_today_data.loc[i, '20_MA']):
            gold_today_data.loc[i, 'Signal'] = 'Buy Signal'
            buy_signal = True
            buy_price = gold_today_data.loc[i, 'Close']
            shares_bought = investment / buy_price
    else:
        if (gold_today_data.loc[i, 'Close'] < gold_today_data.loc[i, '5_MA']) or \
           (gold_today_data.loc[i, 'RSI'] > 70):
            gold_today_data.loc[i, 'Signal'] = 'Sell Signal'
            buy_signal = False
            sell_price = gold_today_data.loc[i, 'Close']
            profit = shares_bought * (sell_price - buy_price)
            gold_today_data.loc[i, 'Profit'] = profit
        else:
            gold_today_data.loc[i, 'Signal'] = 'Hold'

# Calculate total profit
total_profit = gold_today_data['Profit'].sum()

# Save the updated dataframe to a new CSV file
gold_today_data.to_csv(f'{ticker}_15min_with_signals_and_profit.csv', index=False)

# Display the result
print(f"Total Profit: {total_profit}")
gold_today_data[['Datetime', 'Close', '5_MA', '20_MA', 'RSI', 'Signal', 'Profit']]
