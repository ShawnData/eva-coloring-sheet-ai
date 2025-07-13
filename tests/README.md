# Tests

This directory contains all tests for the Eva Coloring Sheet AI project.

## Test Structure

- `test_integration.py` - Integration tests for the complete workflow
- `test_conversation_summarizer.py` - Unit tests for the conversation summarizer agent
- `test_core_functionality.py` - Core functionality tests
- `test_llm_conversation.py` - LLM conversation capability tests
- `test_voice.py` - Voice processing component tests

## Running Tests

### Run all tests
```bash
python run_tests.py
```

### Run specific test file
```bash
python run_tests.py test_integration.py
```

### Run with pytest directly
```bash
pytest tests/ -v
```

### Run with coverage
```bash
pytest tests/ --cov=src --cov-report=html
```

## Test Configuration

Tests are configured in `pytest.ini` and `pyproject.toml`. The configuration includes:

- Test discovery in the `tests/` directory
- Coverage reporting with HTML output
- Python path configuration
- Warning filters

## Environment Setup

Tests require the following environment variables:
- `OPENAI_API_KEY` - For tests that interact with OpenAI APIs

If `OPENAI_API_KEY` is not set, some tests will be skipped automatically.

## Test Categories

### Unit Tests
- Test individual components in isolation
- Mock external dependencies
- Fast execution

### Integration Tests
- Test complete workflows
- May require external services
- Slower execution

### Functional Tests
- Test end-to-end functionality
- May require full application setup
- Longest execution time

## Adding New Tests

1. Create a new test file in the `tests/` directory
2. Follow the naming convention: `test_*.py`
3. Use pytest fixtures for setup and teardown
4. Include proper docstrings and comments
5. Add the test file to this README

## Test Best Practices

- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies when appropriate
- Keep tests independent and isolated
- Use setup and teardown methods for common operations
- Include assertions for expected behavior 