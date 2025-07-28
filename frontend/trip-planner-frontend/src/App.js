import React, { useState } from 'react';
import './App.css';
import { backendUrl } from './config';

function App() {
  const [destination, setDestination] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [preferences, setPreferences] = useState('');
  const [itinerary, setItinerary] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setItinerary(null);
    const res = await fetch(`${backendUrl}/plan_trip`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        destination,
        start_date: startDate,
        end_date: endDate,
        preferences
      })
    });
    const data = await res.json();
    setItinerary(data);
    setLoading(false);
  };

  return (
    <div className="App">
      <div className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">
            <span className="gradient-text">Trip Planner</span>
          </h1>
          <p className="hero-subtitle">Plan your perfect adventure with AI-powered itineraries</p>
        </div>
      </div>

      <div className="main-container">
        <div className="form-card">
          <h2 className="form-title">Plan Your Trip</h2>
          <form onSubmit={handleSubmit} className="trip-form">
            <div className="form-group">
              <label htmlFor="destination">Destination</label>
              <input
                id="destination"
                type="text"
                placeholder="Where do you want to go?"
                value={destination}
                onChange={e => setDestination(e.target.value)}
                required
                className="form-input"
              />
            </div>

            <div className="date-group">
              <div className="form-group">
                <label htmlFor="startDate">Start Date</label>
                <input
                  id="startDate"
                  type="date"
                  value={startDate}
                  onChange={e => setStartDate(e.target.value)}
                  required
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label htmlFor="endDate">End Date</label>
                <input
                  id="endDate"
                  type="date"
                  value={endDate}
                  onChange={e => setEndDate(e.target.value)}
                  required
                  className="form-input"
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="preferences">Preferences (Optional)</label>
              <textarea
                id="preferences"
                placeholder="Tell us about your interests: museums, food, culture, nature, shopping, etc."
                value={preferences}
                onChange={e => setPreferences(e.target.value)}
                className="form-textarea"
                rows="3"
              />
            </div>

            <button 
              type="submit" 
              disabled={loading}
              className={`submit-btn ${loading ? 'loading' : ''}`}
            >
              {loading ? (
                <div className="loading-content">
                  <div className="spinner"></div>
                  <span>Planning your trip...</span>
                </div>
              ) : (
                'Plan My Trip'
              )}
            </button>
          </form>
        </div>

        {itinerary && (
          <div className="itinerary-section">
            <div className="itinerary-header">
              <h2 className="itinerary-title">
                Your {itinerary.destination} Adventure
              </h2>
              <div className="trip-dates">
                <span className="date-badge">
                  {new Date(itinerary.start_date).toLocaleDateString('en-US', { 
                    month: 'short', 
                    day: 'numeric' 
                  })}
                </span>
                <span className="date-separator">→</span>
                <span className="date-badge">
                  {new Date(itinerary.end_date).toLocaleDateString('en-US', { 
                    month: 'short', 
                    day: 'numeric' 
                  })}
                </span>
              </div>
            </div>

            {itinerary.preferences && (
              <div className="preferences-display">
                <strong>Your Preferences:</strong> {itinerary.preferences}
              </div>
            )}

            <div className="itinerary-grid">
              {itinerary.itinerary.map(day => (
                <div key={day.day} className="day-card">
                  <div className="day-header">
                    <span className="day-number">Day {day.day}</span>
                    <div className="day-line"></div>
                  </div>
                  <div className="activities-list">
                    {day.activities.map((activity, index) => (
                      <div key={index} className="activity-item">
                        <div className="activity-dot"></div>
                        <span className="activity-text">{activity}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            {itinerary.review && (
              <div className="review-section">
                <h3 className="review-title">AI Review & Suggestions</h3>
                <div className="review-content">
                  <p className="review-text">{itinerary.review.review}</p>
                  {itinerary.review.suggestions && itinerary.review.suggestions.length > 0 && (
                    <div className="suggestions">
                      <h4>Suggestions:</h4>
                      <ul className="suggestions-list">
                        {itinerary.review.suggestions.map((suggestion, index) => (
                          <li key={index} className="suggestion-item">
                            {suggestion}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
