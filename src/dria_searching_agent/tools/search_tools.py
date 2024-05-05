import json
import os

import requests
from langchain.tools import tool
from dotenv import load_dotenv
import os
from enum import Enum, auto
import httpx
import base64


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


class SearchTools:

    @tool("Search internet")
    def search_internet(query):
        """Useful to search the internet about a given topic and return relevant
    results."""
        return SearchTools.search(query)

    @tool("Search instagram")
    def search_instagram(query):
        """Useful to search for instagram post about a given topic and return relevant
    results."""
        query = f"site:instagram.com {query}"
        return SearchTools.search(query)

    def search(query, lang=Locale.ENGLISH, n_results=5):
        url = "https://google.serper.dev/" + "search"
        payload = json.dumps({
            "q": query,
            "gl": lang.value,
            "hl": lang.value,
            "page": 2
        })
        headers = {
            'X-API-KEY': os.environ['SERPER_API_KEY'],
            'content-type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        results = response.json()['organic']
        knowledge_graph = response.json()['knowledgeGraph']
        results = [SearchResult(result) for result in results[:n_results]]
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
        payload = json.dumps({
            "q": query,
            "gl": lang.value,
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
        formatted_results = []
        for result in results[:n_results]:
            try:
                formatted_results.append(str(result))
            except KeyError:
                pass

        content = '\n'.join(formatted_results)
        return f"\nSearch result: {content}\n"

    def news_search(query, lang=Locale.ENGLISH, n_results=5):
        url = "https://google.serper.dev/" + "news"
        payload = json.dumps({
            "q": query,
            "gl": lang.value,
            "hl": lang.value,
            "page": 2
        })

        headers = {
            'X-API-KEY': os.environ['SERPER_API_KEY'],
            'content-type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)

