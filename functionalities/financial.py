import yfinance as yf
import matplotlib.pyplot as plt
from ta.utils import dropna
from ta.volatility import BollingerBands
from ta.trend import SMAIndicator, EMAIndicator
from ta.momentum import RSIIndicator
from ta.trend import MACD
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import mplfinance as mpf



def plot_bollinger_bands(ticker_symbol, data):
    df = data[['Close']].copy()

    df = dropna(df)

    indicator_bb = BollingerBands(close=df["Close"], window=20, window_dev=2)

    # Add Bollinger Bands features
    df['bb_bbm'] = indicator_bb.bollinger_mavg()
    df['bb_bbh'] = indicator_bb.bollinger_hband()
    df['bb_bbl'] = indicator_bb.bollinger_lband()

    # Plotting
    plt.figure(figsize=(14,7))
    plt.plot(df.index, df['Close'], color='blue', label='Close Price')
    plt.plot(df.index, df['bb_bbm'], color='orange', label='Middle Band')
    plt.plot(df.index, df['bb_bbh'], color='red', label='Upper Band')
    plt.plot(df.index, df['bb_bbl'], color='green', label='Lower Band')
    plt.title(f"{ticker_symbol} Bollinger Bands")
    plt.legend()
    plt.show()

def plot_ma_ema(ticker_symbol, data, window):
    data = yf.download(ticker_symbol, start=start_date, end=end_date)

    df = data[['Close']].copy()

    df = dropna(df)

    # Initialize Simple Moving Average (SMA) and Exponential Moving Average (EMA) indicators
    sma = SMAIndicator(close=df["Close"], window=window)
    ema = EMAIndicator(close=df["Close"], window=window)

    df['sma'] = sma.sma_indicator()
    df['ema'] = ema.ema_indicator()

    # Plotting
    plt.figure(figsize=(14,7))
    plt.plot(df.index, df['Close'], color='blue', label='Close Price')
    plt.plot(df.index, df['sma'], color='orange', label=f'SMA ({window} periods)')
    plt.plot(df.index, df['ema'], color='red', label=f'EMA ({window} periods)')
    plt.title(f"{ticker_symbol} Moving Averages")
    plt.legend()
    plt.show()


def plot_rsi(ticker_symbol, data, window=14):
    # Extracting close price from the fetched data
    df = data[['Close']].copy()

    # Clean NaN values
    df = dropna(df)

    # Initialize RSI Indicator
    rsi = RSIIndicator(close=df["Close"], window=window)

    # Add RSI feature
    df['rsi'] = rsi.rsi()

    # Plotting
    plt.figure(figsize=(14,7))
    plt.plot(df.index, df['Close'], color='blue', label='Close Price')
    plt.title(f"{ticker_symbol} Price Chart with RSI")
    plt.legend(loc='upper left')

    # Create a secondary y-axis for RSI
    ax2 = plt.gca().twinx()

    ax2.plot(df.index, df['rsi'], color='orange', label=f'RSI ({window} periods)')
    ax2.axhline(70, linestyle='--', color='red')  # Overbought threshold
    ax2.axhline(30, linestyle='--', color='green')  # Oversold threshold
    ax2.set_ylabel('RSI')
    ax2.legend(loc='upper right')

    plt.show()


def plot_macd(ticker_symbol, data, window_short=12, window_long=26, signal_window=9):
    # Extracting close price from the fetched data
    df = data[['Close']].copy()

    # Clean NaN values
    df = dropna(df)

    # Initialize MACD Indicator
    macd = MACD(close=df["Close"], window_slow=window_long, window_fast=window_short, window_sign=signal_window)

    # Add MACD features
    df['macd'] = macd.macd()
    df['signal_line'] = macd.macd_signal()
    df['macd_histogram'] = macd.macd_diff()

    # Plotting
    plt.figure(figsize=(14,7))
    plt.plot(df.index, df['Close'], color='blue', label='Close Price')
    plt.title(f"{ticker_symbol} Price Chart with MACD")
    plt.legend(loc='upper left')

    # Create a secondary y-axis for MACD
    ax2 = plt.gca().twinx()
    ax2.plot(df.index, df['macd'], color='orange', label=f'MACD ({window_short},{window_long})')
    ax2.plot(df.index, df['signal_line'], color='red', label=f'Signal Line ({signal_window})')
    ax2.bar(df.index, df['macd_histogram'], color='gray', alpha=0.5, label='MACD Histogram')
    ax2.legend(loc='upper right')

    plt.show()

def plot_volume(ticker_symbol, data):
    # Clean NaN values
    data.dropna(inplace=True)

    # Plotting
    plt.figure(figsize=(14,7))
    plt.plot(data.index, data['Close'], color='blue', label='Close Price')
    plt.bar(data.index, data['Volume'], color='gray', alpha=0.5, label='Volume')
    plt.title(f"{ticker_symbol} Price Chart with Volume")
    plt.legend()
    plt.show()

def plot_support_resistance(ticker_symbol, data):

    # Extracting close price from the fetched data
    df = data[['Close']].copy()

    # Clean NaN values
    df = dropna(df)

    # Plotting
    plt.figure(figsize=(14,7))
    plt.plot(df.index, df['Close'], color='blue', label='Close Price')

    # Calculate support and resistance levels
    support_level = df['Close'].min()
    resistance_level = df['Close'].max()

    # Plot support and resistance levels
    plt.axhline(support_level, linestyle='--', color='green', label='Support Level')
    plt.axhline(resistance_level, linestyle='--', color='red', label='Resistance Level')

    plt.title(f"{ticker_symbol} Price Chart with Support and Resistance Levels")
    plt.legend()
    plt.show()




def plot_candlestick_patterns(ticker_symbol, data):
    # Clean NaN values
    data.dropna(inplace=True)

    # Convert index to matplotlib dates
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].map(mdates.date2num)

    # Plotting
    fig, ax = plt.subplots(figsize=(14,7))

    # Plot candlestick chart
    candlestick_ohlc(ax, data.values, width=0.6, colorup='g', colordown='r', alpha=0.5)

    ax.xaxis_date()
    ax.autoscale_view()
    ax.set_title(f"{ticker_symbol} Candlestick Chart")
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')

    plt.show()


ticker_symbol = "AAPL"
start_date = "2023-01-01"
end_date = "2024-01-01"

data = yf.download(ticker_symbol, start=start_date, end=end_date)


# plot_bollinger_bands(ticker_symbol, data)
# plot_ma_ema(ticker_symbol, data, window=20)
# plot_rsi(ticker_symbol, data)
# plot_macd(ticker_symbol, data, window_short=12, window_long=26, signal_window=9)
# plot_volume(ticker_symbol, data)
# plot_support_resistance(ticker_symbol, data)
# plot_candlestick_patterns(ticker_symbol, data)
