## Getting Started

### Prerequisites
- Ensure you have Python 3.12 or 3.13 installed.
- Install Poetry:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
  
### Installation
Clone the repository and install dependencies:
```bash
git clone git@github.com:firstbatchxyz/dria-searching-agent.git
cd dria-searching-agent
poetry install
```

### Running the Application
Run app directly with:
```bash
poetry run app
```


```bash
docker build -t agent-browser .
docker run -p 3000:3000 agent-browser
docker run -p 3000:3000 -e "TOKEN=6R0W53R135510" ghcr.io/browserless/chromium
``` 

