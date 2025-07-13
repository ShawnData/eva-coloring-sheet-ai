import React, { useState, useRef } from 'react';
import styled, { keyframes } from 'styled-components';

const pulse = keyframes`
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
`;

const RecorderContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  padding: 30px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.2);
`;

const RecordButton = styled.button`
  background: ${props => props.isRecording 
    ? 'linear-gradient(45deg, #FF4757, #FF3838)' 
    : 'linear-gradient(45deg, #FF6B6B, #4ECDC4)'
  };
  border: none;
  border-radius: 50px;
  padding: 25px 50px;
  font-size: 28px;
  font-weight: bold;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 8px 16px rgba(0,0,0,0.2);
  font-family: 'Comic Sans MS', cursive, sans-serif;
  animation: ${props => props.isRecording ? pulse : 'none'} 1.5s infinite;
  
  &:hover {
    transform: scale(1.05);
    box-shadow: 0 12px 24px rgba(0,0,0,0.3);
  }
  
  &:active {
    transform: scale(0.95);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
`;

const StatusText = styled.div`
  color: white;
  font-size: 18px;
  text-align: center;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
`;

const Instructions = styled.div`
  color: #f0f0f0;
  text-align: center;
  font-size: 16px;
  line-height: 1.5;
  
  p {
    margin: 5px 0;
  }
`;

const VoiceRecorder = ({ onVoiceInput, isProcessing }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [audioChunks, setAudioChunks] = useState([]);
  const streamRef = useRef(null);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;
      
      const recorder = new MediaRecorder(stream);
      const chunks = [];
      
      recorder.ondataavailable = (event) => {
        chunks.push(event.data);
      };
      
      recorder.onstop = () => {
        const audioBlob = new Blob(chunks, { type: 'audio/wav' });
        onVoiceInput(audioBlob);
        setAudioChunks([]);
      };
      
      recorder.start();
      setMediaRecorder(recorder);
      setAudioChunks(chunks);
      setIsRecording(true);
      
    } catch (error) {
      console.error('Error accessing microphone:', error);
      alert('Please allow microphone access to use voice recording.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorder && isRecording) {
      mediaRecorder.stop();
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
        streamRef.current = null;
      }
      setMediaRecorder(null);
      setIsRecording(false);
    }
  };

  const handleButtonClick = () => {
    if (isProcessing) return; // Don't allow recording while processing
    
    if (!isRecording) {
      startRecording();
    } else {
      stopRecording();
    }
  };

  const getButtonText = () => {
    if (isProcessing) return '⏳ Processing...';
    return isRecording ? '🎤 STOP' : '🎤 TALK';
  };

  const getStatusText = () => {
    if (isProcessing) return 'Processing your request...';
    return isRecording ? '🔴 Recording... Click to stop' : 'Click to start recording';
  };

  return (
    <RecorderContainer>
      <RecordButton
        onClick={handleButtonClick}
        isRecording={isRecording}
        disabled={isProcessing}
      >
        {getButtonText()}
      </RecordButton>
      
      <StatusText>{getStatusText()}</StatusText>
      
      <Instructions>
        <p>💡 Try saying things like:</p>
        <p>"I want a cat coloring sheet"</p>
        <p>"Draw me a dinosaur"</p>
        <p>"Make a flower picture"</p>
      </Instructions>
    </RecorderContainer>
  );
};

export default VoiceRecorder; 