import json
import os
import re
import requests
from langchain.tools import tool
from unstructured.partition.html import partition_html

import tiktoken
from src.dria_searching_agent.db import Storage
import os
from textblob import TextBlob


class BrowserTools:

  @tool("Scraper")
  def scrape_website(website):
    """
    Tool used to scrape a website content
    Useful to scrape and analyze website content to extract information

    """
    url = f"http://0.0.0.0:3000/content?token={os.getenv('BROWSERLESS_TOKEN')}"
    payload = json.dumps({"url": website})
    headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    elements = partition_html(text=response.text)
    elements = [el for el in elements if el.category in ["NarrativeText", "Title"]]
    body = "\n\n".join([str(el) for el in elements])
    body = BrowserTools.clean_text(body)
    blob = TextBlob(body)
    chunks = [sent.raw.replace("\n", " ") for sent in blob.sentences]

    #storage = Storage()
    #storage.add_text_chunks(chunks, website)
    #print("Collection size: ", storage.client.count(collection_name=storage.col_name))
    return "\n".join(chunks)

  def clean_text(text):
    # Remove unwanted repeated lines and navigational text
    text = re.sub(r'\n\t+', '\n', text)  # Remove tab characters and excessive newlines
    text = re.sub(r'Toggle \w+ subsection', '', text)  # Remove toggle texts
    text = re.sub(r'[\n\r]+', '\n', text)  # Replace multiple newlines with a single newline
    text = re.sub(r'(\nSee also|\nNotes|\nReferences|\nSources|\nFurther reading|\nExternal links).*', '', text,
                  flags=re.DOTALL)  # Remove sections from "See also" to the end
    text = text.strip()  # Remove leading and trailing whitespace
    return text


def main():
    r = BrowserTools.scrape_website("https://en.wikipedia.org/wiki/Quantum_computing")


