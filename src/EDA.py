# src/EDA.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('Data/BrentOilPrices.csv')

# Parse mixed date formats
df['Date'] = pd.to_datetime(df['Date'], format='mixed', dayfirst=True)

# Sort and reset index
df = df.sort_values('Date').reset_index(drop=True)

# Save cleaned version
df.to_csv('Data/brent_cleaned.csv', index=False)

# Compute log returns
df['LogReturn'] = np.log(df['Price'] / df['Price'].shift(1))
df.dropna(inplace=True)

# Plotting
plt.figure(figsize=(14, 6))
plt.plot(df['Date'], df['Price'], label='Brent Crude Price', color='tab:blue')
plt.title('Brent Crude Oil Prices (1987–2022)')
plt.xlabel('Date')
plt.ylabel('Price (USD per barrel)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

plt.figure(figsize=(14, 6))
plt.plot(df['Date'], df['LogReturn'], color='tab:orange', alpha=0.7)
plt.axhline(0, color='black', linestyle='--', linewidth=1)
plt.title('Log Returns of Brent Crude Prices')
plt.xlabel('Date')
plt.ylabel('Log Return')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Rolling volatility
df['Volatility'] = df['LogReturn'].rolling(30).std()
plt.figure(figsize=(14, 6))
plt.plot(df['Date'], df['Volatility'], color='purple')
plt.title('30-Day Rolling Volatility')
plt.xlabel('Date')
plt.ylabel('Volatility (Std Dev)')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()