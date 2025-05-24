import pytest
import os
from unittest.mock import Mock, patch

@pytest.fixture(autouse=True)
def mock_env_vars():
    """Automatically mock environment variables for all tests"""
    with patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'}):
        yield

@pytest.fixture
def mock_crewai_agent():
    """Fixture to mock CrewAI Agent"""
    with patch('crewai.Agent') as mock_agent:
        mock_instance = Mock()
        mock_agent.return_value = mock_instance
        yield mock_instance 