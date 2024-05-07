import json
import os

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
    content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
    chunks = [chunk for chunk in content]
    body = "\n\n".join(chunks)

    model = tiktoken.encoding_for_model("gpt-4")
    body_tokens = model.encode(body)
    if len(body_tokens) > 15_000:
      storage = Storage()
      storage.add_chunks(chunks)
      return "Website too context large, added to storage for further querying"

    return body


