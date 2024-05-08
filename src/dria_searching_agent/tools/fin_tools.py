from langchain.tools import tool
import requests
from bs4 import BeautifulSoup

import json


class FinancialData:
    @tool("Financial Data collector")
    def scrape(exchange, ticker):
        """
        This is a tool used to collect financial stock data

        Parameters:
        - exchange: stock exchange MIC for the stock involved
        - ticker: ticker symbol of the stock

        {"exchange": exchange, "ticker": ticker}

        Returns:
        Response based on the input
        """
        BASE_URL = "https://www.google.com/finance"
        INDEX = exchange
        SYMBOL = ticker
        LANGUAGE = "en"
        TARGET_URL = f"{BASE_URL}/quote/{SYMBOL}:{INDEX}?hl={LANGUAGE}"

        page = requests.get(TARGET_URL)
        soup = BeautifulSoup(page.content, "html.parser")

        items = soup.find_all("div", {"class": "gyFHrc"})

        stock_description = {}
        for item in items:
            item_description = item.find("div", {"class": "mfs7Fc"}).text
            item_value = item.find("div", {"class": "P6K39c"}).text
            stock_description[item_description] = item_value

        return stock_description


def main():
    BASE_URL = "https://www.google.com/finance"
    INDEX = "NASDAQ"
    SYMBOL = "AAPL"
    LANGUAGE = "en"
    TARGET_URL = f"{BASE_URL}/quote/{SYMBOL}:{INDEX}?hl={LANGUAGE}"

    page = requests.get(TARGET_URL)
    soup = BeautifulSoup(page.content, "html.parser")

    items = soup.find_all("div", {"class": "gyFHrc"})

    stock_description = {}
    for item in items:
        item_description = item.find("div", {"class": "mfs7Fc"}).text
        item_value = item.find("div", {"class": "P6K39c"}).text
        stock_description[item_description] = item_value
    print(stock_description)