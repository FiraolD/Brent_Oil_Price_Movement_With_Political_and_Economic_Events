# app.py
from flask import Flask, jsonify
import pandas as pd
import json
import os

app = Flask(__name__)

# --- Load Data ---
try:
    df = pd.read_csv('Data/BrentOilPrices.csv')
    df['Date'] = pd.to_datetime(df['Date'], format='mixed', dayfirst=True)
    df = df.sort_values('Date').reset_index(drop=True)
    print("✅ Brent crude prices loaded successfully")
except Exception as e:
    print(f"❌ Error loading brent_crude_prices.csv: {e}")

try:
    with open('Data/results.json', 'r') as f:
        results = json.load(f)
    print("✅ Model results loaded successfully")
except Exception as e:
    results = {"change_date": "2008-08-04", "prob_vol_increase": 0.95}
    print(f"⚠️  Using fallback results: {e}")

try:
    events_df = pd.read_csv('Data/events.csv')
    events_df['start_date'] = pd.to_datetime(events_df['start_date'], format='mixed', dayfirst=True)
    print("✅ Events data loaded successfully")
except Exception as e:
    events_df = pd.DataFrame(columns=['event_name', 'event_type', 'start_date'])
    print(f"⚠️  Events.csv not loaded: {e}")

# --- API Routes ---

@app.route('/')
def home():
    return """
    <h1>🛢️ Brent Oil Dashboard API</h1>
    <p>✅ Backend is running!</p>
    <p>Available endpoints:</p>
    <ul>
        <li><a href="/api/prices">GET /api/prices</a> - Oil prices</li>
        <li><a href="/api/events">GET /api/events</a> - Key events</li>
        <li><a href="/api/results">GET /api/results</a> - Model results</li>
    </ul>
    """

@app.route('/api/prices')
def get_prices():
    try:
        data = df[['Date', 'Price']].dropna()
        return jsonify([
            {'Date': row['Date'].strftime('%Y-%m-%d'), 'Price': float(row['Price'])}
            for _, row in data.iterrows()
        ])
    except Exception as e:
        return jsonify({"error": f"Failed to load prices: {str(e)}"}), 500
    
    
@app.route('/api/results')
def get_results():
    return jsonify(results)

@app.route('/api/events')
def get_events():
    return jsonify(events_df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)