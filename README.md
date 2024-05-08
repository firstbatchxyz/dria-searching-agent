<p align="center">
  <img src="https://raw.githubusercontent.com/firstbatchxyz/dria-js-client/master/logo.svg" alt="logo" width="142">
</p>

<p align="center">
  <h1 align="center">
    Dria Search Agent
  </h1>
  <p align="center">
    <i>Dria Search Agent replies queries with scientifically grounded answers with a multi-agent system.</i>
  </p>
</p>

<p align="center">
    <a href="https://opensource.org/license/apache-2-0" target="_blank">
        <img alt="License: Apache-2.0" src="https://img.shields.io/badge/license-Apache%202.0-7CB9E8.svg">
    </a>
    <a href="https://discord.gg/2wuU9ym6fq" target="_blank">
        <img alt="Discord" src="https://static-00.iconduck.com/assets.00/discord-icon-1024x1024-nogerd99.png" width="22">
    </a>
</p>


# DRIA Search Agent

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
poetry run search
```
or 
```bash
poetry run search_v2
```
Which compiles two different versions of the program.

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