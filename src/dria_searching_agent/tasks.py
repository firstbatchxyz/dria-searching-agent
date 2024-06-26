from textwrap import dedent
from crewai import Task


class TaskPrompts:

    def do_research(self, query, role, agent):
        return Task(description=dedent(f"""
      Conduct a comprehensive search on the given query using your unique expertise and available tools.
      Utilize your specialty background and {role} perspective to gather relevant information.

      Analyze the query to determine the most appropriate search methods. Consider the following:
      - If the query explicitly requires visual information or real-world examples, prioritize image-based searches.
      - If the query demands scientific or academic insights, focus on scholarly articles and research papers.
      - If the query is related to current events or popular topics, explore news sources and reputable websites.
      - Use direct Google searches to find additional relevant information and fill in any gaps.

      Your search should be guided by the following goal:
      Find a detailed answer that covers multiple aspects of the query and is based on real, reliable information. The answer should be comprehensive, well-rounded, and grounded in scientific evidence or expert knowledge.

      Aim to collect the following types of information:
      - Real-world data and examples that support the answer and make it more concrete.
      - Expert opinions, insights, and know-how that provide deeper understanding and practical applications.
      - Scientific arguments, theories, and evidence that lend credibility to the answer.
      - Relevant case studies, anecdotes, or analogies that illustrate key points and make the answer more relatable.

      {self.__tip_section()} 
      Remember, the ultimate goal is to provide a detailed, informative answer that addresses the query from multiple angles and is supported by reliable, real-world information.

      Query:
      ----------
      {query}

    """), agent=agent,
                    expected_output=dedent(f"""
        The expected output should be a comprehensive and well-researched answer to the given query. The answer should:

        1. Address the query from multiple angles, considering different aspects and perspectives relevant to the topic.
        2. Provide real-world data, examples, and case studies that support the answer and make it more concrete and relatable.
        3. Include expert opinions, insights, and practical know-how that deepen the understanding of the topic and its applications.
        4. Present scientific arguments, theories, and evidence that lend credibility to the answer and demonstrate its grounding in reliable sources.
        5. Offer relevant analogies, anecdotes, or illustrations that clarify key points and make the answer more engaging and accessible.

        The answer should be structured in a logical and coherent manner, with clear transitions between different sections or ideas. It should be written in a clear, concise, and professional tone, avoiding unnecessary jargon or technical language.

        The length of the answer may vary depending on the complexity of the query and the amount of relevant information available. However, it should aim to be comprehensive enough to provide a satisfactory and informative response to the query.

        Overall, the expected output is a well-researched, detailed, and reliable answer that demonstrates a deep understanding of the topic and provides valuable insights and information to the reader.

        Note: Image-based searches should only be used if the query explicitly requires visual information or real-world examples. For queries that do not specifically demand visual content, focus on other search methods such as scholarly articles, news sources, and direct Google searches to gather relevant information.
        """))

    def do_research_w_manager(self, query):
        return Task(description=dedent(f"""
      Conduct a comprehensive search on the given query using your unique expertise and available tools.
      Utilize your specialty background and perspective to gather relevant information.

      Analyze the query to determine the most appropriate search methods. Consider the following:
      - If the query explicitly requires visual information or real-world examples, prioritize image-based searches.
      - If the query demands scientific or academic insights, focus on scholarly articles and research papers.
      - If the query is related to current events or popular topics, explore news sources and reputable websites.
      - Use direct Google searches to find additional relevant information and fill in any gaps.

      Your search should be guided by the following goal:
      Find a detailed answer that covers multiple aspects of the query and is based on real, reliable information. The answer should be comprehensive, well-rounded, and grounded in scientific evidence or expert knowledge.

      Aim to collect the following types of information:
      - Real-world data and examples that support the answer and make it more concrete.
      - Expert opinions, insights, and know-how that provide deeper understanding and practical applications.
      - Scientific arguments, theories, and evidence that lend credibility to the answer.
      - Relevant case studies, anecdotes, or analogies that illustrate key points and make the answer more relatable.

      {self.__tip_section()} 
      Remember, the ultimate goal is to provide a detailed, informative answer that addresses the query from multiple angles and is supported by reliable, real-world information.

      Query:
      ----------
      {query}

    """),
        expected_output=dedent(f"""
        The expected output should be a comprehensive and well-researched answer to the given query. The answer should:

        1. Address the query from multiple angles, considering different aspects and perspectives relevant to the topic.
        2. Provide real-world data, examples, and case studies that support the answer and make it more concrete and relatable.
        3. Include expert opinions, insights, and practical know-how that deepen the understanding of the topic and its applications.
        4. Present scientific arguments, theories, and evidence that lend credibility to the answer and demonstrate its grounding in reliable sources.
        5. Offer relevant analogies, anecdotes, or illustrations that clarify key points and make the answer more engaging and accessible.

        The answer should be structured in a logical and coherent manner, with clear transitions between different sections or ideas. It should be written in a clear, concise, and professional tone, avoiding unnecessary jargon or technical language.

        The length of the answer may vary depending on the complexity of the query and the amount of relevant information available. However, it should aim to be comprehensive enough to provide a satisfactory and informative response to the query.

        Overall, the expected output is a well-researched, detailed, and reliable answer that demonstrates a deep understanding of the topic and provides valuable insights and information to the reader.

        Note: Image-based searches should only be used if the query explicitly requires visual information or real-world examples. For queries that do not specifically demand visual content, focus on other search methods such as scholarly articles, news sources, and direct Google searches to gather relevant information.
        """))

    def do_research_w_feedback(self, query, feedback):
        return Task(description=dedent(f"""
      Conduct further research on the given query based on the provided feedback to improve the search results.
      Utilize your specialty background and perspective to gather additional relevant information.

      Feedback:
      ----------
      {feedback}

      Analyze the feedback to identify areas that need improvement or additional exploration. Consider the following:
      - If the feedback indicates a lack of relevance, refine your search keywords and focus on more specific aspects of the query.
      - If the feedback suggests insufficient comprehensiveness, broaden your search to cover more aspects and perspectives related to the query.
      - If the feedback points out a lack of depth, dive deeper into the most relevant subtopics and gather more detailed information.
      - If the feedback questions the reliability of sources, prioritize reputable and authoritative sources such as scholarly articles and expert opinions.

      Your additional research should be guided by the following goal:
      Address the weaknesses identified in the feedback and enhance the search results to provide a more comprehensive, in-depth, and reliable answer to the query.

      Aim to collect the following types of information based on the feedback:
      - Relevant data, examples, or case studies that strengthen the answer's relevance and concreteness.
      - Expert insights, analysis, or practical applications that deepen the understanding of the topic.
      - Scientific evidence, theories, or arguments that reinforce the credibility and reliability of the answer.
      - Illustrative analogies, anecdotes, or real-world examples that clarify complex concepts and make the answer more relatable.

      {self.__tip_section()}
      Remember, the ultimate goal is to incorporate the feedback and improve the search results to deliver a high-quality, informative answer that effectively addresses the query.

      Query:
      ----------
      {query}

    """),
        expected_output=dedent(f"""
        The expected output should be an improved and refined answer to the given query based on the provided feedback. The answer should:

        1. Address the specific areas of improvement identified in the feedback, such as relevance, comprehensiveness, depth, or reliability.
        2. Incorporate additional relevant data, examples, or case studies that strengthen the answer's relevance and concreteness.
        3. Include expert insights, analysis, or practical applications that deepen the understanding of the topic and address any gaps in the previous answer.
        4. Present scientific evidence, theories, or arguments that reinforce the credibility and reliability of the answer, especially if the feedback questioned the sources.
        5. Offer illustrative analogies, anecdotes, or real-world examples that clarify complex concepts and make the answer more relatable and accessible.

        The refined answer should be structured in a logical and coherent manner, with clear connections between the additional information and the original query. It should be written in a clear, concise, and professional tone, addressing the feedback effectively.

        The length of the refined answer may vary depending on the extent of the feedback and the amount of additional relevant information available. However, it should aim to provide a more comprehensive, in-depth, and reliable response to the query compared to the previous answer.

        Overall, the expected output is an improved and refined answer that incorporates the feedback, addresses the identified weaknesses, and provides a higher-quality, informative response to the query.
        """))

    def pick_agent(self, query, agents, agent):
        return Task(description=dedent(f"""
        Given the query below, select the most suitable agent to conduct the research based on their expertise and background.
        
        Consider the agent's specialty, role, and goal to determine their relevance to the query.
        
        Provide a brief explanation for your choice.
        {self.__tip_section()} 
        Query:
        ----------
        {query}
        
        Available Agents:
        ----------
        {agents}
    """), agent=agent, expected_output=dedent(f"""
    The expected output should be the name of the agent selected for the task, without any additional explanation or information.
    
    For example:
    Ethan Nakamura
    
    The output should only include the name of the agent and nothing else, not even an extra comma. This allows for a clear and concise response that directly answers the question of which agent is most suitable for the given query.
    """))

    def evaluate_results(self, query, search_results, agent):
        return Task(description=dedent(f"""
      Evaluate the search results obtained so far and determine if they adequately answer the given query.

      Consider the following criteria:
      - Relevance: Are the results directly related to the query and provide useful information?
      - Comprehensiveness: Do the results cover various aspects of the query and offer a well-rounded understanding?
      - Depth: Are the results detailed enough to provide a satisfactory answer to the query?
      - Reliability: Are the sources of information trustworthy and based on scientific evidence or expert knowledge?

      If the results meet these criteria, provide a positive feedback saying "satisfactory" only. Indicating that the search results are satisfactory. Message should include nothing else.

      If the results are insufficient or lacking in any of the criteria, provide constructive feedback on what aspects need improvement and suggest additional areas to explore or refine.
        {self.__tip_section()}
      Query:
      ----------
      {query}

      Search Results:
      ----------
      {search_results}
    """), agent=agent,  expected_output=dedent(f"""
    The expected output should be a concise evaluation of the search results based on the given criteria. There are two possible outcomes:

    1. If the search results are satisfactory:
       - The output should consist of a single word: "satisfactory"
       - This indicates that the search results adequately answer the query and meet the criteria of relevance, comprehensiveness, depth, and reliability.
       - No further explanation or feedback is required.

    2. If the search results are insufficient or lacking:
       - The output should provide constructive feedback on the specific aspects that need improvement.
       - It should identify which criteria (relevance, comprehensiveness, depth, reliability) are not fully met by the current search results.
       - The feedback should suggest additional areas or topics to explore to enhance the search results and better address the query.
       - The feedback should be concise, clear, and actionable, guiding the agent on how to refine the search and improve the results.
       - The output should maintain a professional and objective tone, avoiding any personal opinions or biases.

    In both cases, the expected output should be focused and directly address the evaluation of the search results. It should not include any irrelevant information or deviate from the specified format.

    The purpose of the expected output is to provide clear guidance to the agent on whether the search results are satisfactory or need further improvement, enabling them to make informed decisions on the next steps in the research process.
    """))

    def final_report(self, query, search_results, agent):
        return Task(description=dedent(f"""
      Generate a final comprehensive report that answers the given query in extreme detail.

      Synthesize the information gathered from the search results, including data, scientific arguments, examples, and any other relevant insights.

      Ensure that the report covers every aspect of the question and provides a well-rounded, informative response.

      Use real-world data and examples to support your explanations and make the report grounded and reliable.
      {self.__tip_section()}
      Query:
      ----------
      {query}

      Search Results:
      ----------
      {search_results}
    """), agent=agent)

    @staticmethod
    def __tip_section():
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"
