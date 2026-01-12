import os
import argparse
from typing import Any, List

from dotenv import load_dotenv
import cohere
from qdrant_client import QdrantClient

from agents import (
    Agent,
    Runner,
    RunConfig,
    OpenAIChatCompletionsModel,
    AsyncOpenAI
)

# ---------------- ENV ----------------
def load_environment_variables() -> None:
    load_dotenv()
    required_vars = [
        "OPENROUTER_API_KEY",
        "QDRANT_URL",
        "QDRANT_API_KEY",
        "QDRANT_COLLECTION_NAME",
        "COHERE_API_KEY",
    ]
    for var in required_vars:
        if not os.getenv(var):
            raise ValueError(f"{var} environment variable not set.")

# ---------------- COHERE ----------------
def get_cohere_client() -> cohere.Client:
    return cohere.Client(os.getenv("COHERE_API_KEY"))

def get_embedding(text: str, cohere_client: cohere.Client) -> List[float]:
    response = cohere_client.embed(
        texts=[text],
        model="embed-english-v3.0",
        input_type="search_query"
    )
    return response.embeddings[0]

# ---------------- QDRANT ----------------
def get_qdrant_client() -> QdrantClient:
    return QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
    )

def search_qdrant(
    query_embedding: List[float],
    qdrant_client: QdrantClient,
    collection_name: str,
    limit: int = 5
) -> List[Any]:
    result = qdrant_client.query_points(
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

# ---------------- MAIN ----------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a RAG agent")
    parser.add_argument("query", type=str, help="User question")
    args = parser.parse_args()

    try:
        load_environment_variables()

        # OpenRouter client
        client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY")
        )

        # LLM Model
        model = OpenAIChatCompletionsModel(
            model="mistralai/devstral-2512:free",
            openai_client=client
        )

        instructions = (
            "You are a RAG assistant. Answer ONLY from the provided context.\n"
            "If the answer is not present, say: I don't know.\n"
            "Cite document numbers in your answer."
        )

        # Clients
        cohere_client = get_cohere_client()
        qdrant_client = get_qdrant_client()
        collection = os.getenv("QDRANT_COLLECTION_NAME")

        # Embed query
        query_embedding = get_embedding(args.query, cohere_client)

        # Retrieve context
        search_results = search_qdrant(
            query_embedding,
            qdrant_client,
            collection
        )

        context = format_retrieved_chunks(search_results)

        if not context.strip():
            print("I don't know. No relevant information found.")
            exit(0)

        # Agent
        agent = Agent(
            name="RAG_Agent",
            model=model,
            instructions=instructions
        )

        user_input = f"Context:\n{context}\n\nQuestion: {args.query}"

        # Runner
        run_config = RunConfig(model=model)
      
        result = Runner.run_sync(
            agent,
            user_input)

        print("\n--- Agent Response ---")
        print(result.final_output)

    except Exception as e:
        print(f"Error: {e}")