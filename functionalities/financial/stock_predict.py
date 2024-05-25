import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Load historical stock data
data = pd.read_csv('AAPL_today.csv')

# Preprocess data
data['Datetime'] = pd.to_datetime(data['Datetime'])
data.set_index('Datetime', inplace=True)

# Fit ARIMA model
model = ARIMA(data['Close'], order=(5,1,0))
model_fit = model.fit()

forecast = model_fit.forecast(steps=30)

# Plot historical data and predictions
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Close'], color='blue', label='Historical Data')
plt.plot(forecast.index, forecast, color='red', linestyle='--', label='Predicted Data')
plt.scatter(forecast.index, forecast, color='red')  # Mark predicted points
plt.title('Historical Stock Price and Predicted Data')
plt.xlabel('Datetime')
plt.ylabel('Stock Price')
plt.legend()
plt.grid(True)
plt.show()
