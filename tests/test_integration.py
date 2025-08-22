import os
import pytest
import json
from dotenv import load_dotenv
from src.crews.coloring_sheet_crew import create_coloring_sheet_crew

class TestCrewAIIntegration:
    def setup_method(self):
        load_dotenv()
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY environment variable is not set")
        self.crew = create_coloring_sheet_crew()

    def extract_final_output(self, crew_output):
        """Extract the final output from the crew result"""
        # The crew output has the result in the raw attribute as a JSON string
        if hasattr(crew_output, 'raw') and crew_output.raw:
            try:
                # Remove the ```json and ``` markers if present
                raw_str = crew_output.raw.strip()
                if raw_str.startswith('```json'):
                    raw_str = raw_str[7:]  # Remove ```json
                if raw_str.endswith('```'):
                    raw_str = raw_str[:-3]  # Remove ```
                
                return json.loads(raw_str.strip())
            except json.JSONDecodeError:
                return {"message": crew_output.raw, "image_url": None, "error": "Failed to parse output"}
        
        # Fallback: try to_dict() method
        result = crew_output.to_dict()
        
        if isinstance(result, dict) and 'tasks_outputs' in result:
            task_outputs = result['tasks_outputs']
            if task_outputs and len(task_outputs) > 0:
                final_output = task_outputs[-1]  # Last task output
                if isinstance(final_output, str):
                    try:
                        return json.loads(final_output)
                    except json.JSONDecodeError:
                        return {"message": final_output, "image_url": None, "error": "Failed to parse output"}
                elif isinstance(final_output, dict):
                    return final_output
                else:
                    return {"message": str(final_output), "image_url": None, "error": None}
            else:
                return {"message": "No output generated", "image_url": None, "error": "No task output"}
        else:
            return result if isinstance(result, dict) else {"message": str(result), "image_url": None, "error": None}

    def test_full_crew_workflow_coloring_request(self):
        """Test full CrewAI workflow for a coloring sheet request"""
        test_input = "I want a cat coloring sheet"
        crew_output = self.crew.kickoff(inputs={"voice_input": test_input})
        result = self.extract_final_output(crew_output)
        
        assert isinstance(result, dict)
        assert "message" in result
        assert "image_url" in result
        assert "error" in result
        
        # Should have a message about the coloring sheet
        assert result["message"] is not None
        # Should have an image URL for a coloring request
        assert result["image_url"] is not None
        assert result["error"] is None

    def test_full_crew_workflow_non_coloring_request(self):
        """Test CrewAI workflow for a non-coloring request"""
        test_input = "Hello, how are you?"
        crew_output = self.crew.kickoff(inputs={"voice_input": test_input})
        result = self.extract_final_output(crew_output)
        
        assert isinstance(result, dict)
        assert "message" in result
        assert "image_url" in result
        assert "error" in result
        
        # Should have a friendly message
        assert result["message"] is not None
        # Should not return an image URL for non-coloring requests
        assert result["image_url"] is None

    def test_full_crew_workflow_inappropriate_content(self):
        """Test CrewAI workflow with inappropriate content"""
        test_input = "I want a scary monster"
        crew_output = self.crew.kickoff(inputs={"voice_input": test_input})
        result = self.extract_final_output(crew_output)
        
        assert isinstance(result, dict)
        assert "message" in result
        assert "image_url" in result
        assert "error" in result
        
        # Should provide a safe alternative in the message
        message_lower = result["message"].lower()
        assert "friendly" in message_lower or "cute" in message_lower or "happy" in message_lower

    def test_full_crew_workflow_empty_input(self):
        """Test CrewAI workflow with empty input"""
        test_input = ""
        crew_output = self.crew.kickoff(inputs={"voice_input": test_input})
        result = self.extract_final_output(crew_output)
        
        assert isinstance(result, dict)
        assert "message" in result
        # Should handle empty input gracefully
        assert result["message"] is not None

    def test_full_crew_workflow_error_handling(self):
        """Test error handling in the CrewAI workflow"""
        # Simulate error by passing a very long or invalid input
        test_input = "x" * 10000
        try:
            crew_output = self.crew.kickoff(inputs={"voice_input": test_input})
            result = self.extract_final_output(crew_output)
            assert isinstance(result, dict)
            assert "message" in result
            # Should handle long input gracefully
            assert result["message"] is not None
        except Exception as e:
            # If an exception is raised, it should be handled gracefully
            assert "error" in str(e).lower() or "failed" in str(e).lower() 