import json
import os
import re
import requests
from langchain.tools import tool
from unstructured.partition.html import partition_html

import tiktoken
from src.dria_searching_agent.db import Storage
import os


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
    content = "\n\n".join([str(el) for el in elements])
    content = BrowserTools.clean_text(content)
    content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
    chunks = [chunk for chunk in content]
    body = "\n\n".join(chunks)

    storage = Storage()
    storage.add_text_chunks(chunks, website)
    return "Website ready for querying!"

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


