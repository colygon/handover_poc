"""
SWAST Healthcare Analytics Crew
Main crew configuration and orchestration
"""
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI
from .tools.handover_tools import HandoverDataTool, HandoverMetricsTool, HandoverForecastTool


@CrewBase
class SWASTCrew:
    """SWAST Healthcare Analytics Crew for analyzing hospital handover delays"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        """Initialize the crew with custom LLM configuration"""
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7
        )

    @agent
    def handover_data_analyst(self) -> Agent:
        """Create the Handover Data Analyst agent"""
        return Agent(
            config=self.agents_config['handover_data_analyst'],
            tools=[HandoverDataTool(), HandoverMetricsTool()],
            llm=self.llm,
            verbose=True
        )

    @agent
    def performance_monitor(self) -> Agent:
        """Create the Performance Monitor agent"""
        return Agent(
            config=self.agents_config['performance_monitor'],
            tools=[HandoverMetricsTool(), HandoverDataTool()],
            llm=self.llm,
            verbose=True
        )

    @agent
    def predictive_analyst(self) -> Agent:
        """Create the Predictive Analytics Specialist agent"""
        return Agent(
            config=self.agents_config['predictive_analyst'],
            tools=[HandoverForecastTool(), HandoverDataTool(), HandoverMetricsTool()],
            llm=self.llm,
            verbose=True
        )

    @task
    def analyze_handover_delays(self) -> Task:
        """Create task for analyzing handover delays"""
        return Task(
            config=self.tasks_config['analyze_handover_delays'],
            agent=self.handover_data_analyst()
        )

    @task
    def monitor_performance(self) -> Task:
        """Create task for monitoring performance"""
        return Task(
            config=self.tasks_config['monitor_performance'],
            agent=self.performance_monitor()
        )

    @task
    def predict_handover_demand(self) -> Task:
        """Create task for predicting demand"""
        return Task(
            config=self.tasks_config['predict_handover_demand'],
            agent=self.predictive_analyst()
        )

    @crew
    def crew(self) -> Crew:
        """Create the SWAST Healthcare Analytics crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
