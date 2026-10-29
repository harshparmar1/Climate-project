import React, { useState } from 'react';
import { Sparkles } from 'lucide-react';
import { useChatContext } from '../../context/ChatContext';
import { postApiChat } from '../../api/axios';
import ChatWindow from './ChatWindow';
import './chatbot.css';

export default function Chatbot() {
  const { isOpen, toggleChat, closeChat, pageContext } = useChatContext();
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (userText) => {
    const userMsg = { role: 'user', content: userText };
    const updatedMessages = [...messages, userMsg];
    setMessages(updatedMessages);
    setIsLoading(true);

    try {
      const historyItems = updatedMessages.map(m => ({ role: m.role, content: m.content }));
      
      const res = await postApiChat({
        message: userText,
        history: historyItems,
        context: pageContext
      });

      if (res.ok && res.data) {
        const aiMsg = {
          role: 'assistant',
          content: res.data.answer,
          data: res.data.data,
          source: res.data.source
        };
        setMessages(prev => [...prev, aiMsg]);
      } else {
        setMessages(prev => [
          ...prev,
          {
            role: 'assistant',
            content: 'Unable to retrieve weather information right now. Please check your connection and try again.',
            source: 'AstroKites System'
          }
        ]);
      }
    } catch (err) {
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: 'Unable to retrieve weather information right now. Please try again.',
          source: 'AstroKites System'
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <button
        className="astrokites-chatbot-trigger"
        onClick={toggleChat}
        aria-label="Open AstroKites AI Assistant"
        aria-expanded={isOpen}
      >
        <span className="chatbot-pulse-ring" />
        <Sparkles className="chatbot-trigger-icon" size={22} color="#22d3ee" />
        <span className="chatbot-label">AI WEATHER</span>
        <span className="chatbot-trigger-badge" />
      </button>

      {isOpen && (
        <ChatWindow
          messages={messages}
          isLoading={isLoading}
          onSendMessage={handleSendMessage}
          onClose={closeChat}
          onMinimize={toggleChat}
        />
      )}
    </>
  );

}
