# RAG Content Ingestion Pipeline

This directory contains the Python script for ingesting content from the Docusaurus website (`https://physical-ai-humanoid-robotics-book-pink-delta.vercel.app/`) into a Qdrant vector database.

## Setup

### 1. Environment Variables

Create a file named `.env` in this `backend/` directory. This file is used to store your secret API keys. Add the following keys to the file, replacing the placeholder values with your actual keys:

```
# .env

# Your Qdrant Cloud API Key
QDRANT_API_KEY="your_qdrant_api_key_here"

# The URL for your Qdrant Cloud instance
QDRANT_URL="https://your-qdrant-instance-url.qdrant.tech"

# Your Cohere API Key
COHERE_API_KEY="your_cohere_api_key_here"
```

### 2. Install Dependencies

This project uses `uv` for package and virtual environment management.

First, create the virtual environment:
```sh
uv venv
```

Then, install the dependencies listed in `pyproject.toml`:



```sh

# On Windows

.venv\Scripts\activate

uv pip sync



# On macOS/Linux (and other Unix-like systems)

source .venv/bin/activate

uv pip sync

```

## Usage

Once the setup is complete, you can run the ingestion pipeline from within the activated virtual environment:

```sh
python main.py
```

The script will log its progress to the console, indicating which URLs are being processed and when the ingestion is complete.

## Validation

After running the ingestion pipeline, you can validate the retrieval process using the `retrieve.py` script.

This script takes a search query as a command-line argument.

### Usage

From within the activated virtual environment, run the script with your query:
```sh
python retrieve.py "your search query here"
```

You can also specify the number of results to return with the `--top_k` flag:
```sh
python retrieve.py "what is ROS 2?" --top_k 3
```
