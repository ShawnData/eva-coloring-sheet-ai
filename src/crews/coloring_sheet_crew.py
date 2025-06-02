from crewai.project import CrewBase, agent, crew, task
from crewai.agent import BaseAgent
from crewai import Task, Agent, Crew, Process
from typing import List

@CrewBase
class ColoringSheetCrew:
    """A crew that designs a coloring sheet prompt and generates a coloring sheet"""
    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def voice_assistant(self) -> Agent:
        return Agent(
            config = self.agents_config['voice_assistant'],
            verbose=True,
            allow_delegation=False
        )
    
    @task
    def process_voice_input_task(self) -> Task:
        return Task(
            config = self.tasks_config['process_voice_input_task']
        )

    @crew
    def crew(self) -> Crew:
        """Creates and returns a Crew instance with configured agents and tasks."""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            memory=True,  
            verbose=True,
        )