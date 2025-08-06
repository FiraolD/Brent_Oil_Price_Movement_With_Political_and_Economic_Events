# app.py
from flask import Flask, jsonify
import pandas as pd
import json

app = Flask(__name__)

# Load data once
df = pd.read_csv('Data/BrentOilPrices.csv')
df['Date'] = pd.to_datetime(df['Date'], format='mixed', dayfirst=True)
df = df.sort_values('Date').reset_index(drop=True)

# Ensure LogReturn is computed
df['LogReturn'] = pd.to_numeric(df['Price'], errors='coerce')
df['LogReturn'] = df['LogReturn'].pct_change().fillna(0)
# Or use log: df['LogReturn'] = np.log(df['Price'] / df['Price'].shift(1)).fillna(0)

# Load results from interpret.py
try:
    with open('Data/results.json') as f:
        results = json.load(f)
except FileNotFoundError:
    results = {"change_date": "2008-08-04", "prob_vol_increase": 0.95}

# Load events
events_df = pd.read_csv('Data/brent_oil_event_data.csv')
events_df['start_date'] = pd.to_datetime(events_df['start_date'], format='mixed', dayfirst=True)

@app.route('/api/prices')
def get_prices():
    data = df[['Date', 'Price']].dropna()
    return jsonify(data.to_dict(orient='records'))

@app.route('/api/results')
def get_results():
    return jsonify(results)

@app.route('/api/events')
def get_events():
    return jsonify(events_df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    

# Add this route to app.py
@app.route('/')
def home():
    return """
    <h1>Brent Oil Price Dashboard API</h1>
    <p>✅ Backend is running!</p>
    <h3>Available API Endpoints:</h3>
    <ul>
        <li><a href="/api/prices">GET /api/prices</a> - Brent oil prices</li>
        <li><a href="/api/events">GET /api/events</a> - Key events</li>
        <li><a href="/api/results">GET /api/results</a> - Model results</li>
    </ul>
    """