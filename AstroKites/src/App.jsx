import { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import Navbar from './component/navbar';
import Home from './pages/homePage';
import Forecast from './pages/forecast';
import Maps from './pages/maps';
import { ChatProvider, useChatContext } from './context/ChatContext';
import Chatbot from './components/chatbot/Chatbot';
import './App.css';

import Signup from './pages/signup';

const NotFound = () => (
  <div style={{ padding: 40, color: "#fff", textAlign: "center" }}>
    <h2>Page not found</h2>
    <p>Return to <a href="/">home</a>.</p>
  </div>
);

function ScrollProgressBar() {
  const [scrollProgress, setScrollProgress] = useState(0);
  const location = useLocation();
  const { updateCurrentPage } = useChatContext();

  useEffect(() => {
    const handleScroll = () => {
      const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
      if (totalHeight > 0) {
        const currentProgress = (window.scrollY / totalHeight) * 100;
        setScrollProgress(currentProgress);
      }
    };

    window.addEventListener('scroll', handleScroll);
    handleScroll();
    return () => window.removeEventListener('scroll', handleScroll);
  }, [location]);

  useEffect(() => {
    let pageName = 'home';
    if (location.pathname.includes('forecast')) pageName = 'forecast';
    else if (location.pathname.includes('maps')) pageName = 'maps';
    if (updateCurrentPage) {
      updateCurrentPage(pageName);
    }
  }, [location, updateCurrentPage]);

  return (
    <div className="scroll-progress-container">
      <div 
        className="scroll-progress-bar" 
        style={{ width: `${scrollProgress}%` }}
        aria-hidden="true"
      />
    </div>
  );
}

function App() {
  return (
    <ChatProvider>
      <Router>
        <ScrollProgressBar />
        <Navbar />
        <main className="app-content-wrapper">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/home" element={<Home />} />
            <Route path="/forecast" element={<Forecast />} />
            <Route path="/maps" element={<Maps />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
        <Chatbot />
      </Router>
    </ChatProvider>
  );
}

export default App;

