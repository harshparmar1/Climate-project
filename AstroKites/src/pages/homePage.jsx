import React from "react";
import { useNavigate } from "react-router-dom";
import EarthCanvas from "../component/EarthCanvas";
import ScrollReveal from "../component/ScrollReveal";
import "./home.css";

const Home = () => {
  const navigate = useNavigate();

  const handleExploreForecast = () => {
    navigate('/forecast');
  };

  return (
    <div className="home">
      {/* 3D Interactive Three.js Earth Background */}
      <EarthCanvas />

      {/* Chapter 01 & 02: SPACE & EARTH Hero */}
      <section className="hero">
        <div className="overlay">
          <div className="hero-content hero-large">
            <div className="chapter-badge">01 — SPACE & EARTH</div>
            <div className="hero-status-tag">
              <span className="status-dot-pulse"></span>
              <span>LIVE NASA POWER CLIMATE DATA CONSOLE</span>
            </div>
            <div className="topbar">
              <h1 className="hero-title">
                Precise <span className="highlight">weather</span>, precisely for you.
              </h1>
              <p className="hero-subtitle">
                Harness the power of probability-based forecasting for smarter decisions
              </p>
            </div>
            <button className="cta-button start" onClick={handleExploreForecast}>
              Explore Forecast
              <svg className="cta-arrow" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinejoin="round">
                <line x1="5" y1="12" x2="19" y2="12"></line>
                <polyline points="12 5 19 12 12 19"></polyline>
              </svg>
            </button>
          </div>
        </div>
      </section>

      {/* Chapter 03: ATMOSPHERE - About Section */}
      <section className="about">
        <div className="section-container">
          <ScrollReveal>
            <div className="chapter-badge">02 — ATMOSPHERE</div>
            <div className="about-glass-card">
              <h2>About Astrokites</h2>
              <p>
                Astrokites delivers hyper-local weather updates and interactive
                forecasts powered by <strong>probability-based analytics</strong> and statistical modeling. 
                Access both <strong>future weather predictions</strong> and <strong>historical weather data</strong> 
                to make smarter decisions with confidence scores and data-driven insights — 
                whether you're planning ahead or analyzing past weather patterns.
              </p>
            </div>
          </ScrollReveal>
        </div>
      </section>

      {/* Chapter 04: WEATHER - Features Grid Section */}
      <section className="features">
        <div className="section-container">
          <ScrollReveal>
            <div className="chapter-badge">03 — WEATHER INTELLIGENCE</div>
            <div className="section-header">
              <h2>Our Key Features</h2>
              <p className="section-subtitle">Comprehensive satellite metrics and statistical climate intelligence</p>
            </div>
          </ScrollReveal>
          
          <div className="feature-cards">
            <ScrollReveal delay={0}>
              <div className="feature">
                <h3>🌦 Real-Time Forecasts</h3>
                <p>
                  Get instant, location-based weather updates with probability-driven
                  insights.
                </p>
              </div>
            </ScrollReveal>
            <ScrollReveal delay={120}>
              <div className="feature">
                <h3>🗺 Dynamic Maps</h3>
                <p>
                  Visualize temperature, wind flow, and rain movements interactively
                  across regions with satellite imagery.
                </p>
              </div>
            </ScrollReveal>
            <ScrollReveal delay={240}>
              <div className="feature">
                <h3>⚡ Smart Alerts</h3>
                <p>
                  Receive early warnings for storms, rainfall, and changing weather
                  conditions via push notifications.
                </p>
              </div>
            </ScrollReveal>
            <ScrollReveal delay={360}>
              <div className="feature">
                <h3>📊 Advanced Analytics</h3>
                <p>
                  Comprehensive weather analytics with probability distributions for future predictions, 
                  complete historical weather archives, air quality indices, and trend analysis.
                </p>
              </div>
            </ScrollReveal>
            <ScrollReveal delay={480}>
              <div className="feature">
                <h3>🌍 Global Coverage</h3>
                <p>
                  Weather data for over 200,000 cities worldwide with hyper-local
                  precision down to street level.
                </p>
              </div>
            </ScrollReveal>
            <ScrollReveal delay={600}>
              <div className="feature">
                <h3>🔮 Probability-Based Forecasts</h3>
                <p>
                  Advanced statistical models deliver multi-day future predictions with
                  confidence scores and probability metrics, plus access to historical weather patterns.
                </p>
              </div>
            </ScrollReveal>
          </div>
        </div>
      </section>

      {/* Chapter 05: CLIMATE DATA - Why Choose Us Section */}
      <section className="why-choose-us">
        <div className="section-container">
          <ScrollReveal>
            <div className="chapter-badge">04 — CLIMATE DATA</div>
            <h2>Why Choose Astrokites</h2>
            <p className="section-subtitle">
              Powered by advanced statistical models and real-world data
            </p>
          </ScrollReveal>
          
          <div className="stats-grid">
            <ScrollReveal delay={100}>
              <div className="stat-card">
                <div className="stat-icon">🌍</div>
                <div className="stat-number">200K+</div>
                <div className="stat-label">Global Locations</div>
                <div className="stat-description">
                  Hyper-local weather data for cities worldwide
                </div>
              </div>
            </ScrollReveal>
            <ScrollReveal delay={250}>
              <div className="stat-card">
                <div className="stat-icon">📈</div>
                <div className="stat-number">30+ Years</div>
                <div className="stat-label">Historical Data</div>
                <div className="stat-description">
                  Comprehensive weather archives for trend analysis
                </div>
              </div>
            </ScrollReveal>
          </div>

          <ScrollReveal delay={350}>
            <div className="data-sources">
              <h3>Trusted Data Sources</h3>
              <div className="sources-list">
                <div className="source-item">🛰️ NASA POWER API</div>
                <div className="source-item">🌐 OpenStreetMap</div>
                <div className="source-item">📡 Satellite Imagery</div>
                <div className="source-item">🔬 Statistical Models</div>
              </div>
            </div>
          </ScrollReveal>
        </div>
      </section>

      {/* Chapter 06: EXPLORE - Newsletter Section */}
      <section className="newsletter">
        <div className="section-container">
          <ScrollReveal>
            <div className="chapter-badge">05 — EXPLORE</div>
            <div className="newsletter-content">
              <h2>Stay Weather-Wise</h2>
              <p>Get weekly weather insights and storm alerts delivered to your inbox.</p>
              <form className="newsletter-form">
                <input 
                  type="email" 
                  placeholder="Enter your email address" 
                  className="newsletter-input"
                />
                <button type="submit" className="newsletter-button">
                  Subscribe
                </button>
              </form>
              <div className="newsletter-benefits">
                <span>✓ Weekly forecasts</span>
                <span>✓ Storm alerts</span>
                <span>✓ Climate insights</span>
              </div>
            </div>
          </ScrollReveal>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <p>© 2025 Astrokites. All Rights Reserved.</p>
          <div className="footer-status">
            <span className="status-dot-pulse"></span>
            <span>SYSTEM OPERATIONAL · NASA POWER V2.0</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Home;
