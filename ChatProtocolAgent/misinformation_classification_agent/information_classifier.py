from uagents import Agent, Context, Model
import os
from crewai import Agent as CrewAIAgent, Task, Crew, Process
from crewai_tools import SerperDevTool

class InformationRequestModel(Model):
    information: str
 
class AnalysisReportModel(Model):
    analysis: str

os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"
os.environ["SERPER_API_KEY"] = "YOUR_SERPER_API_KEY"

class SeniorInformationAnalyst:
    def __init__(self):
        """
        Initializes the Senior Information Analyst agent with a search tool.
        """
        self.search_tool = SerperDevTool()
 
        self.analyst = CrewAIAgent(
            role="Senior Information Analyst",
            goal="Analyze given information and determine if it is fake or real.",
            backstory="""You are an expert in identifying misinformation.
            Your job is to verify the authenticity of claims using available online sources.""",
            verbose=True,
            allow_delegation=False,
            tools=[self.search_tool],
        )
 
    def create_task(self, information: str) -> Task:
        """
        Creates a task to analyze the authenticity of the given information.
 
        Parameters:
        - information: str, the information to be analyzed.
 
        Returns:
        - Task: The created task with the specified description and expected output.
        """
        task_description = (
            f"Analyze the following information and determine if it is real or fake: '{information}'."
            f"Use credible sources to validate its authenticity."
        )
 
        return Task(
            description=task_description,
            expected_output="Detailed analysis report indicating whether the information is real or fake.",
            agent=self.analyst,
        )
 

async def run_process(information: str):
    """
    Runs the process for the created task and retrieves the result.

    Parameters:
    - information: str, the information to be analyzed.

    Returns:
    - result: The output from the CrewAI process after executing the task.
    """
    seniorInformationAnalyst = SeniorInformationAnalyst()
    task = seniorInformationAnalyst.create_task(information)
    crew = Crew(
        agents=[seniorInformationAnalyst.analyst],
        tasks=[task],
        verbose=True,
        process=Process.sequential,
    )
    result = crew.kickoff()
    return result
 