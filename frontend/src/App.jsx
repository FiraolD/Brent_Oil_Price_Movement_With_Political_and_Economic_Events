// frontend/src/App.jsx
import React, { useEffect, useState } from 'react';

function App() {
  const [prices, setPrices] = useState([]);
  const [events, setEvents] = useState([]);
  const [results, setResults] = useState(null);

  useEffect(() => {
    // Fetch data from Flask backend
    const fetchData = async () => {
      try {
        const pricesRes = await fetch('http://localhost:5000/api/prices');
        const eventsRes = await fetch('http://localhost:5000/api/events');
        const resultsRes = await fetch('http://localhost:5000/api/results');

        const pricesData = await pricesRes.json();
        const eventsData = await eventsRes.json();
        const resultsData = await resultsRes.json();

        setPrices(pricesData);
        setEvents(eventsData);
        setResults(resultsData);
      } catch (err) {
        console.error("Error fetching data:", err);
        alert("Failed to load data. Is Flask running on http://localhost:5000?");
      }
    };

    fetchData();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>🛢️ Brent Oil Price Dashboard</h1>

      <h2>Latest Price Data</h2>
      <p>Total Prices Loaded: {prices.length}</p>
      {prices.length > 0 && (
        <p>First Price: ${prices[0].Price} on {prices[0].Date}</p>
      )}

      <h2>Key Events</h2>
      <ul>
        {events.map((e, i) => (
          <li key={i}>
            <strong>{e.event_name}</strong> - {e.event_date} ({e.event_type})
          </li>
        ))}
      </ul>

      <h2>Model Results</h2>
      {results ? (
        <div>
          <p><strong>Change Date:</strong> {results.change_date}</p>
          <p><strong>Volatility Increase Probability:</strong> {(results.prob_vol_increase * 100).toFixed(1)}%</p>
        </div>
      ) : (
        <p>Loading results...</p>
      )}
    </div>
  );
}

export default App;