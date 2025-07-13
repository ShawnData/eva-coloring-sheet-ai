import React, { useState, useRef } from 'react';
import styled from 'styled-components';
import VoiceRecorder from './components/VoiceRecorder';
import ChatHistory from './components/ChatHistory';
import ImageDisplay from './components/ImageDisplay';

const AppContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Comic Sans MS', cursive, sans-serif;
  padding: 20px;
`;

const Header = styled.div`
  text-align: center;
  margin-bottom: 30px;
`;

const Title = styled.h1`
  color: white;
  font-size: 3rem;
  margin: 0;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
`;

const Subtitle = styled.p`
  color: #f0f0f0;
  font-size: 1.2rem;
  margin: 10px 0 0 0;
`;

const MainContent = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const LeftPanel = styled.div`
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

function App() {
  const [chatHistory, setChatHistory] = useState([]);
  const [currentImage, setCurrentImage] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleVoiceInput = async (audioBlob) => {
    setIsProcessing(true);
    
    try {
      // Create form data for the audio file
      const formData = new FormData();
      formData.append('audio', audioBlob, 'recording.wav');
      
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

  return (
    <AppContainer>
      <Header>
        <Title>🎨 Eva's Coloring Sheet AI 🎨</Title>
        <Subtitle>Tell me what you want to color, and I'll create it for you!</Subtitle>
      </Header>
      
      <MainContent>
        <LeftPanel>
          <VoiceRecorder 
            onVoiceInput={handleVoiceInput}
            isProcessing={isProcessing}
          />
          <ChatHistory messages={chatHistory} />
        </LeftPanel>
        
        <ImageDisplay imageUrl={currentImage} />
      </MainContent>
    </AppContainer>
  );
}

export default App; 