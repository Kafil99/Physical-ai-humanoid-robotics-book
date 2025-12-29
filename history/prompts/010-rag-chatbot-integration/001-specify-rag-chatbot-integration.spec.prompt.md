---
id: 001
title: Specify RAG Chatbot Integration
stage: spec
date: 2025-12-29
surface: agent
model: gemini-cli
feature: 010-rag-chatbot-integration
branch: 010-rag-chatbot-integration
user:
command: /sp.specify
labels: [spec, rag, chatbot, fastapi]
links:
  spec: specs/010-rag-chatbot-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/010-rag-chatbot-integration/spec.md
  - specs/010-rag-chatbot-integration/checklists/requirements.md
tests:
  - none
---

## Prompt

Integrate the RAG agent with an attractive frontend chatbot using FastAPI to enable end-to-end question answering over book content, including answering questions based only on user-selected text IMPORTANT IMPLEMENTATION CONSTRAINT: The Spec-3 agent has already been manually corrected to use the official OpenAI Agents SDK. This implementation must be reused as-is. Do NOT regenerate, refactor, or replace the agent core. --- # 🎯 Target Audience - Full-stack engineers integrating AI agents into web applications - Evaluators validating a complete, user-facing RAG system --- ## 🔍 Focus - Wrapping the standalone RAG agent (Spec-3) with a FastAPI backend - Building a web-based chatbot frontend with an interactive UI - Adding a floating chatbot icon that toggles the chat interface - Enabling user queries to flow from frontend → FastAPI → agent → Qdrant → response - Allowing users to ask questions based on text they explicitly select in the book - Completing the full RAG loop for the published book --- ## 🧠 Supported Query Modes (NEW) The system must support **two distinct query modes**: ### 1️⃣ Global Book RAG Mode (default) - User submits a question **without selecting any text** - FastAPI invokes the existing **Spec-3 agent** - Agent retrieves relevant chunks from **Qdrant** - Answer is generated **strictly from retrieved content** ### 2️⃣ Selected Text Mode (NEW) - User selects a portion of book text in the frontend - Frontend sends the following to FastAPI: - `question` - `selected_text` - FastAPI **bypasses Qdrant retrieval** - The selected text is injected directly as the **only allowed context** - Agent answers **strictly and exclusively** from the selected text - If the answer is not present in the selected text, the agent must respond: > “I don’t know based on the selected text.” --- ## 🧩 Backend Responsibilities (FastAPI) - Expose a chatbot endpoint (e.g. `/chat`) - Accept payloads containing: - `question` - optional `selected_text` - Determine execution mode: - If `selected_text` is present → **Selected Text Mode** - Otherwise → **Global Book RAG Mode** - Invoke the existing agent logic from `agent.py` - **Do NOT modify** the core agent implementation - Return agent responses to the frontend --- ## 🖥️ Frontend Responsibilities - Render a floating chatbot icon - Toggle chatbot open/close on click - Display user messages and agent responses distinctly - Allow users to: - Ask general questions about the book - Select text from the book and ask context-specific questions - When text is selected: - Capture the selected content - Send it along with the user question to FastAPI --- ## ✅ Success Criteria - A FastAPI backend exposes an endpoint for chatbot queries - A floating chatbot icon is visible on the frontend - Clicking the icon opens and closes the chatbot interface - The chatbot UI is visually clean and user-friendly - User messages and agent responses are clearly distinguishable - The frontend sends user queries to the FastAPI backend - FastAPI invokes the existing agent logic from `agent.py` **without modification** - The agent retrieves relevant context from Qdrant in global mode - The agent answers strictly from user-selected text in selected-text mode - Responses are rendered correctly in the frontend - Users can ask multiple questions sequentially without errors - The system works end-to-end in a local development environment --- ## ⚙️ Constraints - Agent logic must remain unchanged (reuse Spec-3 implementation) - Backend framework: **FastAPI** - Frontend: web-based chatbot (HTML/JS or Docusaurus React component) - Chatbot UI must be lightweight and responsive - Communication must be local (development setup) - No re-embedding or re-ingestion of data - Responses must remain strictly grounded in provided context - Minimal additional infrastructure --- ## 🚫 Not Building - Authentication or authorization - Production deployment or scaling - Streaming responses - Long-term chat history persistence - Analytics or monitoring dashboards

## Response snapshot

Created new feature `010-rag-chatbot-integration`.
- **Branch**: `010-rag-chatbot-integration`
- **Specification**: `specs/010-rag-chatbot-integration/spec.md`
- **Checklist**: `specs/010-rag-chatbot-integration/checklists/requirements.md`

The specification has been created based on your description and is ready for the next phase.

## Outcome

- ✅ Impact: Created a new feature specification and all associated files.
- 🧪 Tests: No tests were run.
- 📁 Files: 3 files created.
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: The process was smooth, but the initial script execution failure required manual intervention. The user's prompt was very detailed, which made spec creation straightforward.
