from fastapi import APIRouter
from starlette.exceptions import HTTPException
from pydantic import BaseModel
from typing import Optional, List
import os

from dotenv import load_dotenv

from .agent import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    AsyncOpenAI,
    get_cohere_client,
    get_qdrant_client,
    get_embedding,
    search_qdrant,
    format_retrieved_chunks,
    load_environment_variables # Import the function to load env vars
)

# Load environment variables at the start of the module
load_environment_variables()

router = APIRouter()

class ChatPayload(BaseModel):
    question: str
    selected_text: Optional[str] = None

class AgentResponse(BaseModel):
    answer: str
    mode: str

# Initialize clients and model once
try:
    openai_client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )
    llm_model = OpenAIChatCompletionsModel(
        model="mistralai/devstral-2512:free",
        openai_client=openai_client
    )
    rag_agent = Agent(
        name="RAG_Agent",
        model=llm_model,
        instructions=(
            "You are a RAG assistant. Answer ONLY from the provided context.\n"
            "If the answer is not present, say: I don't know based on the provided context.\n"
            "Cite document numbers in your answer if present."
        )
    )
    cohere_client = get_cohere_client()
    qdrant_client = get_qdrant_client()
    QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")
    if not QDRANT_COLLECTION_NAME:
        raise ValueError("QDRANT_COLLECTION_NAME environment variable not set.")

except ValueError as e:
    raise RuntimeError(f"Failed to initialize RAG components: {e}") from e

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.post("/chat", response_model=AgentResponse)
async def chat(payload: ChatPayload):
    if not payload.question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    context = ""
    mode = "global_rag"

    if payload.selected_text:
        # This branch will be fully implemented in T021
        mode = "selected_text"
        context = payload.selected_text
    else:
        # Global RAG Mode (T015)
        try:
            query_embedding = get_embedding(payload.question, cohere_client)
            search_results = search_qdrant(
                query_embedding,
                qdrant_client,
                QDRANT_COLLECTION_NAME
            )
            context = format_retrieved_chunks(search_results)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Retrieval error: {e}")

    if not context.strip():
        # Adjusting the response for no context to match spec for selected text mode
        # and provide a general "I don't know" for global mode if no context is retrieved
        if mode == "selected_text":
             return AgentResponse(answer="I don’t know based on the selected text.", mode=mode)
        else:
            return AgentResponse(answer="I don’t know. No relevant information found.", mode=mode)


    user_input = f"Context:\n{context}\n\nQuestion: {payload.question}"

    try:
        result = await Runner.run(rag_agent, user_input) # Use await for async run
        return AgentResponse(answer=result.final_output, mode=mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution error: {e}")
