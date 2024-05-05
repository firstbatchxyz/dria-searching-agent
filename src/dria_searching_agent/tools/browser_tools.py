import json
import os

import requests
from langchain.tools import tool
from unstructured.partition.html import partition_html

from dotenv import load_dotenv
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
    return "\n\n".join(chunks)

