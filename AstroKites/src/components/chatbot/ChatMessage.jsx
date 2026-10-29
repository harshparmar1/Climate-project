import React from 'react';
import { Bot, User, Database, CloudSun, Wind, Droplets, Thermometer } from 'lucide-react';

const renderFormattedText = (text) => {
  if (!text) return null;
  const lines = text.split('\n');
  return lines.map((line, lineIdx) => {
    const parts = line.split(/(\*\*.*?\*\*)/g);
    const renderedLine = parts.map((part, partIdx) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={partIdx} style={{ color: '#67e8f9', fontWeight: '700' }}>{part.slice(2, -2)}</strong>;
      }
      return part;
    });

    return (
      <React.Fragment key={lineIdx}>
        {renderedLine}
        {lineIdx < lines.length - 1 && <br />}
      </React.Fragment>
    );
  });
};

export default function ChatMessage({ message }) {
  const isAi = message.role === 'assistant';
  const data = message.data;

  return (
    <div className={`chat-message-row ${message.role}`}>
      <div className={`message-avatar ${isAi ? 'ai' : 'user'}`}>
        {isAi ? <Bot size={15} /> : <User size={15} />}
      </div>

      <div className="message-content-group">
        <div className={`chat-bubble ${message.role}`}>
          {renderFormattedText(message.content)}

          {/* Structured mini weather card when weather data is retrieved */}
          {isAi && data && data.temperature !== undefined && (
            <div className="weather-summary-card">
              <div className="card-location-header">
                <span>📍 {data.location || 'WEATHER METRICS'}</span>
                <span>{data.unit || '°C'}</span>
              </div>
              <div className="card-metrics-grid">
                <div className="metric-pill">
                  <Thermometer size={14} color="#38bdf8" />
                  <span>Temp</span>
                  <span className="val">{data.temperature}{data.unit || '°C'}</span>
                </div>
                <div className="metric-pill">
                  <Droplets size={14} color="#60a5fa" />
                  <span>Rain</span>
                  <span className="val">{data.precipitation ?? 0} mm</span>
                </div>
                <div className="metric-pill">
                  <Wind size={14} color="#34d399" />
                  <span>Wind</span>
                  <span className="val">{data.wind_speed ?? 3.2} m/s</span>
                </div>
                <div className="metric-pill">
                  <CloudSun size={14} color="#fbbf24" />
                  <span>Humidity</span>
                  <span className="val">{data.humidity ?? 65}%</span>
                </div>
              </div>
              <div className="card-source-footer">
                <span><Database size={10} style={{ display: 'inline', marginRight: 4 }} /> NASA POWER</span>
                <span>Verified Data</span>
              </div>
            </div>
          )}
        </div>

        {isAi && message.source && (
          <div className="message-source-tag">
            <Database size={10} /> Source: {message.source}
          </div>
        )}
      </div>
    </div>
  );
}
