import os
import argparse
from typing import Any, List
from dotenv import load_dotenv
import cohere
from qdrant_client import QdrantClient

# This assumes the 'agents' library is installed and requires openai>=1.0.0
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI

# ---------------- ENV ----------------
def load_environment_variables() -> None:
    load_dotenv()
    required_vars = [
        "OPENROUTER_API_KEY", "QDRANT_URL", "QDRANT_API_KEY",
        "QDRANT_COLLECTION_NAME", "COHERE_API_KEY",
    ]
    for var in required_vars:
        if not os.getenv(var):
            raise ValueError(f"{var} environment variable not set.")

# ---------------- CLIENTS & MODEL (GLOBAL) ----------------
# Load vars and initialize clients once on module load
try:
    load_environment_variables()

    # OpenAI Client for the LLM
    openai_client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )

    # LLM Model
    llm_model = OpenAIChatCompletionsModel(
        model="mistralai/devstral-2512:free",
        openai_client=openai_client
    )

    # RAG Agent
    rag_agent = Agent(
        name="RAG_Agent",
        model=llm_model,
        instructions=(
            "You are a RAG assistant. Answer ONLY from the provided context.\n"
            "If the answer is not present, say: I don't know based on the provided context."
        )
    )

    # Other clients
    cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))
    qdrant_client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
    )
    QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")

except (ValueError, ImportError) as e:
    raise RuntimeError(f"Failed to initialize agent components: {e}")

# ---------------- EMBEDDING & RETRIEVAL FUNCTIONS ----------------
def get_embedding(text: str, client: cohere.Client) -> List[float]:
    response = client.embed(
        texts=[text],
        model="embed-english-v3.0",
        input_type="search_query"
    )
    return response.embeddings[0]

def search_qdrant(
    query_embedding: List[float],
    client: QdrantClient,
    collection_name: str,
    limit: int = 5
) -> List[Any]:
    result = client.query_points(
        collection_name=collection_name,
        query=query_embedding,
        limit=limit,
        with_payload=True
    )
    return result.points

def format_retrieved_chunks(search_results: List[Any]) -> str:
    context_parts = []
    for i, hit in enumerate(search_results):
        text = hit.payload.get("text", "")
        if text:
            context_parts.append(f"Document {i+1}:\n{text}\n")
    return "\n".join(context_parts)

# ---------------- MAIN (for CLI testing) ----------------
async def main_async():
    parser = argparse.ArgumentParser(description="Run a RAG agent")
    parser.add_argument("query", type=str, help="User question")
    args = parser.parse_args()

    try:
        query_embedding = get_embedding(args.query, cohere_client)
        search_results = search_qdrant(query_embedding, qdrant_client, QDRANT_COLLECTION_NAME)
        context = format_retrieved_chunks(search_results)

        if not context.strip():
            print("I don't know. No relevant information found.")
            return

        user_input = f"Context:\n{context}\n\nQuestion: {args.query}"

        result = await Runner.run(rag_agent, user_input)

        print("\n--- Agent Response ---")
        print(result.final_output)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main_async())