from fastapi import APIRouter
from starlette.exceptions import HTTPException
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

# Assuming 'agent.py' contains the necessary agent setup and a functioning Runner
from agent import (
    rag_agent,
    cohere_client,
    qdrant_client,
    QDRANT_COLLECTION_NAME,
    get_embedding,
    search_qdrant,
    format_retrieved_chunks,
    load_environment_variables,
    Runner,
)

# Load environment variables at the start
load_environment_variables()

router = APIRouter()


class ChatPayload(BaseModel):
    question: str
    selected_text: Optional[str] = None


class AgentResponse(BaseModel):
    answer: str


@router.post("/chat", response_model=AgentResponse)
async def chat(payload: ChatPayload):
    """
    Handles chat requests, supporting both global and selected-text modes.
    """
    if not payload.question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # --- STRICT 'selected_text' LOGIC ---
    if payload.selected_text and payload.selected_text.strip():
        # If selected_text is provided, it is the ONLY context.
        # Vector search is SKIPPED.
        
        context = payload.selected_text
        question = payload.question

        # A highly specific, deterministic prompt for explaining selected text.
        # This forces the LLM to act as an explainer, not a search agent.
        user_input = f"""
        You are an expert assistant. Your task is to explain the following text snippet provided by the user.
        The user's question is: "{question}"

        **Provided Text Snippet:**
        ---
        {context}
        ---

        Based ONLY on the text snippet above, provide a clear and concise explanation.
        - If the question is generic like "What is this?" or "Explain", summarize the text.
        - If the question is specific, answer it directly from the text.
        - Do NOT use any outside knowledge.
        - Do NOT mention that you are basing your answer on the provided text.
        """
        
        try:
            result = await Runner.run(rag_agent, user_input)
            answer = result.final_output
            if not answer:
                # This should rarely happen with the new prompt, but is a safe fallback.
                answer = "I was unable to generate an explanation from the selected text."
            return AgentResponse(answer=answer)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Agent execution error for selected text: {str(e)}")

    # --- GLOBAL RAG LOGIC ---
    else:
        # If no selected_text, proceed with the normal vector search.
        try:
            query_embedding = get_embedding(payload.question, cohere_client)
            search_results = search_qdrant(
                query_embedding,
                qdrant_client,
                QDRANT_COLLECTION_NAME,
            )
            context = format_retrieved_chunks(search_results)
            
            if not context.strip():
                return AgentResponse(answer="I could not find any relevant information in the book to answer that question.")

            # Standard RAG prompt
            user_input = f"Using the following context from the book:\n---\n{context}\n---\nAnswer the following question: {payload.question}"
            
            result = await Runner.run(rag_agent, user_input)
            answer = result.final_output
            if not answer:
                answer = "I was unable to determine an answer from the provided context."
            return AgentResponse(answer=answer)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Global RAG error: {str(e)}")
