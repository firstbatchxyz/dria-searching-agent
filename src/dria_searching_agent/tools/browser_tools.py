import json
import os

import requests
from crewai import Agent, Task
from playwright.sync_api import sync_playwright
from langchain.tools import tool
from unstructured.partition.html import partition_html

from dotenv import load_dotenv
import os


class BrowserTools:

  @tool("Scraper")
  def scrape_website(website):
    """Useful to scrape and summarize a website content"""
    url = f"http://0.0.0.0:3000/content?token={os.getenv('BROWSERLESS_TOKEN')}"
    payload = json.dumps({"url": website})
    headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    elements = partition_html(text=response.text)
    content = "\n\n".join([str(el) for el in elements])
    content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
    for chunk in content:
      print(chunk)
      print("\n\n")
    """
    summaries = []
    for chunk in content:
      agent = Agent(
          role='Principal Researcher',
          goal=
          'Do amazing researches and summaries based on the content you are working with',
          backstory=
          "You're a Principal Researcher at a big company and you need to do a research about a given topic.",
          allow_delegation=False)
      task = Task(
          agent=agent,
          description=
          f'Analyze and summarize the content bellow, make sure to include the most relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{chunk}'
      )
      summary = task.execute()
      summaries.append(summary)
    """
    return ""#"\n\n".join(summaries)



def main():
    load_dotenv()
    bt = BrowserTools()
    d = bt.scrape_website("https://towardsdatascience.com/understanding-kl-divergence-f3ddc8dff254")
    print("Hello, I am a searching agent")


def test():

  with sync_playwright() as p:
    browser = p.firefox.connect('wss://production-sfo.browserless.io/firefox/playwright?token=GOES-HERE')
    context = browser.new_context()
    page = context.new_page()
    page.goto('http://www.example.com', wait_until='domcontentloaded')
    print(page.content())
    context.close()