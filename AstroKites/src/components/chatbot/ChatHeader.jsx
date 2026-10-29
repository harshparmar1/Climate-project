import React from 'react';
import { Bot, Minus, X, Sparkles } from 'lucide-react';

export default function ChatHeader({ onClose, onMinimize }) {
  return (
    <div className="chat-header">
      <div className="chat-header-info">
        <div className="chat-avatar-container">
          <Bot size={20} />
        </div>
        <div className="chat-title-group">
          <h3>
            AstroKites AI <Sparkles size={14} color="#22d3ee" />
          </h3>
          <div className="chat-subtitle">
            <span className="status-indicator">
              <span className="status-dot"></span>
              ASTROKITES DATA
            </span>
          </div>
        </div>
      </div>
      <div className="chat-header-actions">
        <button
          className="chat-action-btn"
          onClick={onMinimize}
          aria-label="Minimize chatbot"
        >
          <Minus size={18} />
        </button>
        <button
          className="chat-action-btn"
          onClick={onClose}
          aria-label="Close chatbot"
        >
          <X size={18} />
        </button>
      </div>
    </div>
  );
}
