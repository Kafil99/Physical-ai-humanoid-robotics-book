# main.py
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from chatbot_api import router as chatbot_router

# This script will contain the logic for the RAG content ingestion pipeline.

import os
import uuid
import requests
from bs4 import BeautifulSoup
import cohere
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
import logging

# --- FastAPI App Setup ---
app = FastAPI()

# Add CORS middleware to allow requests from the Docusaurus frontend
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chatbot_router, prefix="/api")

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Environment and Clients Setup ---
load_dotenv()

def init_cohere_client():
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        logging.error("COHERE_API_KEY environment variable not set.")
        raise ValueError("COHERE_API_KEY is required.")
    return cohere.Client(cohere_api_key)

def init_qdrant_client():
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    if not qdrant_api_key or not qdrant_url:
        logging.error("QDRANT_API_KEY or QDRANT_URL environment variable not set.")
        raise ValueError("QDRANT_API_KEY and QDRANT_URL are required.")
    return QdrantClient(api_key=qdrant_api_key, url=qdrant_url)

DOCUSAURUS_BASE_URL = "https://physical-ai-humanoid-robotics-book-pink-delta.vercel.app"

def get_all_urls(sitemap_url: str) -> list[str]:
    """
    Parses a sitemap.xml file and returns a list of all URLs.
    """
    urls = []
    try:
        response = requests.get(sitemap_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "xml")
        locs = soup.find_all("loc")
        for loc in locs:
            # Replace placeholder URL with the actual deployed base URL
            corrected_url = loc.text.replace("https://your-docusaurus-site.example.com", DOCUSAURUS_BASE_URL)
            urls.append(corrected_url)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching sitemap: {e}")
    return urls

def extract_text_from_url(url: str) -> str:
    """
    Downloads HTML from a URL and extracts clean text from the <article> tag.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        article = soup.find("article")
        if article:
            return article.get_text(separator=" ", strip=True)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching URL {url}: {e}")
    return ""

def chunk_text(text: str, chunk_size: int = 2000, overlap: int = 400) -> list[str]:
    """
    Splits a text into fixed-size chunks with overlap.
    """
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def embed(co_client: cohere.Client, chunks: list[str]) -> list[list[float]]:
    """
    Generates embeddings for a list of text chunks using the Cohere API.
    """
    if not chunks:
        return []
    try:
        response = co_client.embed(
            texts=chunks,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return response.embeddings
    except cohere.CohereError as e:
        logging.error(f"Cohere API error during embedding: {e}")
        return []

def create_collection(qd_client: QdrantClient, collection_name: str):
    """
    Creates a collection in Qdrant if it does not already exist.
    If it exists, it will delete and recreate it to ensure a clean state as per spec.
    """
    try:
        if qd_client.collection_exists(collection_name=collection_name):
            logging.info(f"Collection '{collection_name}' already exists. Deleting and recreating...")
            qd_client.delete_collection(collection_name=collection_name)
        
        qd_client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE),
        )
        logging.info(f"Collection '{collection_name}' created successfully.")
    except Exception as e:
        logging.error(f"Error creating Qdrant collection: {e}")
        raise

def save_chunks_to_qdrant(qd_client: QdrantClient, collection_name: str, chunks: list[str], embeddings: list[list[float]], source_url: str):
    """
    Saves chunks and their embeddings to Qdrant.
    """
    if not chunks or not embeddings:
        return

    try:
        qd_client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embeddings[i],
                    payload={"text": chunk, "source_url": source_url, "chunk_index": i}
                ) for i, chunk in enumerate(chunks)
            ],
            wait=True
        )
        logging.info(f"Saved {len(chunks)} chunks to collection '{collection_name}'.")
    except Exception as e:
        logging.error(f"Error saving chunks to Qdrant: {e}")

def run_ingestion():
    """Main function to orchestrate the ingestion pipeline."""
    logging.info("RAG Content Ingestion Pipeline Started")
    SITEMAP_URL = "https://physical-ai-humanoid-robotics-book-pink-delta.vercel.app/sitemap.xml"
    COLLECTION_NAME = "rag_embedding"

    try:
        co_client = init_cohere_client()
        qd_client = init_qdrant_client()
    except ValueError as e:
        logging.critical(f"Client initialization failed: {e}")
        return

    all_urls = get_all_urls(SITEMAP_URL)
    logging.info(f"Found {len(all_urls)} URLs in the sitemap.")
    if not all_urls:
        logging.warning("No URLs found. Exiting.")
        return

    try:
        create_collection(qd_client, COLLECTION_NAME)
    except Exception:
        logging.critical("Failed to create Qdrant collection. Aborting.")
        return

    for url in all_urls:
        logging.info(f"--- Processing URL: {url} ---")
        
        text = extract_text_from_url(url)
        if not text:
            logging.warning(f"No content found for {url}, skipping.")
            continue
        logging.info(f"Extracted {len(text)} characters.")

        chunks = chunk_text(text)
        logging.info(f"Created {len(chunks)} chunks.")
        if not chunks:
            continue

        embeddings = embed(co_client, chunks)
        if not embeddings:
            logging.warning(f"Failed to generate embeddings for {url}, skipping.")
            continue
        logging.info(f"Generated {len(embeddings)} embeddings.")
        
        save_chunks_to_qdrant(qd_client, COLLECTION_NAME, chunks, embeddings, url)

    logging.info("--- Ingestion complete! ---")

if __name__ == "__main__":
    # This block allows running the ingestion script directly
    # e.g., `python backend/main.py ingest`
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "ingest":
        run_ingestion()
    else:
        # This will run the FastAPI app
        uvicorn.run(app, host="0.0.0.0", port=8000)
