import json
import os

import requests
from langchain.tools import tool
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
import httpx
import base64


class Vision:
    @tool("Image analysis")
    def vision(inp):
        """
    This is a tool used to analyze an image based on a query

    Parameters:
    - query: This is the query
    - url: This is the url of the image to be analyzed

    {"prompt": prompt, "url": url}

    Returns:
    Response from the vision model based on the prompt and image provided
    """

        inp = json.loads(inp)

        chat = ChatAnthropic(model=os.environ["CLAUDE_SONNET"], api_key=os.environ['ANTHROPIC_KEY'])
        url = inp["url"]
        query = inp["query"]
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
