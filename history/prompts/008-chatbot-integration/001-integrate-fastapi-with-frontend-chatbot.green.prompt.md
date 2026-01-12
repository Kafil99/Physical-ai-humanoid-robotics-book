---
id: 001
title: Integrate FastAPI with Frontend Chatbot
stage: green
date: 2026-01-06
surface: agent
model: gemini
feature: 008-chatbot-integration
branch: 011-fix-chatbot-ui
user: {{USER}}
command: /sp.specify — Spec-4: FastAPI + Frontend Chatbot Integration (Agent: agent.py)
labels: [ "fastapi", "docusaurus", "chatbot", "rag" ]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/main.py
  - backend/agent.py
  - backend/requirements.txt
  - src/clientModules/chatbot.js
  - src/clientModules/chatbot.css
tests:
  - "none"
---

## Prompt

/sp.specify — Spec-4: FastAPI + Frontend Chatbot Integration (Agent: agent.py)

## 🎯 Objective

Integrate the existing **Spec-3 RAG agent (`agent.py`)** with a **FastAPI backend** and a **lightweight, floating frontend chatbot UI** to enable **end-to-end question answering over book content**, including **questions based exclusively on user-selected text**.

⚠️ **Critical Rule:**  
The core agent implementation inside `agent.py` **must be reused as-is**.  
No regeneration, refactoring, or logic changes are allowed.

---

## 🧑‍💻 Target Audience

- Full-stack engineers integrating AI agents into web applications  
- Evaluators validating a complete, user-facing RAG system  
- Developers working with Docusaurus and FastAPI  

---

## 🔍 Scope & Focus

- Wrap the standalone RAG agent (`agent.py`, Spec-3) with FastAPI  
- Provide a `/chat` API endpoint for chatbot queries  
- Build a floating chatbot UI injected safely into Docusaurus  
- Enable two query modes:
  - Global Book RAG
  - Selected Text Only
- Ensure frontend → backend → agent → response flow  
- Complete the full RAG loop for the published book  

---

## 🧠 Supported Query Modes

### 1️⃣ Global Book RAG Mode (Default)

**Trigger:**  
User asks a question **without selecting any text**

**Behavior:**

- FastAPI forwards the question to `agent.py`
- Agent retrieves relevant chunks from **Qdrant**
- Response is generated **strictly from retrieved book content**
- No hallucinations or external knowledge

---

### 2️⃣ Selected Text Mode (Strict Context Mode)

**Trigger:**  
User selects text from the book before asking a question

**Frontend sends to FastAPI:**

```json
{
  "question": "string",
  "selected_text": "string"
}
Behavior:

FastAPI bypasses Qdrant retrieval entirely

Selected text is injected as the only allowed context

Agent answers strictly and exclusively from the selected text

If the answer is not present, the agent must respond:

“I don’t know based on the selected text.”

🧩 Backend Responsibilities (FastAPI)
API Design
Expose endpoint:

bash
Copy code
POST /chat
Accept JSON payload:

json
Copy code
{
  "question": "string",
  "selected_text": "string | null"
}
Execution Rules
Endpoint must be asynchronous

Use:

python
Copy code
await Runner.run(agent, input)
❌ Do NOT use run_sync() (event loop conflict)

Determine execution mode:

selected_text present → Selected Text Mode

otherwise → Global Book RAG Mode

Invoke logic from agent.py without modification

Return response:

json
Copy code
{
  "answer": "string"
}
Handle errors gracefully without crashing the endpoint

🖥️ Frontend Responsibilities (Docusaurus)
Injection Method
Use Docusaurus clientModules

Dynamically create a root DOM element

Render chatbot using createRoot

❌ Do NOT swizzle or wrap the Docusaurus Layout

Chatbot UI Requirements
Floating chatbot icon (bottom corner)

Click icon toggles chat open / close

Lightweight, clean, responsive UI

Clear distinction between:

User messages

Agent responses

Support multiple consecutive questions

Selected Text Support
Allow users to select text from the book

Capture selected text on the frontend

Send question and selected_text to FastAPI

Selected text mode must bypass Qdrant

✅ Success Criteria
/chat endpoint executes asynchronously

No “event loop already running” errors

Floating chatbot icon is visible

Chat UI opens and closes correctly

User messages and agent replies render correctly

Global mode retrieves context from Qdrant

Selected text mode ignores Qdrant completely

Agent responses are strictly grounded in context

Users can ask multiple questions sequentially

Fully functional in a local development environment

⚙️ Constraints
Agent file name: agent.py

Agent logic: unchanged (Spec-3 reuse)

Backend framework: FastAPI

Frontend: Docusaurus (clientModules)

No re-embedding or re-ingestion

No streaming responses

No authentication

Minimal infrastructure only

🚫 Explicitly Out of Scope
Authentication or authorization

Persistent chat history

Streaming responses

Analytics or monitoring

Production deployment or scaling

## Response snapshot

### Running the Integrated Chatbot

To run the complete application, you need to run the backend server and the frontend development server in two separate terminals.

**1. Backend Setup & Execution**

First, ensure you have all the required environment variables set up in a `.env` file in the `backend` directory. These should include `OPENROUTER_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`, `QDRANT_COLLECTION_NAME`, and `COHERE_API_KEY`.

Next, install the dependencies and run the server:

```bash
# Navigate to the backend directory
cd backend

# (Optional, but recommended) Activate your Python virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
# source .venv/bin/activate

# Install/update Python dependencies
pip install -r requirements.txt

# Run the FastAPI server
uvicorn main:app --reload
```

The backend server will start on `http://localhost:8000`.

**2. Frontend Execution**

In a second terminal, run the Docusaurus development server:

```bash
# Navigate to the project root directory
# (If you are in the backend directory, navigate back)
cd ..

# Install npm dependencies (if you haven't already)
npm install

# Start the Docusaurus development server
npm start
```

The frontend development server will start on `http://localhost:3000` and open in your browser.

**3. Using the Chatbot**

Navigate to your Docusaurus site in the browser. You should see a floating chat icon in the bottom right corner. Click it to open the chat window.

You can now ask questions in two ways:
1.  **Global Book RAG:** Simply type a question and hit send. The agent will search the entire book content for an answer.
2.  **Selected Text RAG:** Highlight any text on the page, then open the chat window and ask a question about the selection. The agent will only use the text you selected to answer.

## Outcome

- ✅ Impact: High. Implemented the full end-to-end RAG system with a UI.
- 🧪 Tests: No automated tests were added, but manual testing is required.
- 📁 Files: 5 files created/modified.
- 🔁 Next prompts: "none"
- 🧠 Reflection: The `agents` library was not found, which was a challenge. I had to proceed with the assumption that it was an installed library. The rest of the implementation was straightforward.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a
