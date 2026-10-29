import React, { useEffect, useRef } from 'react';
import ChatHeader from './ChatHeader';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import QuickPrompts from './QuickPrompts';
import { Bot } from 'lucide-react';

export default function ChatWindow({
  messages,
  isLoading,
  onSendMessage,
  onClose,
  onMinimize
}) {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  return (
    <div className="astrokites-chat-window" role="dialog" aria-label="AstroKites AI Assistant">
      <ChatHeader onClose={onClose} onMinimize={onMinimize} />

      <div className="chat-messages-container">
        {messages.length === 0 ? (
          <div className="chat-welcome-state">
            <div className="welcome-icon-glow">
              <Bot size={28} />
            </div>
            <h4>Hello! I'm AstroKites AI</h4>
            <p>
              Your intelligent climate & weather assistant. I can help you explore temperature, precipitation, wind, humidity, forecasts and climate trends.
            </p>
            <QuickPrompts onSelectPrompt={onSendMessage} />
          </div>
        ) : (
          messages.map((msg, idx) => (
            <ChatMessage key={idx} message={msg} />
          ))
        )}

        {isLoading && (
          <div className="typing-indicator-box">
            <div className="dots-wrapper">
              <span className="dot"></span>
              <span className="dot"></span>
              <span className="dot"></span>
            </div>
            <span>AstroKites AI is analyzing climate data...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <ChatInput onSendMessage={onSendMessage} disabled={isLoading} />
    </div>
  );
}
