from textwrap import dedent


class TaskPrompts:
    def do_research(query, role):
        return dedent(f"""
      Conduct a comprehensive search on the given query using your unique expertise and available tools.
      Utilize your specialty background and {role} perspective to gather relevant information.

      Analyze the query to determine the most appropriate search methods. Consider the following:
      - If the query requires visual information or real-world examples, prioritize image-based searches.
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

      Remember, the ultimate goal is to provide a detailed, informative answer that addresses the query from multiple angles and is supported by reliable, real-world information.

      Query:
      ----------
      {query}
    """)

    def pick_agent(query, agents):
        return dedent(f"""
      Given the query below, select the most suitable agent to conduct the research based on their expertise and background.

      Consider the agent's specialty, role, and goal to determine their relevance to the query.

      Provide a brief explanation for your choice.

      Query:
      ----------
      {query}

      Available Agents:
      ----------
      {agents}
    """)

    def evaluate_results(query, search_results):
        return dedent(f"""
      Evaluate the search results obtained so far and determine if they adequately answer the given query.

      Consider the following criteria:
      - Relevance: Are the results directly related to the query and provide useful information?
      - Comprehensiveness: Do the results cover various aspects of the query and offer a well-rounded understanding?
      - Depth: Are the results detailed enough to provide a satisfactory answer to the query?
      - Reliability: Are the sources of information trustworthy and based on scientific evidence or expert knowledge?

      If the results meet these criteria, provide a positive feedback saying "satisfactory" only. Indicating that the search results are satisfactory. Message should include nothing else.

      If the results are insufficient or lacking in any of the criteria, provide constructive feedback on what aspects need improvement and suggest additional areas to explore or refine.

      Query:
      ----------
      {query}

      Search Results:
      ----------
      {search_results}
    """)

    def final_report(query, search_results):
        return dedent(f"""
      Generate a final comprehensive report that answers the given query in extreme detail.

      Synthesize the information gathered from the search results, including data, scientific arguments, examples, and any other relevant insights.

      Ensure that the report covers every aspect of the question and provides a well-rounded, informative response.

      Use real-world data and examples to support your explanations and make the report grounded and reliable.

      Query:
      ----------
      {query}

      Search Results:
      ----------
      {search_results}
    """)