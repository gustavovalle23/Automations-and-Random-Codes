import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

# Function to identify engulfing patterns
def identify_engulfing_patterns(data):
    data['Signal'] = 'Hold'
    for i in range(1, len(data)):
        prev_open = data.loc[i - 1, 'Open']
        prev_close = data.loc[i - 1, 'Close']
        curr_open = data.loc[i, 'Open']
        curr_close = data.loc[i, 'Close']

        # Bullish Engulfing
        if prev_close < prev_open and curr_close > curr_open and curr_open < prev_close and curr_close > prev_open:
            data.loc[i, 'Signal'] = 'Buy'
        
        # Bearish Engulfing
        elif prev_close > prev_open and curr_close < curr_open and curr_open > prev_close and curr_close < prev_open:
            data.loc[i, 'Signal'] = 'Sell'

    return data

# Load historical stock data from a CSV file
file_path = 'AAPL_today.csv'  # Replace with your CSV file path
data = pd.read_csv(file_path)

# Ensure the data is sorted by date
data['Datetime'] = pd.to_datetime(data['Datetime'])
data = data.sort_values('Datetime')

# Identify engulfing patterns and add signals
data = identify_engulfing_patterns(data)

# Plotting
buy_signals = data[data['Signal'] == 'Buy']
sell_signals = data[data['Signal'] == 'Sell']

# Configure the plot style
mpf_style = mpf.make_mpf_style(base_mpf_style='classic', mavcolors=['#1f77b4', '#ff7f0e', '#2ca02c'])

# Create the plot
fig, axes = mpf.plot(data.set_index('Datetime'),
                     type='candle',
                     style=mpf_style,
                     title='Stock Price with Engulfing Patterns',
                     ylabel='Price',
                     volume=True,
                     returnfig=True)

# Plot Buy signals
axes[0].plot(buy_signals['Datetime'], buy_signals['Close'], '^', markersize=10, color='green', label='Buy Signal')

# Plot Sell signals
axes[0].plot(sell_signals['Datetime'], sell_signals['Close'], 'v', markersize=10, color='red', label='Sell Signal')

# Adding legend
axes[0].legend()

# Save the plot
plt.savefig('engulfing_patterns_plot.png')

# Show the plot
plt.show()
