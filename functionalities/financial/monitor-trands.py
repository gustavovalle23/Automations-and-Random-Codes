import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Define the stock ticker
ticker = 'AAPL'

# Fetch data for today
end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

# Download 15-minute interval data
data = yf.download(ticker, start=start_date, end=end_date, interval='5m')

# Filter today's data
data_today = data[data.index.date == datetime.now().date()]

# Save the data to a CSV file
file_path = f'{ticker}_today.csv'
data.to_csv(file_path)

print(f"Today's 15-minute interval data saved to {file_path}")

file_path_today = f'{ticker}_today.csv'
today_data = pd.read_csv(file_path_today)

# Ensure Datetime is in datetime format
today_data['Datetime'] = pd.to_datetime(today_data['Datetime'])

# Calculate Moving Averages
today_data['5_MA'] = today_data['Close'].rolling(window=5).mean()
today_data['20_MA'] = today_data['Close'].rolling(window=20).mean()

# Calculate RSI
def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

today_data['RSI'] = calculate_rsi(today_data)

# Calculate MACD
def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    short_ema = data['Close'].ewm(span=short_window, adjust=False).mean()
    long_ema = data['Close'].ewm(span=long_window, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    return macd, signal

today_data['MACD'], today_data['Signal_Line'] = calculate_macd(today_data)

# Calculate Bollinger Bands
def calculate_bollinger_bands(data, window=20, no_of_std=2):
    rolling_mean = data['Close'].rolling(window).mean()
    rolling_std = data['Close'].rolling(window).std()
    upper_band = rolling_mean + (rolling_std * no_of_std)
    lower_band = rolling_mean - (rolling_std * no_of_std)
    return rolling_mean, upper_band, lower_band

today_data['BB_Mid'], today_data['BB_Upper'], today_data['BB_Lower'] = calculate_bollinger_bands(today_data)

# Plot the data with all indicators
fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(14, 15))

# Plot the close price, moving averages, and Bollinger Bands
ax1.plot(today_data['Datetime'], today_data['Close'], label='Close Price', color='blue')
ax1.plot(today_data['Datetime'], today_data['5_MA'], label='5-MA', color='green')
ax1.plot(today_data['Datetime'], today_data['20_MA'], label='20-MA', color='red')
ax1.plot(today_data['Datetime'], today_data['BB_Upper'], label='Bollinger Upper Band', color='grey')
ax1.plot(today_data['Datetime'], today_data['BB_Lower'], label='Bollinger Lower Band', color='grey')
ax1.fill_between(today_data['Datetime'], today_data['BB_Lower'], today_data['BB_Upper'], color='grey', alpha=0.1)
ax1.set_title(f'{ticker} Stock Price with Moving Averages and Bollinger Bands')
ax1.set_xlabel('Time')
ax1.set_ylabel('Price')
ax1.legend()
ax1.grid(True)

# Plot the RSI
ax2.plot(today_data['Datetime'], today_data['RSI'], label='RSI', color='purple')
ax2.axhline(70, linestyle='--', color='red', label='Overbought')
ax2.axhline(30, linestyle='--', color='green', label='Oversold')
ax2.set_title('Relative Strength Index (RSI)')
ax2.set_xlabel('Time')
ax2.set_ylabel('RSI')
ax2.legend()
ax2.grid(True)

# Plot the MACD
ax3.plot(today_data['Datetime'], today_data['MACD'], label='MACD', color='blue')
ax3.plot(today_data['Datetime'], today_data['Signal_Line'], label='Signal Line', color='red')
ax3.set_title('MACD')
ax3.set_xlabel('Time')
ax3.set_ylabel('MACD')
ax3.legend()
ax3.grid(True)

plt.tight_layout()
plt.show()

# Save the updated dataframe to a new CSV file
today_data.to_csv(f'{ticker}_15min_with_all_indicators.csv', index=False)
