# Langchain Agent

A minimal LangChain-based agent project built for experimentation and learning. This repository demonstrates how to set up a Python environment, install dependencies, and run a simple agent-driven application using environment-based API keys.

## Features

- Simple LangChain agent scaffold
- Environment variable support via `.env`
- Example app entrypoints: `app.py`, `main.py`
- Notebook research work in `research/agent_demo.ipynb`

## Technology

- Python 3.11
- LangChain
- OpenAI API
- dotenv for environment configuration

## Architecture

This repository is organized as a small Python agent project:

- `app.py` - Primary application script for launching the agent logic.
- `main.py` - Secondary entrypoint, typically used for testing or demo execution.
- `requirements.txt` - Python dependencies required to run the project.
- `.env` - Local environment variables containing API keys.
- `research/agent_demo.ipynb` - Jupyter notebook for experimentation and development notes.

The application follows a simple architecture:

1. Load configuration from `.env`.
2. Initialize the agent and language model client.
3. Execute the agent workflow through `app.py` or `main.py`.

## Getting Started

### Prerequisites

- Python 3.11
- `conda` or any Python virtual environment manager

### Installation

```bash
conda create -n langagent python=3.11 -y
conda activate langagent
pip install -r requirements.txt
```

### Configuration

Create a `.env` file at the repository root and add your API keys:

```dotenv
OPENAI_API_KEY="your-openai-api-key"
TAVILY_API_KEY="your-tavily-api-key"
WEATHERSTACK_API_KEY="your-weatherstack-api-key"
```

> Do not commit your `.env` file or secret keys to source control.

### Run the Project

Use one of the Python entrypoints:

```bash
python app.py
```

or

```bash
python main.py
```

### Notebook Exploration

Open the research notebook for additional agent demos and experiments:

```bash
jupyter notebook research/agent_demo.ipynb
```

## Project Structure

```text
.
├── .env
├── README.md
├── app.py
├── main.py
├── requirements.txt
└── research/
    └── agent_demo.ipynb
```

## Contribution

Contributions are welcome. If you'd like to improve this repo, open an issue or submit a pull request with enhancements, bug fixes, or documentation improvements.

## License

This project is provided under an open source-friendly license. Add a license file if you want to publish this repository publicly.
