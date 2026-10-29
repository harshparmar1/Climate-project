import React, { createContext, useContext, useState, useCallback } from 'react';

const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [pageContext, setPageContext] = useState({
    currentPage: 'home',
    selectedLocation: null,
    selectedMetric: 'T2M',
    dateRange: null
  });

  const toggleChat = useCallback(() => setIsOpen(prev => !prev), []);
  const openChat = useCallback(() => setIsOpen(true), []);
  const closeChat = useCallback(() => setIsOpen(false), []);

  const updateLocationContext = useCallback((locationObj) => {
    setPageContext(prev => {
      if (prev.selectedLocation === locationObj) return prev;
      return { ...prev, selectedLocation: locationObj };
    });
  }, []);

  const updateMetricContext = useCallback((metricName) => {
    setPageContext(prev => {
      if (prev.selectedMetric === metricName) return prev;
      return { ...prev, selectedMetric: metricName };
    });
  }, []);

  const updateCurrentPage = useCallback((pageName) => {
    setPageContext(prev => {
      if (prev.currentPage === pageName) return prev;
      return { ...prev, currentPage: pageName };
    });
  }, []);

  return (
    <ChatContext.Provider
      value={{
        isOpen,
        toggleChat,
        openChat,
        closeChat,
        pageContext,
        setPageContext,
        updateLocationContext,
        updateMetricContext,
        updateCurrentPage
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};

export const useChatContext = () => {
  const context = useContext(ChatContext);
  if (!context) {
    console.warn('useChatContext was called outside of ChatProvider');
    return {
      isOpen: false,
      toggleChat: () => {},
      openChat: () => {},
      closeChat: () => {},
      pageContext: { currentPage: 'home', selectedLocation: null, selectedMetric: 'T2M', dateRange: null },
      setPageContext: () => {},
      updateLocationContext: () => {},
      updateMetricContext: () => {},
      updateCurrentPage: () => {}
    };
  }
  return context;
};
