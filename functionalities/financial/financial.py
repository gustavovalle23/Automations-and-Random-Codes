import yfinance as yf
import matplotlib.pyplot as plt
from ta.utils import dropna
from ta.volatility import BollingerBands
from ta.trend import SMAIndicator, EMAIndicator
from ta.momentum import RSIIndicator
from ta.trend import MACD


def plot_bollinger_bands(ticker_symbol, data):
    df = data[['Close']].copy()

    df = dropna(df)

    indicator_bb = BollingerBands(close=df["Close"], window=20, window_dev=2)

    # Add Bollinger Bands features
    df['bb_bbm'] = indicator_bb.bollinger_mavg()
    df['bb_bbh'] = indicator_bb.bollinger_hband()
    df['bb_bbl'] = indicator_bb.bollinger_lband()

    # Define buy/sell signals
    df['buy_signal'] = df['Close'] < df['bb_bbl']  # Buy when price is below lower band
    df['sell_signal'] = df['Close'] > df['bb_bbh']  # Sell when price is above upper band

    # Plotting
    plt.figure(figsize=(14,7))
    plt.plot(df.index, df['Close'], color='blue', label='Close Price')
    plt.plot(df.index, df['bb_bbm'], color='orange', label='Middle Band')
    plt.plot(df.index, df['bb_bbh'], color='red', label='Upper Band')
    plt.plot(df.index, df['bb_bbl'], color='green', label='Lower Band')

    # Plot buy/sell signals
    plt.plot(df.index[df['buy_signal']], df['Close'][df['buy_signal']], '^', markersize=10, color='g', lw=0, label='Buy Signal')
    plt.plot(df.index[df['sell_signal']], df['Close'][df['sell_signal']], 'v', markersize=10, color='r', lw=0, label='Sell Signal')

    plt.title(f"{ticker_symbol} Bollinger Bands with Buy/Sell Signals")
    plt.legend()
    plt.show()



def plot_ma_ema(ticker_symbol, data, window):
    df = data[['Close']].copy()

    df = dropna(df)

    sma = SMAIndicator(close=df["Close"], window=window)
    ema = EMAIndicator(close=df["Close"], window=window)

    df['sma'] = sma.sma_indicator()
    df['ema'] = ema.ema_indicator()

    # Define buy/sell signals
    df['buy_signal'] = df['sma'] > df['ema']  # Buy when SMA crosses above EMA
    df['sell_signal'] = df['sma'] < df['ema']  # Sell when SMA crosses below EMA

    plt.figure(figsize=(14,7))
    plt.plot(df.index, df['Close'], color='blue', label='Close Price')
    plt.plot(df.index, df['sma'], color='orange', label=f'SMA ({window} periods)')
    plt.plot(df.index, df['ema'], color='red', label=f'EMA ({window} periods)')

    # Plot buy/sell signals
    plt.plot(df.index[df['buy_signal']], df['Close'][df['buy_signal']], '^', markersize=10, color='g', lw=0, label='Buy Signal')
    plt.plot(df.index[df['sell_signal']], df['Close'][df['sell_signal']], 'v', markersize=10, color='r', lw=0, label='Sell Signal')

    plt.title(f"{ticker_symbol} Moving Averages with Buy/Sell Signals")
    plt.legend()
    plt.show()


def plot_rsi(ticker_symbol, data, window=14):
    df = data[['Close']].copy()

    df = dropna(df)

    rsi = RSIIndicator(close=df["Close"], window=window)

    df['rsi'] = rsi.rsi()

    # Define buy/sell signals
    df['buy_signal'] = df['rsi'] < 30  # Buy when RSI is below 30 (oversold)
    df['sell_signal'] = df['rsi'] > 70  # Sell when RSI is above 70 (overbought)

    plt.figure(figsize=(14,7))
    plt.plot(df.index, df['Close'], color='blue', label='Close Price')
    plt.title(f"{ticker_symbol} Price Chart with RSI")
    plt.legend(loc='upper left')

    ax2 = plt.gca().twinx()

    ax2.plot(df.index, df['rsi'], color='orange', label=f'RSI ({window} periods)')
    ax2.axhline(70, linestyle='--', color='red')  
    ax2.axhline(30, linestyle='--', color='green')  
    ax2.set_ylabel('RSI')
    ax2.legend(loc='upper right')

    # Plot buy/sell signals
    plt.plot(df.index[df['buy_signal']], df['Close'][df['buy_signal']], '^', markersize=10, color='g', lw=0, label='Buy Signal')
    plt.plot(df.index[df['sell_signal']], df['Close'][df['sell_signal']], 'v', markersize=10, color='r', lw=0, label='Sell Signal')

    plt.show()


def plot_macd(ticker_symbol, data, window_short=12, window_long=26, signal_window=9):
    df = data[['Close']].copy()

    df = dropna(df)

    macd = MACD(close=df["Close"], window_slow=window_long, window_fast=window_short, window_sign=signal_window)

    df['macd'] = macd.macd()
    df['signal_line'] = macd.macd_signal()
    df['macd_histogram'] = macd.macd_diff()

    # Define buy/sell signals
    df['buy_signal'] = df['macd'] > df['signal_line']  # Buy when MACD crosses above signal line
    df['sell_signal'] = df['macd'] < df['signal_line']  # Sell when MACD crosses below signal line

    plt.figure(figsize=(14,7))
    plt.plot(df.index, df['Close'], color='blue', label='Close Price')
    plt.title(f"{ticker_symbol} Price Chart with MACD")
    plt.legend(loc='upper left')

    ax2 = plt.gca().twinx()
    ax2.plot(df.index, df['macd'], color='orange', label=f'MACD ({window_short},{window_long})')
    ax2.plot(df.index, df['signal_line'], color='red', label=f'Signal Line ({signal_window})')
    ax2.bar(df.index, df['macd_histogram'], color='gray', alpha=0.5, label='MACD Histogram')
    ax2.legend(loc='upper right')

    # Plot buy/sell signals
    plt.plot(df.index[df['buy_signal']], df['Close'][df['buy_signal']], '^', markersize=10, color='g', lw=0, label='Buy Signal')
    plt.plot(df.index[df['sell_signal']], df['Close'][df['sell_signal']], 'v', markersize=10, color='r', lw=0, label='Sell Signal')

    plt.show()


def plot_volume(ticker_symbol, data):
    data.dropna(inplace=True)

    plt.figure(figsize=(14,7))
    plt.plot(data.index, data['Close'], color='blue', label='Close Price')
    plt.bar(data.index, data['Volume'], color='gray', alpha=0.5, label='Volume')
    plt.title(f"{ticker_symbol} Price Chart with Volume")
    plt.legend()
    plt.show()


def plot_support_resistance(ticker_symbol, data):
    df = data[['Close']].copy()

    df = dropna(df)

    plt.figure(figsize=(14,7))
    plt.plot(df.index, df['Close'], color='blue', label='Close Price')

    support_level = df['Close'].min()
    resistance_level = df['Close'].max()

    plt.axhline(support_level, linestyle='--', color='green', label='Support Level')
    plt.axhline(resistance_level, linestyle='--', color='red', label='Resistance Level')

    plt.title(f"{ticker_symbol} Price Chart with Support and Resistance Levels")
    plt.legend()
    plt.show()

ticker_symbol = "AAPL"
data = yf.download(ticker_symbol, interval='1h', period='1d')

plot_bollinger_bands(ticker_symbol, data)
plot_ma_ema(ticker_symbol, data, window=20)
plot_rsi(ticker_symbol, data)
plot_macd(ticker_symbol, data, window_short=12, window_long=26, signal_window=9)
plot_volume(ticker_symbol, data)
plot_support_resistance(ticker_symbol, data)
