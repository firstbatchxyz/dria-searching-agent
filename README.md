# DRIA Searching Agent

DRIA Searching Agent is an AI-powered tool that answers your questions by selecting the most relevant agent from a pool of agents with different backstories. The selected agent searches the internet, reads articles and websites, and provides a detailed response to your query.

## Prerequisites
- Python 3.12 or 3.13
- Poetry
- Docker

## Installation
1. Install Poetry:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
2. Clone the repository:
   ```bash
   git clone git@github.com:firstbatchxyz/dria-searching-agent.git
   cd dria-searching-agent
   ```
3. Install dependencies using Poetry:
   ```bash
   poetry install
   ```
## Docker Compose
The project includes a `docker-compose.yml` file for running Qdrant and Browserless services. To start the services, run:
```bash
docker-compose up -d
```

## Running the Application
Run the application using Poetry:
```bash
poetry run app
```

This command sets up a virtual environment specific to the project and executes the `app` script or module specified in the `pyproject.toml` under `[tool.poetry.scripts]`.



This will start Qdrant and Browserless services in the background.

## How to Use
1. Ask a question or provide a query.
2. The DRIA Searching Agent will select the most relevant agent from its pool based on the question.
3. The selected agent will search the internet, read articles, and gather information to provide a detailed response.
4. The agent will present the answer to your question, along with the sources used to compile the response.

## Additional Tools and Commands
- Run tests with Poetry using a command like `poetry run pytest`.
- Update Python dependencies using `poetry update`.