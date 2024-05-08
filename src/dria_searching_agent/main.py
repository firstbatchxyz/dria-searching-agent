import json
import os
import shutil
from textwrap import dedent

from crewai import Agent, Crew, Task
from crewai.process import Process
from langchain_anthropic import ChatAnthropic

from src.dria_searching_agent.tasks import TaskPrompts

from src.dria_searching_agent.tools.fin_tools import FinancialData
from src.dria_searching_agent.tools.search_tools import SerperSearchTools
from src.dria_searching_agent.tools.vision_tools import VisionTools
from src.dria_searching_agent.tools.browser_tools import BrowserTools
from dotenv import load_dotenv


class ResearchCrew:
    def __init__(self, query):
        self.agents_config = json.loads(open("src/dria_searching_agent/config/agents.json", "r").read())
        self.agents = {}
        self.picker = None
        self.evaluator = None
        self.query = query
        self.scraped_links = []
        self.__create_agents()

    def run(self):
        research = self.__do_research()
        feedback = self.__evaluate(research)
        i = 0
        if feedback[-1] == ".":
            feedback = feedback[:-1]

        while i < 1 and feedback.lower().strip() != "satisfactory":
            research = self.__do_research_w_feedback(feedback)
            feedback = self.__evaluate(research)
        return research

    def run_w_manager(self):
        research = self.__do_research_w_manager()
        return research

    def __do_research(self):

        agent = self.__pick_agent()
        initial_search = TaskPrompts().do_research(query=self.query, agent=agent, role=agent.role)
        crew = Crew(
            agents=list(self.agents.values()),
            tasks=[initial_search],
            verbose=True,
            memory=True,
            llm=ChatAnthropic(model=os.environ["CLAUDE_OPUS"], api_key=os.environ['ANTHROPIC_KEY'])
        )
        research = crew.kickoff()
        return research

    def __do_research_w_manager(self):

        initial_search = TaskPrompts().do_research_w_manager(query=self.query)
        crew = Crew(
            agents=list(self.agents.values()),
            tasks=[initial_search],
            verbose=True,
            memory=True,
            process=Process.hierarchical,
            manager_llm=ChatAnthropic(model=os.environ["CLAUDE_OPUS"], api_key=os.environ['ANTHROPIC_KEY'])
        )
        research = crew.kickoff()
        return research

    def __do_research_w_feedback(self,feedback):

            feedback_search = TaskPrompts().do_research_w_feedback(query=self.query, feedback=feedback)
            crew = Crew(
                agents=list(self.agents.values()),
                tasks=[feedback_search],
                verbose=True,
                memory=True,
                process=Process.hierarchical,
                manager_llm=ChatAnthropic(model=os.environ["CLAUDE_OPUS"], api_key=os.environ['ANTHROPIC_KEY'])
            )
            research = crew.kickoff()
            return research

    def __pick_agent(self):

        task = TaskPrompts().pick_agent(
            query=self.query,
            agents="\n".join([agent + "\n" + self.agents[agent].backstory for agent in self.agents.keys()]),
            agent=self.picker)

        crew = Crew(
            agents=[self.picker],
            tasks=[task],
            verbose=True
        )
        agent = crew.kickoff()
        agent = self.agents[agent.lower().strip()]
        return agent

    def __evaluate(self, research):
        evaluate_task = TaskPrompts().evaluate_results(
                search_results=research,
                query=self.query,agent=self.evaluator)

        crew = Crew(
            agents=[self.evaluator],
            tasks=[evaluate_task],
            verbose=True
        )
        evaluation = crew.kickoff()
        return evaluation

    def __create_agents(self):

        for k,v in self.agents_config.items():
            agent = Agent(
                **v,
                verbose=True,
                llm = ChatAnthropic(model=os.environ["CLAUDE_OPUS"], api_key=os.environ['ANTHROPIC_KEY']),
                tools=[
                    SerperSearchTools.search_internet,
                    SerperSearchTools.search_images,
                    BrowserTools.scrape_website,
                    SerperSearchTools.get_context,
                    FinancialData.scrape,
                    VisionTools.vision,
                    VisionTools.read_pdf
                ]
            )
            self.agents[k.lower().strip()] = agent

        evaluator_config = {
            "role": "Answer Evaluation Specialist",
            "specialty": "Assessing the Quality and Relevance of Answers",
            "backstory": "Dr. Liam Hoffman is a renowned information quality expert with a background in data analysis and decision science. He has developed rigorous evaluation frameworks for assessing the quality, relevance, and completeness of information in various domains. His critical thinking skills and ability to objectively evaluate the strengths and weaknesses of answers make him a valuable asset in ensuring the highest standards of information quality.",
            "goal": "Utilize my expertise in information quality assessment and decision science to objectively evaluate the created report/answer and collected data against the given query. I will assess the relevance, comprehensiveness, accuracy, and reliability of the provided information, identifying any gaps or areas for improvement. By critically analyzing the answer and providing constructive feedback, I aim to ensure that the final output is of the highest quality and effectively addresses the query.",
            "allow_delegation": False
        }

        self.evaluator = Agent(
            **evaluator_config,
            verbose=True)

        picker_config = {
            "role": "Agent Selection Specialist",
            "specialty": "Matching Queries with Agents",
            "backstory": "Dr. Nadia Patel is a highly skilled information retrieval expert with a background in cognitive science and decision-making. She has developed advanced algorithms for matching user queries with the most suitable agents based on their expertise, background, and problem-solving approaches. Her keen understanding of agent capabilities and her ability to analyze complex queries make her an invaluable asset in optimizing the research process.",
            "goal": "Utilize my expertise in information retrieval and cognitive science to select the most appropriate agent for a given query, considering factors such as the agent's specialty, role, background, and problem-solving style. By carefully analyzing the query and the available agents, I aim to optimize the research process and ensure that the most relevant and accurate information is obtained efficiently.",
            "allow_delegation": False
            }

        self.picker = Agent(
            **picker_config,
            verbose=True
        )

def main():
    load_dotenv()
    print("Welcome to Researcher!")
    query = input("# Write down a question:\n\n")
    crew = ResearchCrew(query)
    result = crew.run()
    print(result)
    print("==========================================")

def main_w_manager():
    load_dotenv()
    print("Welcome to Researcher!")
    query = input("# Write down a question:\n\n")
    crew = ResearchCrew(query)
    result = crew.run_w_manager()
    print(result)
    print("==========================================")