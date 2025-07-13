import React from 'react';
import styled from 'styled-components';

const ImageContainer = styled.div`
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.2);
  padding: 20px;
  height: 500px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`;

const ImageTitle = styled.h3`
  color: white;
  font-size: 24px;
  margin: 0 0 20px 0;
  text-align: center;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
`;

const GeneratedImage = styled.img`
  max-width: 100%;
  max-height: 400px;
  border-radius: 15px;
  box-shadow: 0 8px 16px rgba(0,0,0,0.3);
  object-fit: contain;
`;

const EmptyState = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: rgba(255, 255, 255, 0.7);
  text-align: center;
  
  .icon {
    font-size: 80px;
    margin-bottom: 20px;
  }
  
  h3 {
    margin: 0 0 10px 0;
    font-size: 24px;
  }
  
  p {
    margin: 0;
    font-size: 16px;
    line-height: 1.5;
  }
`;

const ImageDisplay = ({ imageUrl }) => {
  if (!imageUrl) {
    return (
      <ImageContainer>
        <EmptyState>
          <div className="icon">🎨</div>
          <h3>Your Coloring Sheet</h3>
          <p>Your beautiful coloring sheet will appear here after you tell me what you'd like to create!</p>
        </EmptyState>
      </ImageContainer>
    );
  }

  return (
    <ImageContainer>
      <ImageTitle>🎨 Your Coloring Sheet</ImageTitle>
      <GeneratedImage 
        src={imageUrl} 
        alt="Generated coloring sheet"
        onError={(e) => {
          console.error('Failed to load image:', imageUrl);
          e.target.style.display = 'none';
        }}
      />
    </ImageContainer>
  );
};

export default ImageDisplay; 