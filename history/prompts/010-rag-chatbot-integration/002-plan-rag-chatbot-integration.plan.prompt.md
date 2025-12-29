---
id: 002
title: Plan RAG Chatbot Integration
stage: plan
date: 2025-12-29
surface: agent
model: gemini-cli
feature: 010-rag-chatbot-integration
branch: 010-rag-chatbot-integration
user:
command: /sp.plan
labels: [plan, backend, frontend, fastapi, react]
links:
  spec: specs/010-rag-chatbot-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/010-rag-chatbot-integration/plan.md
  - specs/010-rag-chatbot-integration/research.md
  - specs/010-rag-chatbot-integration/data-model.md
  - specs/010-rag-chatbot-integration/contracts/openapi.yaml
  - GEMINI.md
tests:
  - none
---

## Prompt

/sp.plan Plan FastAPI, frontend chatbot, and UI integration to complete the RAG agent system with global and selected-text question answering

---

## 🔧 Technical Scope

### 🧠 Backend (FastAPI)

- Create a FastAPI application in the backend 
- Accept user queries from the frontend via the `/chat` endpoint
- Pass the user query (and optional selected text) to the existing agent invocation function
- Return the agent’s generated response back to the frontend in a structured JSON format 
- Import and reuse the existing agent from `backend/agent.py`  
- Agent implementation **MUST remain unchanged**  
- Reuse the manually corrected **Spec-3 agent** using the official **OpenAI Agents SDK**  
- Expose a **POST** endpoint (e.g., `/chat`) that:
  - Accepts a JSON payload containing:
    - `question` (string, required)
    - `selected_text` (string, optional)

---

## 🔀 Query Mode Handling

### 🌍 Global Book RAG Mode (default)

- Triggered when `selected_text` is **NOT provided**
- Pass the `question` to the existing agent
- Agent retrieves context from **Qdrant**
- Agent generates an answer **strictly from retrieved chunks**

### ✂️ Selected Text Mode (NEW)

- Triggered when `selected_text` **IS provided**
- **Bypass Qdrant retrieval**
- Inject `selected_text` directly as the **only allowed context**
- Invoke the existing agent logic **without modifying its core**
- If the answer is not found in the selected text, return:

> “I don’t know based on the selected text.”

---

## ⚠️ Error Handling

- Handle basic backend errors:
  - Empty or missing `question`
  - Invalid payload format
  - Agent execution failures
- Return **user-friendly error messages** to the frontend

---

## 🖥️ Frontend (Chatbot UI)

- Build a web-based chatbot interface:
  - HTML/JS **or**
  - Docusaurus React component
- Add a **floating chatbot icon/button** fixed on all book pages
- Clicking the icon toggles the chatbot **open and closed**

---

## 🎨 Chatbot UI Design

- Clean and attractive chat window with:
  - Scrollable message area
  - Input field for user questions
  - Send button
- Clearly distinguish:
  - User messages
  - Agent responses
- Responsive layout that does **not obstruct** main content

---

## ✂️ Selected Text Interaction (NEW)

- Allow users to select text from the book content
- When text is selected:
  - Capture the selected text
  - Provide an action (e.g., button or context option) to **“Ask about selection”**
- When the user asks a question:
  - Send both `question` and `selected_text` to the FastAPI `/chat` endpoint
- Ensure:
  - Selected text is sent **only when explicitly chosen**
  - Normal questions continue to work **without selection**

---

## 🔗 Frontend–Backend Integration

- Connect frontend to FastAPI using HTTP requests (`fetch` / AJAX)
- Send requests to `/chat` with:
  - Question only → **Global Book RAG Mode**
  - Question + selected text → **Selected Text Mode**
- Receive and render agent responses dynamically
- Allow **multiple consecutive questions** in a single session

---

## 🧪 Validation & Testing

- Verify full end-to-end flow:
  - User opens chatbot via floating icon
  - User asks a general book question
  - Agent retrieves context from Qdrant
  - Answer is displayed in the chatbot
- Verify selected-text flow:
  - User selects text in the book
  - User asks a question about that text
  - Agent answers strictly from selected text
  - Out-of-context questions return the fallback response
- Confirm:
  - No changes were required to agent core logic
  - Both modes work reliably in local development

---

## 📦 Deliverables

- FastAPI backend exposing a `/chat` endpoint  
- Floating chatbot icon with toggle behavior  
- Clean, responsive chatbot UI  
- Support for:
  - Global book questions
  - Selected-text-only questions  
- Demonstration of complete end-to-end RAG interaction

---

## 🚫 Exclusions

- No changes to agent or vector retrieval logic  
- No authentication or authorization  
- No production deployment or scaling  
- No streaming responses  
- No long-term chat history persistence  
- No analytics or monitoring dashboards

## Response snapshot

Created the implementation plan for feature `010-rag-chatbot-integration`.
- **Plan**: `specs/010-rag-chatbot-integration/plan.md`
- **Research**: `specs/010-rag-chatbot-integration/research.md`
- **Data Model**: `specs/010-rag-chatbot-integration/data-model.md`
- **API Contract**: `specs/010-rag-chatbot-integration/contracts/openapi.yaml`
Agent context has been updated with new technologies.

## Outcome

- ✅ Impact: Created a new implementation plan and all associated artifacts.
- 🧪 Tests: No tests were run.
- 📁 Files: 5 files created/modified.
- 🔁 Next prompts: /sp.tasks
- 🧠 Reflection: The process of creating a plan from a detailed spec is straightforward. The manual fallback for script failures is now a standard procedure. The agent context update is a bit of a guess, but seems like the right direction.
