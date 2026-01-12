# main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import cohere
from qdrant_client import QdrantClient
from dotenv import load_dotenv

# Assume agents is an installed library based on the spec
from agents import Agent, Runner, RunConfig, OpenAIChatCompletionsModel, AsyncOpenAI

# Import functions from agent.py
from agent import (
    load_environment_variables,
    get_cohere_client,
    get_qdrant_client,
    get_embedding,
    search_qdrant,
    format_retrieved_chunks,
)

# --- FastAPI App Initialization ---
app = FastAPI()

# --- CORS Configuration ---
# This allows the frontend to communicate with the backend
origins = [
    "http://localhost:3000",  # Docusaurus default dev port
    "http://localhost:3001",
    "https://physical-ai-humanoid-robotics-book-pink-delta.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Environment and Clients Setup ---
try:
    load_environment_variables()
except ValueError as e:
    print(f"Error loading environment variables: {e}")
    # Handle the error appropriately, maybe exit or use default fallbacks
    # For now, we'll print the error and continue, but in production, you might want to stop
    # if the application can't function without these variables.

# Initialize clients once at startup
cohere_client = get_cohere_client()
qdrant_client = get_qdrant_client()
collection_name = os.getenv("QDRANT_COLLECTION_NAME")

# OpenRouter client for the LLM
openrouter_client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# LLM Model
model = OpenAIChatCompletionsModel(
    model="mistralai/devstral-2512:free",
    openai_client=openrouter_client
)

# --- API Models ---
from schemas import ChatRequest, ChatResponse

# --- Agent Instructions ---
instructions = (
    "You are a RAG assistant. Answer ONLY from the provided context.\n"
    "If the answer is not present, say: I don't know.\n"
    "Cite document numbers in your answer when possible."
)

# --- FastAPI Endpoints ---
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Handles chat requests, supporting both global RAG and selected text modes.
    """
    context = ""
    
    if request.selected_text:
        # 2. Selected Text Mode (Strict Context Mode)
        context = f"Document 1:\n{request.selected_text}\n"
    else:
        # 1. Global Book RAG Mode (Default)
        # Embed the user's question
        query_embedding = get_embedding(request.question, cohere_client)

        # Retrieve relevant context from Qdrant
        search_results = search_qdrant(query_embedding, qdrant_client, collection_name)
        
        context = format_retrieved_chunks(search_results)

    if not context.strip():
        return ChatResponse(answer="I don't know. No relevant information found.")

    # Create the agent
    agent = Agent(
        name="RAG_Agent",
        model=model,
        instructions=instructions
    )
    
    # Prepare the input for the agent
    user_input = f"Context:\n{context}\n\nQuestion: {request.question}"

    # Run the agent asynchronously as per the spec
    try:
        # The spec requires `await Runner.run(...)`
        result = await Runner.run(agent, user_input)
        answer = result.final_output
    except Exception as e:
        # Handle potential errors during agent execution
        print(f"Error during agent execution: {e}")
        # As per the spec, handle errors gracefully without crashing
        return ChatResponse(answer="An error occurred while processing your request.")

    return ChatResponse(answer=answer)

@app.get("/")
def read_root():
    return {"message": "FastAPI server for the RAG agent is running."}
