import React from 'react';
import './ChatButton.css';

const ChatButton = ({ onClick, isOpen }) => {
  return (
    <button 
      className={`chat-button ${isOpen ? 'active' : ''}`}
      onClick={onClick}
      title={isOpen ? "Close chat" : "Open chat"}
    >
      {isOpen ? (
        <span className="chat-icon">✕</span>
      ) : (
        <span className="chat-icon">💬</span>
      )}
      <div className="chat-pulse"></div>
    </button>
  );
};

export default ChatButton;
