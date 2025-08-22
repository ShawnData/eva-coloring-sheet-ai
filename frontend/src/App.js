import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import VoiceRecorder from './components/VoiceRecorder';
import ChatHistory from './components/ChatHistory';
import ImageDisplay from './components/ImageDisplay';

const AppContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  color: white;
`;

const Header = styled.header`
  text-align: center;
  margin-bottom: 30px;
`;

const Title = styled.h1`
  font-size: 2.5rem;
  margin: 0;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
`;

const Subtitle = styled.p`
  font-size: 1.2rem;
  margin: 10px 0 0 0;
  opacity: 0.9;
`;

const MainContent = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  align-items: start;
`;

const LeftPanel = styled.div`
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const RightPanel = styled.div`
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const ConversationStatus = styled.div`
  background: rgba(255, 255, 255, 0.1);
  padding: 15px;
  border-radius: 10px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
`;

const StatusText = styled.p`
  margin: 0;
  font-size: 1rem;
  font-weight: 500;
`;

const Controls = styled.div`
  display: flex;
  gap: 10px;
  margin-top: 10px;
`;

const Button = styled.button`
  background: ${props => props.variant === 'secondary' ? 'rgba(255, 255, 255, 0.2)' : '#4CAF50'};
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  
  &:hover {
    background: ${props => props.variant === 'secondary' ? 'rgba(255, 255, 255, 0.3)' : '#45a049'};
    transform: translateY(-2px);
  }
  
  &:disabled {
    background: #ccc;
    cursor: not-allowed;
    transform: none;
  }
`;

const ProcessingIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
`;

const Spinner = styled.div`
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

function App() {
  const [chatHistory, setChatHistory] = useState([]);
  const [currentImage, setCurrentImage] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [conversationState, setConversationState] = useState(null);

  // Initialize session on component mount
  useEffect(() => {
    if (!sessionId) {
      setSessionId(crypto.randomUUID());
    }
  }, [sessionId]);

  const getConversationStatus = () => {
    if (!conversationState) return "Starting conversation...";
    
    switch (conversationState.current_phase) {
      case "collecting":
        return "Collecting your requirements...";
      case "confirming":
        return "Confirming your choices...";
      case "generating":
        return "Creating your coloring sheet...";
      case "complete":
        return "Conversation complete!";
      default:
        return "Ready to chat!";
    }
  };

  const handleVoiceInput = async (audioBlob) => {
    setIsProcessing(true);
    
    try {
      // Create form data for the audio file
      const formData = new FormData();
      formData.append('audio', audioBlob, 'recording.wav');
      if (sessionId) {
        formData.append('session_id', sessionId);
      }
      
      // Send to backend
      const response = await fetch('/api/process-voice', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error('Failed to process voice input');
      }
      
      const result = await response.json();
      
      // Add to chat history
      setChatHistory(prev => [
        ...prev,
        { role: 'user', content: result.transcription },
        { role: 'assistant', content: result.message }
      ]);
      
      // Update conversation state
      if (result.conversation_state) {
        setConversationState(result.conversation_state);
      }
      
      // Update image if provided
      if (result.image_url) {
        setCurrentImage(result.image_url);
      }
      
      // Play TTS audio if available
      if (result.tts_url) {
        const audio = new Audio(result.tts_url);
        audio.play().catch(error => {
          console.warn('Could not play TTS audio:', error);
        });
      }
      
    } catch (error) {
      console.error('Error processing voice input:', error);
      setChatHistory(prev => [
        ...prev,
        { role: 'system', content: 'Sorry, I had trouble understanding that. Please try again!' }
      ]);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleResetConversation = async () => {
    if (!sessionId) return;
    
    try {
      const response = await fetch('/api/reset-conversation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ session_id: sessionId }),
      });
      
      if (response.ok) {
        const result = await response.json();
        setChatHistory([]);
        setCurrentImage(null);
        setConversationState(result.conversation_state);
      }
    } catch (error) {
      console.error('Error resetting conversation:', error);
    }
  };

  const handleNewConversation = () => {
    const newSessionId = crypto.randomUUID();
    setSessionId(newSessionId);
    setChatHistory([]);
    setCurrentImage(null);
    setConversationState(null);
  };

  return (
    <AppContainer>
      <Header>
        <Title>🎨 Eva's Coloring Sheet AI</Title>
        <Subtitle>Create beautiful coloring sheets through natural conversation!</Subtitle>
      </Header>
      
      <MainContent>
        <LeftPanel>
          <ConversationStatus>
            <StatusText>Status: {getConversationStatus()}</StatusText>
            <Controls>
              <Button onClick={handleResetConversation} variant="secondary">
                Reset Conversation
              </Button>
              <Button onClick={handleNewConversation} variant="secondary">
                New Conversation
              </Button>
            </Controls>
          </ConversationStatus>
          
          {isProcessing && (
            <ProcessingIndicator>
              <Spinner />
              <span>Processing your voice input...</span>
            </ProcessingIndicator>
          )}
          
          <VoiceRecorder onVoiceInput={handleVoiceInput} disabled={isProcessing} />
          
          <ChatHistory messages={chatHistory} />
        </LeftPanel>
        
        <RightPanel>
          <ImageDisplay imageUrl={currentImage} />
        </RightPanel>
      </MainContent>
    </AppContainer>
  );
}

export default App; 