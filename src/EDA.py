# src/EDA.py

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Load the data
df = pd.read_csv('Data/BrentOilPrices.csv')

# Convert 'Date' to datetime using the correct format
df['Date'] = pd.to_datetime(df['Date'], format='mixed', dayfirst=True )

# Sort by date to ensure chronological order
df = df.sort_values('Date').reset_index(drop=True)

# Display basic info
print("Data loaded successfully!")
print(df.head())
print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
print(f"Shape: {df.shape}")

# Plot raw prices
plt.figure(figsize=(14, 6))
plt.plot(df['Date'], df['Price'], color='tab:blue')
plt.title('Brent Crude Oil Prices (1987–2022)')
plt.xlabel('Date')
plt.ylabel('Price (USD per barrel)')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# Compute log returns
df['LogReturn'] = np.log(df['Price'] / df['Price'].shift(1))
df.dropna(subset=['LogReturn'], inplace=True)

# Plot log returns
plt.figure(figsize=(14, 6))
plt.plot(df['Date'], df['LogReturn'], color='tab:orange', alpha=0.7)
plt.title('Log Returns of Brent Crude Prices')
plt.xlabel('Date')
plt.ylabel('Log Return')
plt.axhline(0, color='black', linestyle='--', linewidth=1)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# Rolling volatility (30-day)
df['Volatility'] = df['LogReturn'].rolling(30).std()
plt.figure(figsize=(14, 6))
plt.plot(df['Date'], df['Volatility'], color='purple')
plt.title('30-Day Rolling Volatility of Brent Crude Prices')
plt.xlabel('Date')
plt.ylabel('Volatility (Std Dev of Log Returns)')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()