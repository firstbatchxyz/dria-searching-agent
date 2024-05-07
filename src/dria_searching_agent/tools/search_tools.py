import json
import requests
from langchain.tools import tool, DuckDuckGoSearchRun
import os
from enum import Enum, auto
import httpx
import base64
from crewai import Agent, Task
from src.dria_searching_agent.tools.vision_tools import VisionTools
from src.dria_searching_agent.db import Storage


class Locale(Enum):
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    ITALIAN = "it"
    JAPANESE = "ja"
    KOREAN = "ko"
    DUTCH = "nl"
    PORTUGUESE = "pt"
    RUSSIAN = "ru"
    CHINESE = "zh"
    ARABIC = "ar"
    TURKISH = "tr"
    AZERBAIJANI = "az"

    @classmethod
    def get_locale(cls, language):
        # Find the locale by the name in English
        for locale in cls:
            if locale.name.lower() == language.lower().replace(" ", ""):
                return locale.value
        return cls.ENGLISH.value  # Default to English if not found


class SearchResult:
    def __init__(self, result_data):
        # Directly pass the dictionary, assuming it's already parsed from JSON
        self.title = result_data.get("title", "none")
        self.link = result_data.get("link", "none")
        self.snippet = result_data.get("snippet", "none")
        self.date = result_data.get("date", "none")
        self.position = result_data.get("position", -1)  # -1 indicates missing position

    def __getitem__(self, key):
        return getattr(self, key)

    def __str__(self):
        return f"{self.title} \n {self.link} \n {self.snippet} \n {self.date} \n {self.position}"


class ImageResult:
    def __init__(self, result_data):
        # Directly pass the dictionary, assuming it's already parsed from JSON
        self.title = result_data.get("title", "none")
        self.imageUrl = result_data.get("imageUrl", "none")
        self.imageWidth = result_data.get("imageWidth", -1)
        self.imageHeight = result_data.get("imageHeight", -1)
        self.thumbnailUrl = result_data.get("thumbnailUrl", "none")
        self.thumbnailWidth = result_data.get("thumbnailWidth", -1)
        self.thumbnailHeight = result_data.get("thumbnailHeight", -1)
        self.source = result_data.get("source", "none")
        self.domain = result_data.get("domain", "none")
        self.link = result_data.get("link", "none")
        self.googleUrl = result_data.get("googleUrl", "none")
        self.position = result_data.get("position", -1)  # -1 indicates missing position

    def __getitem__(self, key):
        return getattr(self, key)

    def __call__(self):
        return base64.b64encode(httpx.get(self.imageUrl).content).decode("utf-8")

    def __str__(self):
        return f"{self.title} \n {self.imageUrl} \n {self.imageWidth} \n {self.imageHeight} \n {self.thumbnailUrl} \n {self.thumbnailWidth} \n {self.thumbnailHeight} \n {self.source} \n {self.domain} \n {self.link} \n {self.googleUrl} \n {self.position}"


class ScholarResult:
    def __init__(self, result_data):
        # Directly pass the dictionary, assuming it's already parsed from JSON
        self.title = result_data.get("title", "none")
        self.link = result_data.get("link", "none")
        self.publicationInfo = result_data.get("publicationInfo", "none")
        self.snippet = result_data.get("snippet", "none")
        self.year = result_data.get("year", -1)
        self.citedBy = result_data.get("citedBy", -1)

    def __getitem__(self, key):
        return getattr(self, key)

    def __str__(self):
        return f"{self.title} \n {self.link} \n {self.publicationInfo} \n {self.snippet} \n {self.year} \n {self.citedBy}"


class NewsResult:
    def __init__(self, result_data):
        # Directly pass the dictionary, assuming it's already parsed from JSON
        self.title = result_data.get("title", "none")
        self.link = result_data.get("link", "none")
        self.snippet = result_data.get("snippet", "none")
        self.date = result_data.get("date", "none")
        self.source = result_data.get("source", "none")
        self.imageUrl = result_data.get("imageUrl", "none")
        self.position = result_data.get("position", -1)  # -1 indicates missing position

    def __getitem__(self, key):
        return getattr(self, key)

    def __str__(self):
        return f"{self.title} \n {self.link} \n {self.snippet} \n {self.date} \n {self.source} \n {self.imageUrl} \n {self.position}"


class SerperSearchTools:

    @tool("Arxiv search")
    def search_arxiv(query):
        """
        This is a tool to search the arxiv web about a given question and return relevant sources written on the topic.
        It will return a list of results where each result have an arxiv paper url

        Parameters:
        - query: the question to search for

        {"query": query}

        Returns:
        Response based on the input """
        query = "arxiv " + query
        stype = "search"
        lang = Locale.ENGLISH.value
        n_results = 25

        return SerperSearchTools.search(query, stype, lang, n_results)

    @tool("Search internet")
    def search_internet(query, lang, n_results):
        """
        This is a tool to search the internet about a given question and return relevant results.

        Parameters:
        - query: the question to search for
        - lang: language to search in
        - n_results: number of results to return

        {"query": query, "lang": lang, "n_results": n_results}

        Returns:
        Response based on the input """
        stype = "search"

        return SerperSearchTools.search(query, stype, lang, n_results)

    @tool("Search internet for PDF articles")
    def search_pdf(query, lang, n_results):
        """
        This is a tool to search the web about a given question and stores relevant PDF article in storage.

        Parameters:
        - query: the question to search for
        - lang: language to search in
        - n_results: number of results to return

        {"query": query, "lang": lang, "n_results": n_results}

        Returns:
        State of the operation, successful or error """
        query = "pdf " + query

        return SerperSearchTools.pdf_search(query, lang, n_results)

    @tool("Search scholarly articles")
    def search_articles(query, lang, n_results):
        """
        This is a tool to search the scholar web about a given question and return relevant sources written on the topic.

        Parameters:
        - query: the question to search for
        - lang: language to search in
        - n_results: number of results to return

        {"query": query, "lang": lang, "n_results": n_results}

        Returns:
        Response based on the input """
        stype = "scholar"

        return SerperSearchTools.search(query, stype, lang, n_results)

    @tool("Search news")
    def search_news(query, lang, n_results):
        """
        This is a tool to search the news web about a given question and return relevant news articles.

        Parameters:
        - query: the question to search for
        - lang: language to search in
        - n_results: number of results to return

        {"query": query, "lang": lang, "n_results": n_results}

        Returns:
        Response based on the input """
        stype = "news"

        return SerperSearchTools.search(query, stype, lang, n_results)

    @tool("Search images")
    def search_images(query, lang, n_results):
        """
        This is a tool to search the web for images based on a given query.

        Parameters:
        - query: the query to search for
        - lang: language to search in
        - n_results: number of results to return

        {"query": query, "lang": lang, "n_results": n_results}

        Returns:
        Response based on the input """

        return SerperSearchTools.image_search(query, lang, n_results)

    @tool("Ask storage for context")
    def get_context(query):
        """
        This is a tool to get revelant context of stored PDFs in the storage

        Parameters:
        - query: the query to search for

        {"query": query}

        Returns:
        a list of relevant text chunks with metadata """
        storage = Storage()
        results = storage.query(query)
        return results

    def search(query, stype="search", lang=Locale.ENGLISH.value, n_results=5):

        assert stype in ["search", "scholar", "news"], "Invalid search type"
        url = "https://google.serper.dev/" + stype
        gl = lang if lang != "en" else "us"
        payload = {
            "q": query,
            "gl": gl,
            "hl": lang,
            "page": 1,
            "num": min(n_results, 50)
        }

        if stype == "scholar":
            del payload["num"]

        payload = json.dumps(payload)
        headers = {
            'X-API-KEY': os.environ['SERPER_API_KEY'],
            'content-type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        results = response.json()['organic']
        # knowledge_graph = response.json()['knowledgeGraph']
        if stype == "search":
            results = [SearchResult(result) for result in results[:n_results]]
        elif stype == "scholar":
            results = [ScholarResult(result) for result in results[:n_results]]
        elif stype == "news":
            results = [NewsResult(result) for result in results[:n_results]]
        else:
            raise ValueError("Invalid search type")

        formatted_results = []
        for result in results[:n_results]:
            try:
                formatted_results.append(str(result))
            except KeyError:
                pass

        content = '\n'.join(formatted_results)
        return f"\nSearch result: {content}\n"

    def image_search(query, lang=Locale.ENGLISH.value, n_results=5):
        url = "https://google.serper.dev/" + "image"
        gl = lang if lang != "en" else "us"
        payload = json.dumps({
            "q": query,
            "gl": gl,
            "hl": lang,
            "num": min(n_results, 15)
        })
        headers = {
            'X-API-KEY': os.environ['SERPER_API_KEY'],
            'content-type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        results = response.json()['images']
        results = [ImageResult(result) for result in results[:n_results]]
        # TODO: Add Vision API to get image content
        formatted_results = []
        for result in results[:n_results]:
            try:
                formatted_results.append(str(result))
            except KeyError:
                pass

        content = '\n'.join(formatted_results)
        return f"\nSearch result: {content}\n"

    def pdf_search(query, lang=Locale.ENGLISH.value, n_results=5):
        url = "https://google.serper.dev/" + "search"
        gl = lang if lang != "en" else "us"
        payload = json.dumps({
            "q": query,
            "gl": gl,
            "hl": lang,
            "num": min(n_results, 15)
        })
        headers = {
            'X-API-KEY': os.environ['SERPER_API_KEY'],
            'content-type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        results = response.json()['organic']
        results = [SearchResult(result) for result in results[:n_results]]
        formatted_results = []
        for result in results[:n_results]:
            try:
                formatted_results.append(str(result))
            except KeyError:
                pass

        content = '\n'.join(formatted_results)

        agent = Agent(
            role='Principal Researcher',
            goal='Do amazing researches and summaries based on the content you are working with',
            backstory="You're a Principal Researcher at a big company and you need to do a research about a given topic.",
            allow_delegation=False)

        task = Task(
              agent=agent,
              description=f"""
                You will be provided with a search query and a list of search results. Your task is to determine which 
                search result is the most relevant to the given query.
                
                Here is the search query:
                <query>
                {query}
                </query>
                
                And here are the search results to analyze:
                <search_results>
                {content}
                </search_results>
                
                Please carefully read the search query and each of the search results. 
                Analyze how relevant each search result is to answering the query. 
                Format your result like this:
                [link to the search result]
                
                Remember, I am looking for the single most relevant result from the provided list, not a new search or 
                information from outside the given search_results. 
                Analyze the relevance carefully and explain your reasoning before providing your final result.
                """,
                expected_output="The expected output should be the link to the most relevant search result from the list provided. "
          )
        #TODO: Do OCR here with PDFs.
        most_relevant = task.execute()
        # Double-check the string to pick the url from string using regex
        msg = VisionTools.read_pdf(most_relevant)

        return msg



