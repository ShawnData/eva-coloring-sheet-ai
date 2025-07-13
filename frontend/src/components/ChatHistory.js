import React from 'react';
import styled from 'styled-components';

const ChatContainer = styled.div`
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.2);
  padding: 20px;
  height: 400px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
`;

const Message = styled.div`
  padding: 15px;
  border-radius: 15px;
  max-width: 80%;
  word-wrap: break-word;
  font-size: 16px;
  line-height: 1.4;
  
  ${props => {
    switch (props.role) {
      case 'user':
        return `
          background: linear-gradient(45deg, #4ECDC4, #44A08D);
          color: white;
          align-self: flex-end;
          margin-left: auto;
        `;
      case 'assistant':
        return `
          background: linear-gradient(45deg, #FF6B6B, #FF8E53);
          color: white;
          align-self: flex-start;
          margin-right: auto;
        `;
      case 'system':
        return `
          background: rgba(255, 255, 255, 0.2);
          color: #FF4757;
          align-self: center;
          text-align: center;
          font-weight: bold;
        `;
      default:
        return `
          background: rgba(255, 255, 255, 0.1);
          color: white;
        `;
    }
  }}
`;

const EmptyState = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: rgba(255, 255, 255, 0.7);
  text-align: center;
  
  h3 {
    margin: 0 0 10px 0;
    font-size: 20px;
  }
  
  p {
    margin: 0;
    font-size: 16px;
  }
`;

const ChatHistory = ({ messages }) => {
  if (messages.length === 0) {
    return (
      <ChatContainer>
        <EmptyState>
          <h3>🎨 Start Your Adventure!</h3>
          <p>Click the TALK button and tell me what you'd like to color!</p>
        </EmptyState>
      </ChatContainer>
    );
  }

  return (
    <ChatContainer>
      {messages.map((message, index) => (
        <Message key={index} role={message.role}>
          {message.content}
        </Message>
      ))}
    </ChatContainer>
  );
};

export default ChatHistory; 