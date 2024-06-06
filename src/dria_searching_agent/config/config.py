import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()  # This loads environment variables from a .env file if it exists
        
        self.agent_model_provider = os.getenv('AGENT_MODEL_PROVIDER')
        self.agent_model = os.getenv('AGENT_MODEL')
        self.agent_max_iter = os.getenv('AGENT_MAX_ITER', 10)

        self.anthropic_key = os.getenv('ANTHROPIC_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.serper_api_key = os.getenv('SERPER_API_KEY')
        self.browserless_token = os.getenv('BROWSERLESS_TOKEN')
        
        self.vision_tool_model = os.getenv('VISION_TOOL_MODEL', "CLAUDE_SONNET")

        self.ollama_url = os.getenv('OLLAMA_URL')
        self.qdrant_url = os.getenv('QDRANT_URL')
        self.browserless_url = os.getenv('BROWSERLESS_URL')

config = Config()
def load_config():
    global config
    config = Config()

def AGENT_MODEL_PROVIDER():
    return config.agent_model_provider

def AGENT_MODEL():
    return config.agent_model

def AGENT_MAX_ITER():
    return config.agent_max_iter

def ANTHROPIC_KEY():
    return config.anthropic_key

def OPENAI_API_KEY():
    return config.openai_api_key

def OLLAMA_URL():
    return config.ollama_url

def BROWSERLESS_TOKEN():
    return config.browserless_token

def SERPER_API_KEY():
    return config.serper_api_key

def QDRANT_URL():
    return config.qdrant_url

def BROWSERLESS_URL():
    return config.browserless_url

def VISION_TOOL_MODEL():
    return config.vision_tool_model

