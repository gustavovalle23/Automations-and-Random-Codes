import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime, timedelta
import ta
import time

# Initialize MT5 connection
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()

ticker = 'USDJPY'
timeframe = mt5.TIMEFRAME_H1  # 15-minute interval

while True:
    # Define the date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=6)

    # Get the date range for MT5
    utc_from = datetime(start_date.year, start_date.month, start_date.day)
    utc_to = datetime(end_date.year, end_date.month, end_date.day + 1)

    # Download the data
    rates = mt5.copy_rates_range(ticker, timeframe, utc_from, utc_to)

    # Check if data is received
    if rates is None:
        print(f"No data for {ticker}")
        mt5.shutdown()
    else:
        # Convert to DataFrame
        data = pd.DataFrame(rates)
        
        # Convert time in seconds to datetime
        data['time'] = pd.to_datetime(data['time'], unit='s')
        
        # Save the data to a CSV file
        file_path = 'today.csv'
        data.to_csv(file_path, index=False)

        # Ensure Datetime is in datetime format
        today_data = data.copy()
        today_data.rename(columns={'time': 'Datetime', 'close': 'Close', 'high': 'High', 'low': 'Low', 'open': 'Open', 'tick_volume': 'Volume'}, inplace=True)

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

        # Initialize symbol in the market watch
        if not mt5.symbol_select(ticker):
            print(f"\nERROR - Failed to select '{ticker}' in MetaTrader 5 with error :", mt5.last_error())
            mt5.shutdown()

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

        if today_data.loc[i, 'Signal'] == 'Buy' and not buy_signal:
            buy_signal = True
            buy_price = today_data.loc[i, 'Close']
            shares_bought = investment / buy_price

            # Place a buy order
            order = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": ticker,
                "volume": 0.1,
                "type": mt5.ORDER_TYPE_BUY,
                "price": mt5.symbol_info_tick(ticker).ask,
                "deviation": 20,
                "magic": 234000,
                "comment": "Python script open",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_RETURN,
            }

            print('sending buy order', order)
            result = mt5.order_send(order)
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print(f"Order send failed, retcode={result}")

        elif (today_data.loc[i, 'Signal'] == 'Sell' or today_data.loc[i, 'Signal'] == 'Sell') and buy_signal:
            buy_signal = False
            sell_price = today_data.loc[i, 'Close']
            profit = shares_bought * (sell_price - buy_price)
            today_data.loc[i, 'Profit'] = profit

            # Place a sell order
            order = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": ticker,
                "volume": 0.1,
                "type": mt5.ORDER_TYPE_SELL,
                "price": mt5.symbol_info_tick(ticker).bid,
                "deviation": 20,
                "magic": 234000,
                "comment": "Python script close",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_RETURN,
            }

            print('sending sell order', order)
            result = mt5.order_send(order)
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print(f"Order send failed, retcode={result}")

    # Calculate total profit
    total_profit = today_data['Profit'].sum()
    print(f"Total Profit: {total_profit}")
    print(today_data[['Datetime', 'Close', '5_MA', '20_MA', 'RSI', 'Signal', 'Profit']])

    time.sleep(10)  # Wait before checking again
