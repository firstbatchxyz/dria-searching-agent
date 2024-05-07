import json
import os
from collections import defaultdict

import requests
from langchain.tools import tool
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
import httpx
import base64
from io import BytesIO
from src.dria_searching_agent.db import Storage


def read_response_bytes(response):
    stream = BytesIO()
    for chunk in response.iter_content(chunk_size=1024 * 1024):  # Process the stream in chunks of 1MB
        stream.write(chunk)
    stream.seek(0)

    return stream
def to_chunks(fname):
    from unstructured.partition.pdf import partition_pdf
    from unstructured.chunking.title import chunk_by_title
    import re
    from unstructured.cleaners.core import clean_non_ascii_chars, clean_extra_whitespace, group_broken_paragraphs, \
        replace_unicode_quotes
    para_split_re = re.compile(r"(\s*\n\s*){3}")
    response = requests.get(fname)
    response_bytes = read_response_bytes(response)

    elements = partition_pdf(file=response_bytes, include_page_breaks=False)
    language_d = defaultdict(int)
    for el in elements:
        language = el.metadata.languages[0]
        language_d[language] += 1
        el.apply(replace_unicode_quotes)
        el.apply(clean_extra_whitespace)
        el.apply(clean_non_ascii_chars)
    chunks = chunk_by_title(elements, max_characters=1000)
    for chunk in chunks:
        chunk.text = group_broken_paragraphs(chunk.text, paragraph_split=para_split_re)
    return [{"text": chunk.text, "id": chunk.id, "page": str(chunk.metadata.page_number)} for chunk in chunks], list(language_d.keys())[0]


def download_pdf(url, save_path):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Open a local file with write-binary mode
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"PDF saved successfully at {save_path}")
    else:
        print(f"Failed to download PDF: status code {response.status_code}")


class VisionTools:
    @tool("Image analysis")
    def vision(url, query):
        """
    This is a tool used to analyze an image based on a query

    Parameters:
    - query: This is the query
    - url: This is the url of the image to be analyzed

    {"prompt": prompt, "url": url}

    Returns:
    Response from the vision model based on the prompt and image provided
    """

        chat = ChatAnthropic(model=os.environ["CLAUDE_SONNET"], api_key=os.environ['ANTHROPIC_KEY'])
        #url = inp["url"]
        #query = inp["query"]
        # Check if url ends with jpg, jpeg or png, or other
        if url.endswith("jpg") or url.endswith("jpeg") or url.endswith("png"):
            media_type = "image/{}".format(url.split(".")[-1])
        else:
            raise ValueError("Invalid image format")

        data = base64.b64encode(httpx.get(url).content).decode("utf-8")
        messages = [
            HumanMessage(
                content=[
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{media_type};base64,{data}",
                        },
                    },
                    {"type": "text", "text": query},
                ]
            )
        ]
        re = chat.invoke(messages)
        return re.content

    @tool("Read PDF analysis")
    def read_pdf(url):
        """
    This is a tool used to extract text from a PDF and store it in a storage
        Parameters:
        - url: This is the url of the PDF to be analyzed
        :return:
    """
        # Download PDF from URL
        # Read the PDF
        chunks, lang = to_chunks(url)
        storage = Storage()
        storage.add_chunks(chunks)
        return "Pdf added to storage successfully"
