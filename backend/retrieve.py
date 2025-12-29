# retrieve.py
# This script will be used to query the Qdrant vector database and validate the RAG retrieval pipeline.

import os
import argparse
import cohere
from dotenv import load_dotenv
from qdrant_client import QdrantClient
import logging

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Environment and Clients Setup ---
load_dotenv()

def init_cohere_client() -> cohere.Client:
    """Initializes and returns the Cohere client."""
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        logging.error("COHERE_API_KEY environment variable not set.")
        raise ValueError("COHERE_API_KEY is required.")
    return cohere.Client(cohere_api_key)

def init_qdrant_client() -> QdrantClient:
    """Initializes and returns the Qdrant client."""
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    if not qdrant_api_key or not qdrant_url:
        logging.error("QDRANT_API_KEY and QDRANT_URL environment variables are required.")
        raise ValueError("QDRANT_API_KEY and QDRANT_URL are required.")
    return QdrantClient(api_key=qdrant_api_key, url=qdrant_url)

def search_qdrant(query: str, co_client: cohere.Client, qd_client: QdrantClient, collection_name: str, top_k: int = 5) -> list:
    """
    Performs a semantic search in the Qdrant collection for a given query.
    """
    try:
        logging.info(f"Embedding query: '{query[:50]}...'")
        query_embedding = co_client.embed(
            texts=[query],
            model="embed-english-v3.0",
            input_type="search_query"
        ).embeddings[0]

        logging.info(f"Searching collection '{collection_name}'...")
        search_results = qd_client.query_points(
            collection_name=collection_name,
            query=query_embedding,
            limit=top_k,
            with_payload=True
        )
        logging.info(f"Found {len(search_results.points)} results.")
        return search_results.points

    except Exception as e:
        logging.error(f"An error occurred during search: {e}")
        return []

def display_results(results: list):
    """
    Prints the search results to the console in a readable format.
    """
    if not results:
        logging.warning("No results found.")
        return

    print("\n--- Search Results ---")
    for i, result in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print(f"Score: {result.score:.4f}")
        if result.payload:
            print(f"Source URL: {result.payload.get('source_url')}")
            print(f"Chunk Index: {result.payload.get('chunk_index')}")
            print("Text:")
            print(result.payload.get('text'))
        print("--------------------")

def main():
    """Main function to orchestrate the retrieval and validation."""
    parser = argparse.ArgumentParser(description="Query the RAG vector database.")
    parser.add_argument("query", type=str, help="The search query to execute.")
    parser.add_argument("--top_k", type=int, default=5, help="The number of results to retrieve.")
    args = parser.parse_args()

    COLLECTION_NAME = "rag_embedding"

    try:
        co_client = init_cohere_client()
        qd_client = init_qdrant_client()
    except ValueError as e:
        logging.critical(f"Client initialization failed: {e}")
        return

    logging.info(f"Searching for: '{args.query}'")
    search_results = search_qdrant(
        query=args.query,
        co_client=co_client,
        qd_client=qd_client,
        collection_name=COLLECTION_NAME,
        top_k=args.top_k
    )

    display_results(search_results)

if __name__ == "__main__":
    main()