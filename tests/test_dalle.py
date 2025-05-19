from eva_coloring_sheet_agent.crew import EvaColoringSheetAgent

def main():
    # Create an instance of the agent
    agent = EvaColoringSheetAgent()
    
    # Run the crew
    result = agent.crew().kickoff()
    
    print("Crew execution completed!")
    print("Result:", result)

if __name__ == "__main__":
    main() 