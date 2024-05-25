import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Define the stock ticker
ticker = 'AAPL'

# Fetch data for today
end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=6)).strftime('%Y-%m-%d')

# Download 15-minute interval data
data = yf.download(ticker, start=start_date, end=end_date, interval='1H')

# Save the data to a CSV file
file_path = f'{ticker}_today.csv'
data.to_csv(file_path)

print(f"Today's 15-minute interval data saved to {file_path}")
