import json
import requests
from langchain.tools import tool, DuckDuckGoSearchRun
import os
from enum import Enum, auto
import httpx
import base64
from crewai import Agent, Task



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
    def search_arxiv(inp):
        """
        This is a tool to search the arxiv web about a given question and return relevant sources written on the topic.

        Parameters:
        - query: the question to search for

        {"query": query}

        Returns:
        Response based on the input """
        inp = json.loads(inp)
        query = "arxiv " + inp["query"]
        stype = "search"
        lang = Locale.ENGLISH
        n_results = 25

        return SerperSearchTools.search(query, stype, lang, n_results)

    @tool("Search internet")
    def search_internet(inp):
        """
        This is a tool to search the internet about a given question and return relevant results.

        Parameters:
        - query: the question to search for
        - lang: language to search in
        - n_results: number of results to return

        {"query": query, "lang": lang, "n_results": n_results}

        Returns:
        Response based on the input """
        inp = json.loads(inp)
        query = inp["query"]
        stype = "search"
        lang = inp["lang"]
        n_results = inp["n_results"]

        return SerperSearchTools.search(query, stype, lang, n_results)

    @tool("Search scholarly articles")
    def search_articles(inp):
        """
        This is a tool to search the scholar web about a given question and return relevant sources written on the topic.

        Parameters:
        - query: the question to search for
        - lang: language to search in
        - n_results: number of results to return

        {"query": query, "lang": lang, "n_results": n_results}

        Returns:
        Response based on the input """
        inp = json.loads(inp)
        query = inp["query"]
        stype = "scholar"
        lang = inp["lang"]
        n_results = inp["n_results"]

        return SerperSearchTools.search(query, stype, lang, n_results)

    @tool("Search news")
    def search_news(inp):
        """
        This is a tool to search the news web about a given question and return relevant news articles.

        Parameters:
        - query: the question to search for
        - lang: language to search in
        - n_results: number of results to return

        {"query": query, "lang": lang, "n_results": n_results}

        Returns:
        Response based on the input """
        inp = json.loads(inp)
        query = inp["query"]
        stype = "news"
        lang = inp["lang"]
        n_results = inp["n_results"]

        return SerperSearchTools.search(query, stype, lang, n_results)

    @tool("Search images")
    def search_images(inp):
        """
        This is a tool to search the web for images based on a given query.

        Parameters:
        - query: the query to search for
        - lang: language to search in
        - n_results: number of results to return

        {"query": query, "lang": lang, "n_results": n_results}

        Returns:
        Response based on the input """
        inp = json.loads(inp)
        query = inp["query"]
        lang = inp["lang"]
        n_results = inp["n_results"]

        return SerperSearchTools.image_search(query, lang, n_results)

    def search(query, stype="search", lang=Locale.ENGLISH, n_results=5):

        assert stype in ["search", "scholar", "news"], "Invalid search type"
        url = "https://google.serper.dev/" + stype
        gl = lang.value if lang.value != "en" else "us"
        payload = {
            "q": query,
            "gl": gl,
            "hl": lang.value,
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

    def image_search(query, lang=Locale.ENGLISH, n_results=5):
        url = "https://google.serper.dev/" + "image"
        gl = lang.value if lang.value != "en" else "us"
        payload = json.dumps({
            "q": query,
            "gl": gl,
            "hl": lang.value,
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

    def arxiv_search(query, lang=Locale.ENGLISH, n_results=5):
        url = "https://google.serper.dev/" + "search"
        gl = lang.value if lang.value != "en" else "us"
        payload = json.dumps({
            "q": query,
            "gl": gl,
            "hl": lang.value,
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
              description=f'Analyze the content bellow, make sure to include the most relevant '
                          f'information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{content}'
          )
        #TODO: Do OCR here with PDFs.
        #summary = task.execute()
        #summaries.append(summary)

        return f"\nSearch result: {content}\n"


